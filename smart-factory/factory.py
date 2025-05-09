#!/usr/bin/env python3

import os
import threading
from argparse import ArgumentParser
from queue import Empty, Queue
from time import sleep

import cv2
import numpy as np
import openvino as ov
from pathlib import Path
#from openvino.inference_engine import IECore

from iotdemo import FactoryController, MotionDetector, ColorDetector

FORCE_STOP = False


def thread_cam1(q):
    # 모션 감지기 초기화
    Motion = MotionDetector()
    Motion.load_preset('resources/motion.cfg')

    # OpenVINO 로드 및 초기화
    device = "CPU"

    base_artifacts_dir = Path("resources").expanduser()
    model_name = "exported_model"
    model_xml_name = f"{model_name}.xml"
    model_xml_path = base_artifacts_dir / model_xml_name

    core = ov.Core()
    model = core.read_model(model=model_xml_path)
    compiled_model = core.compile_model(model=model, device_name=device)
    output_layer = compiled_model.output(0)
    
    # 비디오 파일 열기
    cap = cv2.VideoCapture('resources/conveyor.mp4')
    
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # 라이브 프레임 큐에 추가
        q.put(('VIDEO:Cam1 live', frame))
        
        # 모션 감지 수행
        detected = Motion.detect(frame)
        if detected is None:
            continue
            
        # 감지된 프레임 큐에 추가
        q.put(('VIDEO:Cam1 detected', detected))
        
        # 이미지 전처리
        frame = cv2.cvtColor(detected, cv2.COLOR_BGR2RGB)
        reshaped = frame[:, :, [2, 1, 0]]
        np_data = np.moveaxis(reshaped, -1, 0)
        preprocessed_numpy = [((np_data / 255.0) - 0.5) * 2]
        batch_tensor = np.stack(preprocessed_numpy, axis=0)

        # OpenVINO 추론 실행
        results = compiled_model([batch_tensor])[output_layer]
        
        # 결과 처리 (모델에 따라 조정 필요)
        # 예시: 결과에서 x와 원 비율 추출
        x_ratio = abs(results[0][0]) * 50
        circle_ratio = abs(results[0][1]) * 50
        
        print(f"X = {x_ratio:.2f}%, Circle = {circle_ratio:.2f}%")

        # 액추에이터 1 제어
        if x_ratio > 60:  # 임계값은 적절히 조정
            q.put(("PUSH", 1))

    cap.release()
    q.put(('DONE', None))
    exit()


def thread_cam2(q : Queue):
    # TODO: MotionDetector
    motiondetector=MotionDetector()
    motiondetector.load_preset("resources/motion.cfg")
    # TODO: ColorDetector
    cColor=ColorDetector()
    cColor.load_preset("resources/color_cap.cfg")
    # TODO: HW2 Open "resources/conveyor.mp4" video clip
    cap=cv2.VideoCapture("resources/conveyor.mp4")
    while not FORCE_STOP:
        sleep(0.03)
        _, frame = cap.read()
        if frame is None:
            break

        # TODO: HW2 Enqueue "VIDEO:Cam2 live", frame info
        q.put(("VIDEO:Cam2 live", frame))
        # TODO: Detect motion
        detected=motiondetector.detect(frame)
        if detected is None:
            continue
        # TODO: Enqueue "VIDEO:Cam2 detected", detected info.
        q.put(("VIDEO:Cam2 detected", detected))
        # TODO: Detect color
        name, ratio = cColor.detect(detected)[0]
        # TODO: Compute ratio
        ratio=ratio*100
        print(f"{name}: {ratio:.2f}%")
       
        # TODO: Enqueue to handle actuator 2
        if name=="blue":
            q.put(('PUSH',2))
    cap.release()
    q.put(('DONE', None))
    exit()


def imshow(title, frame, pos=None):
    cv2.namedWindow(title)
    if pos:
        cv2.moveWindow(title, pos[0], pos[1])
    cv2.imshow(title, frame)


def main():
    global FORCE_STOP

    parser = ArgumentParser(prog='python3 factory.py',
                            description="Factory tool")

    parser.add_argument("-d",
                        "--device",
                        default=None,
                        type=str,
                        help="Arduino port")
    args = parser.parse_args()

    # TODO: HW2 Create a Queue
    q = Queue()
    
    # TODO: HW2 Create thread_cam1 and thread_cam2 threads and start them.
    t1 = threading.Thread(target=thread_cam1, args=(q,))
    t2 = threading.Thread(target=thread_cam2, args=(q,))

    t1.start()
    t2.start()

    with FactoryController(args.device) as ctrl:
        while not FORCE_STOP:
            if cv2.waitKey(10) & 0xff == ord('q'):
                break

            # TODO: HW2 get an item from the queue. You might need to properly handle exceptions.
            # de-queue name and data
            try:
                name, frame=q.get_nowait()
            except Empty:
                continue


            # TODO: HW2 show videos with titles of 'Cam1 live' and 'Cam2 live' respectively.
            if name[-4:]=='live':
                cv2.imshow(name[6:],frame)
            elif name[-8:]=='detected':
                cv2.imshow(name[6:],frame)
            # TODO: Control actuator, name == 'PUSH'
            elif name=='PUSH':
                ctrl.push_actuator(frame)
            elif name == 'DONE':
                FORCE_STOP = True

            q.task_done()

    cv2.destroyAllWindows()
    t1.join()
    t2.join()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        os._exit()
