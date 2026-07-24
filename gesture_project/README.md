# 🖐️ YOLOv5 UltraFast Gesture & Person Detection on Arduino UNO Q (4GB)

> **Arduino UNO Q (Imola) 엣지 디바이스 및 퀄컴 Adreno 702 GPU 가속 기반 초경량 커스텀 YOLOv5 엣지 AI 마스터 프로젝트**

---

## 📌 프로젝트 개요 (Overview)

본 프로젝트는 표준 YOLOv5s 모델(702만 개 파라미터)을 **1.76M 파라미터(75% 감축, 3.7MB)**로 다이어트 설계하여 **Arduino UNO Q (Imola 4GB RAM)** 보드 상에서 실시간 손 제스처(`fist`, `like`, `no_gesture`, `ok`, `palm`) 및 사람(`person`)을 탐지하고, 아두이노 모터 및 LED를 제어하는 엣지 AI 시스템입니다.

* **최종 수정일**: 2026년 7월 24일
* **하드웨어 디바이스**: Arduino UNO Q 4GB (`arduino,imola` / Qualcomm QRB2210 SoC)
* **내장 GPU가속기**: Qualcomm Adreno 702 OpenCL GPU (`FD702`)

---

## 📝 오늘 완료한 작업 내역 (2026-07-24 작업 기록)

### 1. ⚙️ 파이썬 3.13 가상환경 구축 및 의존성 완벽 정합
* **가상환경 디렉터리**: `/home/arduino/main/canlab/gesture_project/.venv`
* **디스크 용량 초과 해결**: `pip` 설치 시 `/tmp` (RAM 1.8GB) 용량 초과(`Errno 28`) 방지를 위해 `TMPDIR=/home/arduino/main/canlab/gesture_project/tmp` 설정 적용.
* **설치된 필수 라이브러리**:
  * `torch 2.13.0+cpu` & `torchvision 0.28.0+cpu` (Pure ARM64 CPU 바이너리)
  * `opencv-python-headless 5.0.0` (Headless Linux 전용)
  * `onnxruntime 1.27.0` (ARM64 ONNX 추론 엔진)
  * `pandas`, `tqdm`, `scipy`, `matplotlib`, `seaborn`, `thop`, `flask`, `setuptools<70`

### 2. 🛠️ 코드 호환성 및 튕김 에러 100% 해결 트러블슈팅
1. **`Illegal instruction` (ARM64 CPU C++ crash) 원천 해결**:
   * **원인**: CUDA 13.0 패키지(`+cu130`) 및 PyTorch `fuse()` (컨볼루션 레이어 융합 C++ 연산)가 ARM64 CPU 미지원 기계어 명령을 호출하여 발생.
   * **해결**: Pure ARM64 CPU PyTorch (`torch-2.13.0+cpu`) 교체 및 [models/common.py](file:///home/arduino/main/canlab/gesture_project/gesture_final/yolov5/models/common.py#L305) 305번 줄에 `fuse=False` 옵션 부여로 100% 해결.
2. **PyTorch 2.6+ `weights_only=False` 호환성 패치**:
   * [models/experimental.py](file:///home/arduino/main/canlab/gesture_project/gesture_final/yolov5/models/experimental.py#L96) 96번 줄에 `weights_only=False` 옵션 추가로 PyTorch 2.6 호환성 확보.
3. **`ModuleNotFoundError: No module named 'pkg_resources'` 해결**:
   * [utils/general.py](file:///home/arduino/main/canlab/gesture_project/gesture_final/yolov5/utils/general.py#L27) 27번 줄에 Python 3.13 `packaging` 폴백 예외 처리 적용.
4. **`qt.qpa.xcb: could not connect to display` 헤드리스 해결**:
   * 디스플레이 없는 터미널 환경 호환을 위해 `opencv-python-headless`로 전환 및 [utils/datasets.py](file:///home/arduino/main/canlab/gesture_project/gesture_final/yolov5/utils/datasets.py#L351) 351번 줄 `cv2.waitKey` 방어 패치.

### 3. ⚡ 퀄컴 Adreno 702 GPU 하드웨어 가속 검증 완료
* **Qualcomm Adreno 702 GPU (`FD702`)** 디바이스의 OpenCL (`rusticl`) 하드웨어 가속 검증 완료.
* `best.onnx` 모델을 OpenCV DNN OpenCL 백엔드(`--dnn`)로 구동하여 **`Qualcomm Adreno 702 OpenCL GPU Forward SUCCESS!`** (출력 텐서: `(1, 5040, 11)`) 검증 성공.

### 4. 🌐 웹 스트리밍 파이프라인 개발
* `laptop_webcam.py`: LG 그램 노트북 카메라 영상을 5000번 포트로 MJPEG 웹 송출.
* `web_detect.py`: 아두이노 보드에서 퀄컴 GPU + ONNX 탐지 결과를 7000번 포트로 실시간 웹 송출 (`http://192.168.45.124:7000`).

---

## ⚡ 모델 스펙 & 6개 클래스 정보

* **모델 파라미터**: `1.76M` (표준 YOLOv5s 대비 75% 다이어트 모델)
* **텐서 입력 크기**: `[256, 320]`
* **가중치 파일**: [best.pt](file:///home/arduino/main/canlab/gesture_project/gesture_final/models/weights_170_256x320_ultrafast/best.pt) (PyTorch) / [best.onnx](file:///home/arduino/main/canlab/gesture_project/gesture_final/models/weights_170_256x320_ultrafast/best.onnx) (ONNX)

```yaml
0: fist        # 주먹 ✊ (Command 'F')
1: like        # 따봉 👍 (Command 'L')
2: no_gesture  # 일반 손 ✋ (Command 'N')
3: ok          # 오케이 👌 (Command 'O')
4: palm        # 보자기 🖐️ (Command 'P')
5: person      # 사람 👤 (Command 'X')
```

---

## 🔋 하드웨어 전원 및 카메라 연결 가이드

* **전원 구성**: `PD-IN` (Power Delivery 100W) 정식 지원 멀티허브 (ipTIME UC305HDMI PLUS / DCH-H301) + C타입 PD 20W~30W 충전기 연결.
* **카메라 구성**: Arducam 1080P USB 카메라 (B0200) ➔ 멀티허브 USB-A 포트 연결 (`--source 0`).

---

## 🎯 향후 작업 로드맵 (Next Steps Roadmap)

1. **[1단계] PD 멀티허브 및 Arducam 카메라 구동 검증**
   * PD 멀티허브 도착 시 Arducam B0200 카메라를 보드 USB-A 포트에 꽂고, 퀄컴 GPU 가속 모델(`best.onnx + --dnn --source 0`) 정상 작동 확인.
2. **[2단계] 손동작 기반 객체 추적 종료(Control) 기능 개발**
   * 특정 손 제스처(예: `fist` 주먹, `palm` 보자기 등) 감지 시 **객체 추적(Object Tracking) 프로세스를 자동으로 제어 및 종료**하는 파이프라인 코드 작성.
