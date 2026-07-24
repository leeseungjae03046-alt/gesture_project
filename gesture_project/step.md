# 📋 Arduino UNO Q (4GB) YOLOv5 제스처 탐지 프로젝트 이식 및 실행 절차 가이드 (step.md)

본 문서는 Jetson Nano 환경에서 개발된 `gesture_project` (YOLOv5 UltraFast)를 **Arduino UNO Q (4GB)** 공식 제원에 맞춰 커스텀하고 카메라를 연결하여 구동하기 위한 단계별 가이드입니다.

---

## 📸 1. Arduino UNO Q 공식 제원 및 카메라 연결 가이드

아두이노 정식 공식 문서(`docs.arduino.cc`) 기준 UNO Q 보드의 인터페이스 제원입니다.

### ❓ Qwiic 커넥터로 카메라 연결이 가능한가요?
* **불가능합니다.** 보드의 **Qwiic 커넥터**는 3.3V 기반의 **I2C 센서 통신 전용 포트** (온습도, 자이로, 버튼 등 Modulino 전용)입니다.
* 비디오 영상 데이터(초당 수십 MB~수백 MB)는 I2C 대역폭을 초과하므로 Qwiic으로는 카메라 영상을 전송할 수 없습니다.

### 📸 카메라 연결 방법 2가지

#### [방법 1] USB-C 포트 + USB C-to-A 젠더 (Arducam B0200 연결 - 가장 추천)
* **공식 제원**: UNO Q의 **USB Type-C 포트**는 USB Host 기능을 지원합니다.
* **연결 방식**:
  1. 보드의 USB-C 포트에 **`USB C-to-A 젠더`** (또는 USB-C 허브)를 꽂습니다.
  2. 보유 중이신 **Arducam 1080P USB 카메라(B0200)** 케이블을 젠더에 연결합니다.
* **인식 경로**: 리눅스 OS에서 `/dev/video0`으로 즉시 자동 인식됩니다.
* **실행 옵션**: `python3 detect.py --source 0`

#### [방법 2] 네트워크 영상 스트리밍 (노트북/스마트폰 카메라 활용)
* **공식 제원**: UNO Q 보드 상단에는 직접 꽂는 라즈베리파이형 CSI 플랫 슬롯이 없으며, 보드 하단(Bottom)의 하이스피드 헤더(High-Speed Header)를 통해 전용 카메라 확장 캐리어를 장착해야 합니다.
* 확장 캐리어가 없는 경우, **노트북/스마트폰의 웹캠 스트리밍 앱(RTSP/HTTP)**을 켜고 Wi-Fi 네트워크로 영상 스트림을 받아올 수 있습니다.
* **실행 옵션**: `python3 detect.py --source http://<노트북_IP>:8080/video`

---

## ⚙️ 2. Jetson Nano ➔ Arduino UNO Q 이식 절차 (커스텀 가이드)

### [단계 1] 환경 차이점 및 가중치 파일 변경 확인
* **가중치 파일 변경**: Jetson Nano 전용인 `best.engine` (TensorRT)은 NVIDIA GPU 전용이므로 UNO Q에서 작동하지 않습니다.
* **대응 파일**: `gesture_final/models/weights_170_256x320_ultrafast/best.pt` (PyTorch) 또는 `best.onnx` (ONNX Runtime)를 사용합니다.

### [단계 2] 파이썬 가상환경 생성 및 라이브러리 설치
```bash
# 1. 작업 디렉터리 이동
cd ~/main/canlab/gesture_project

# 2. 파이썬 3.13용 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate

# 3. 필요 패키지 설치
pip install torch torchvision opencv-python pillow pyyaml requests
# ONNX 사용 시: pip install onnxruntime
```

### [단계 3] `detect.py` 코드 수정 포인트 (사용자 직접 수정용)
`gesture_project/gesture_final/yolov5/detect.py` 파일을 열어 다음 설정을 확인 및 수정합니다.

1. **모델 가중치 경로**:
   * 기존: `../models/weights_170_256x320_ultrafast/best.engine`
   * 변경: `../models/weights_170_256x320_ultrafast/best.pt` (또는 `best.onnx`)
2. **카메라 소스 지정**:
   * Arducam (USB-C 젠더 연결): `--source 0`
   * 네트워크 스트리밍: `--source http://<IP>:8080/video`

### [단계 4] 최종 테스트 실행 명령어
```bash
# 가상환경 활성화 및 실행 경로 이동
source ~/main/canlab/gesture_project/.venv/bin/activate
cd ~/main/canlab/gesture_project/gesture_final/yolov5

# PyTorch best.pt 모델로 제스처 탐지 기동
python3 detect.py --weights ../models/weights_170_256x320_ultrafast/best.pt --img 256 320 --conf 0.8 --source 0 --data ../dataset.yaml
```
