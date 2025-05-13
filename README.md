# Project-SmartFactory

![image](https://github.com/user-attachments/assets/dd5ef29f-0fd9-4608-bd37-edbe52ff2812)

![20250508_090039](https://github.com/user-attachments/assets/23c348de-7685-4770-a19a-71248c354326)

![20250508_090059](https://github.com/user-attachments/assets/bd1d6951-a3c7-4b2a-a308-2f9730dd5610)


## ⚙️ 사용 기술 스택

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenVINO-0099CC?style=for-the-badge&logo=intel&logoColor=white"/>
  <img src="https://img.shields.io/badge/MobileNetV3-4479A1?style=for-the-badge&logo=tensorflow&logoColor=white"/>
  <img src="https://img.shields.io/badge/OTX-FF6F00?style=for-the-badge&logo=openvino&logoColor=white"/>
  <img src="https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white"/>
  <img src="https://img.shields.io/badge/Logitech%20C270%20HD-C92228?style=for-the-badge&logo=logitech&logoColor=white"/>
  <img src="https://img.shields.io/badge/iotdem--color-00B8D4?style=for-the-badge&logo=palette&logoColor=white"/>
</p>

## 실행 방법
smart-factory 내의 readme를 따라 환경설정 후 arduino 디렉토리 내에서 $ make init, $ make build, $ make flash 순으로 명령 실행.
그 후 smart-factory내의 factory.py 실행.

## 프로젝트 개요

생산 라인에서 물체의 **불량 여부(O/X)**와 **색상(예: 파란색)**을 자동으로 분류하여, 아두이노와 연결된 액추에이터를 통해 물체를 레일에서 제거하는 스마트 팩토리 모형 시스템을 구현하였습니다. AI 모델을 직접 학습하고, 색상 인식 로직과 하드웨어 제어까지 통합한 프로젝트입니다.

## AI 모델 개발 과정

### ✔ 모델 선택 및 학습
* 모델 구조: MobileNetV3-Large

* 프레임워크: OTX (OpenVINO Training Extension)

* 입력 데이터: O 또는 X가 표시된 원형 물체의 이미지

* 출력: O / X 분류

### ✔ 학습 데이터 수집 및 트러블슈팅

* 초기에는 소수의 이미지로 학습 → 낮은 정확도
* 해결 방법:

* 다양한 조명, 각도에서 이미지 수집

* 단순히 이미지 수를 늘리는 것만으로는 성능이 크게 개선되지 않음을 경험

* → 모델 구조 변경 실험, 에폭 수 조절 등의 추가 실험 수행

* 에폭 수가 무조건 많다고 성능이 좋은 것은 아님을 직접 실험을 통해 체감

### ✔ 모델 배포
* 학습 완료 후 .xml, .bin 형식으로 export → OpenVINO 기반 디바이스에서 추론 수행

## 🎥 시스템 구성
### 하드웨어 구성
* 카메라: Logitech C270 HD (2대, 전방/후방)

* MCU: Arduino Mega 2560

* 출력 장치: 액추에이터 (2개), LED, 모터 레일

* 센서 제어 흐름:

첫 번째 카메라: O/X 분류 → X면 액추에이터 작동

두 번째 카메라: 색상 분류 → 파란색이면 다른 액추에이터 작동

### 색상 분류 방식
* 라이브러리: iotdem-color

* 구성 파일: color.cfg

* RGB 범위 기준으로 파란색 감지

## ⚠ 트러블슈팅 & 실험 기록
| 문제 | 분석 | 해결 |
|----|----|----|
| 모델이 X를 잘 인식하지 못함 |	데이터 부족, 단조로운 배경 | 다양한 배경/조명에서 다량의 이미지 수집 및 정밀 라벨링 |
| 성능 저하 | 학습 데이터만 증가 | 에폭 수, 모델 아키텍처 등 하이퍼파라미터 조정 |
| 오버피팅 | 에폭 수 과다 |	에폭 수를 적절히 줄이고 검증 데이터를 적극 활용 |

## 결과 및 배운 점
* 임베디드 환경에서도 동작 가능한 AI 기반 실시간 분류 시스템 구현

* 단순히 "학습 이미지 수를 늘리는 것"이 아니라, 모델 구조, 하이퍼파라미터 조정, 데이터 다양성 확보가 중요함을 실험을 통해 학습

* AI와 IoT 시스템을 통합


