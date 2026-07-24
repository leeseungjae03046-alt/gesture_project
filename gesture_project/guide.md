# 📘 YOLOv5 UltraFast Gesture Project Master Guidebook (Arduino UNO Q)

> **최종 수정일:** 2026년 7월 24일  
> **대상 보드:** Arduino UNO Q 4GB (`arduino,imola` / Qualcomm QRB2210 SoC)  
> **프로젝트 위치:** `/home/arduino/main/canlab/gesture_project`

---

## 🛠️ 1. 가상환경 원클릭 재복구 명령어 (`requirements.txt`)

새 보드나 새로운 디바이스에 프로젝트를 복제한 후 가상환경을 10초 만에 복구하는 방법입니다:

```bash
cd /home/arduino/main/canlab/gesture_project
python3 -m venv .venv
source .venv/bin/activate

# requirements.txt 기반 필요 의존성 자동 복구
pip install -r requirements.txt
```

---

## 📜 2. 오늘 완료한 핵심 개발 & 트러블슈팅 이력 (2026-07-24)

### 🚨 주요 해결 내역
1. **임시 디렉터리 디스크 용량 부족 (`[Errno 28] No space left on device`)**:
   * **원인**: `pip` 패키지 설치 시 시스템 가상 램 디스크 `/tmp` (1.8GB) 용량이 포화됨.
   * **해결**: eMMC 14GB 여유 공간이 있는 `TMPDIR=/home/arduino/main/canlab/gesture_project/tmp` 경로로 전환하여 의존성 전체 설치 완료.
2. **`Illegal instruction` ARM64 CPU C++ 튕김 현상**:
   * **원인**: `+cu130` (CUDA GPU) 패키지 및 PyTorch `fuse()` (레이어 병합 연산)가 ARM64 미지원 기계어 명령 호출.
   * **해결**: Pure ARM64 CPU 패키지(`torch-2.13.0+cpu`) 교체 및 [models/common.py](file:///home/arduino/main/canlab/gesture_project/gesture_final/yolov5/models/common.py#L305) `attempt_load(..., fuse=False)` 옵션 반영으로 100% 원천 해결.
3. **PyTorch 2.6+ `weights_only=False` 호환성 구현**:
   * [models/experimental.py](file:///home/arduino/main/canlab/gesture_project/gesture_final/yolov5/models/experimental.py#L96) `torch.load(..., weights_only=False)` 반영.
4. **`pkg_resources` Python 3.13 폴백 패치**:
   * [utils/general.py](file:///home/arduino/main/canlab/gesture_project/gesture_final/yolov5/utils/general.py#L27) `try-except packaging` 방어 코드로 Python 3.13 / setuptools 83+ 완벽 호환.
5. **퀄컴 Adreno 702 GPU (`FD702`) OpenCL 가속 구동 성공**:
   * `clinfo` 점검을 통해 `Platform: rusticl / Device: FD702` 검증.
   * `best.onnx` 모델을 OpenCV DNN OpenCL 백엔드(`--dnn`)로 구동하여 퀄컴 GPU 가속 추론 성공 (`shape: (1, 5040, 11)`).

---

## 🚀 3. 추천 실행 명령어 모음

#### [방법 1] 퀄컴 Adreno 702 GPU + ONNX 가속 실행 (추천 ⭐)
```bash
cd ~/main/canlab/gesture_project/gesture_final/yolov5
source ../../.venv/bin/activate

python3 detect.py --weights ../models/weights_170_256x320_ultrafast/best.onnx --dnn --source 'http://192.168.45.84:5000/video'
```

#### [방법 2] PyTorch CPU 실행
```bash
cd ~/main/canlab/gesture_project/gesture_final/yolov5
source ../../.venv/bin/activate

python3 detect.py --weights ../models/weights_170_256x320_ultrafast/best.pt --source 'http://192.168.45.84:5000/video'
```

#### [방법 3] 실시간 탐지 웹 스트리밍 서비스 실행 (크롬 `7000`번 포트 접속)
```bash
cd ~/main/canlab/gesture_project/gesture_final/yolov5
source ../../.venv/bin/activate

SOURCE_URL='http://192.168.45.84:5000/video' python3 web_detect.py
```

---

## 🔋 4. 하드웨어 전원 및 카메라 연결 표준 가이드

1. **전원 공급 구성 (PD IN 전원 필수)**
   * `PD 100W IN` 패스스루 포트가 포함된 C타입 멀티허브 (ipTIME UC305HDMI PLUS / DCH-H301) 사용.
   * 멀티허브 PD-IN 포트에 C타입 PD 충전기(20W~30W 이상) 전원 인가.
2. **카메라 연결 구성**
   * Arducam B0200 USB 카메라는 멀티허브의 USB 3.0 A타입 포트에 연결.
   * 실물 카메라 꽂은 후 실행 명령어: `python3 detect.py --source 0`

---

## 🎯 5. 향후 작업 로드맵 (Next Steps Roadmap)

1. **[1단계] PD 멀티허브 & Arducam 카메라 장착 테스트**
   * 택배 도착 시 Arducam 카메라 꽂고 퀄컴 GPU 가속 모델(`best.onnx + --dnn --source 0`) 기동 확인.
2. **[2단계] 손동작 기반 객체 추적 종료(Control) 기능 개발**
   * 특정 손 제스처(예: `fist` 주먹 ✊ 시 추적 종료, `palm` 보자기 🖐️ 시 추적 시작 등)를 감지했을 때 **객체 추적 루프를 제어하고 자동 종료/전환하는 제어 로직 개발**.
