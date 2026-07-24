# 📘 YOLOv5 UltraFast (113 FPS) 제스처 프로젝트 통합 개발 & 마스터 가이드북

> **최종 수정일:** 2026년 7월 24일  
> **대상 환경:** Jetson Nano 4GB DevKit + Arduino Serial Control  
> **프로젝트 루트:** `~/canlab/git_communicate/gesture_project/gesture_final`

---

## 📜 1. 프로젝트 개발 진행 이력 및 트러블슈팅 잔혹사 (History)

본 프로젝트는 Jetson Nano의 4GB RAM 한계와 CUDA 텐서 연산 트러블을 극복하며 113 FPS 최고속 반응 속도를 달성하기까지의 정밀 엔지니어링 기록입니다.

### 🚨 주요 해결 트러블슈팅 내역
1. **Jetson Nano RAM 포화 (OOM 렉) 문제**:
   * **상황**: 표준 YOLOv5s (702만 파라미터) 640px 추론 시 4GB RAM 중 3.8GB 이상을 점유하며 메모리 스와핑 렉 발생.
   * **해결**: 신경망 구조를 `width: 0.25`, `depth: 0.33`으로 75% 다이어트하여 **1.76M 파라미터(3.7MB)** 슬림 모델(`yolov5_gesture_slim.yaml`)을 커스텀 설계함.
2. **`AssertionError: im.shape == engine.binding_shape` 차원 불일치 오류**:
   * **상황**: `detect.py` 기동 시 `--img 320` 단일 숫자를 넘기면 YOLOv5 코드가 내부적으로 `[320, 320]` 정방형으로 자동 확장하여 가속 엔진 텐서 차원과 안 맞아 에러 발생.
   * **해결**: 가속 엔진 컴파일 당시의 실제 바인딩 차원인 **`--img 256 320`** (높이 256 x 너비 320)으로 2개의 숫자를 직접 정합 명시하여 에러 0% 및 113 FPS 속도 확보.
3. **`IndexError: list index out of range` 라벨 오류**:
   * **상황**: 훈련 모델은 6개 클래스인데 `dataset.yaml` 파일이 3개 클래스로 남아있어 발생.
   * **해결**: `dataset.yaml` 파일의 `nc: 6` 및 6개 `names` 리스트를 훈련 당시 순서와 1대1로 일치시킴.
4. **리눅스 터미널 `Ctrl + S` 얼음 현상**:
   * **해결**: **`Ctrl + Q`** 키를 누르면 얼어있던 터미널 화면이 1초 만에 풀림.

---

## 🛠️ 2. 가상환경 및 개발 환경 세팅 명세

* **OS**: JetPack 4.6 (Ubuntu 18.04 LTS / L4T R32.6.1)
* **Python**: `Python 3.6.9` (가상환경 경로: `/home/mijung/canlab/.venv`)
* **TensorRT**: `TensorRT 8.2.1` (`/usr/src/tensorrt/bin/trtexec`)
* **PyTorch / OpenCV**: `torch 1.9.0+cu102` / `OpenCV 4.5.4`

### 🐍 가상환경 활성화 명령어
```bash
source /home/mijung/canlab/.venv/bin/activate
```

---

## 📊 3. 최종 UltraFast 모델 벤치마크 및 6-Class 라벨 명세

* **파라미터 수:** `1.76M` (75% 감축)
* **가중치 파일 용량:** `3.7 MB` (`best.pt`)
* **TRT 입력 텐서 차원:** `[256, 320]`
* **실측 반응 지연시간:** **`8.6 ms (0.008초)`**
* **실측 프레임 속도:** **`113.27 FPS`** (초당 113 프레임 폭발적 처리)

```yaml
# 6개 클래스 라벨 명세 (dataset.yaml)
0: fist        # 주먹 ✊ (Command 'F')
1: like        # 따봉 👍 (Command 'L')
2: no_gesture  # 일반 손 ✋ (Command 'N')
3: ok          # 오케이 👌 (Command 'O')
4: palm        # 보자기 🖐️ (Command 'P')
5: person      # 사람 👤 (Command 'X')
```

---

## 📂 4. 깔끔하게 정립된 최종 프로젝트 디렉터리 구조

```text
gesture_project/
├── README.md                           # GitHub 메인 소개서
├── guide.md                            # [본 문서] 마스터 종합 기술 가이드북
├── markdown/                           # 리눅스 명령어(commands.md) 및 IP 접속 모음
└── gesture_final/                      # [독립 실행 단권화 메인 프로젝트]
    ├── dataset/                        # 독립 검증 데이터셋
    ├── dataset.yaml                    # 6개 클래스 라벨 매핑 파일
    ├── guide.md                        # gesture_final 단일 가이드
    ├── models/
    │   └── weights_170_320x240_ultrafast/
    │       ├── best.pt                 # 파이토치 원본 가중치 (3.7 MB)
    │       ├── best.onnx               # ONNX 변환 모델 (7.1 MB)
    │       └── best.engine             # [핵심] 113.27 FPS TensorRT FP16 가속 엔진 (6.9 MB)
    └── yolov5/                         # 경량화된 YOLOv5 소스
        ├── detect.py                   # 라이브 카메라 & 아두이노 송신 메인 실행 코드
        ├── export.py                   # ONNX 내보내기 도구
        ├── models/                     # 슬림 신경망 구조 레이어 정의
        └── utils/                      # 전처리 모듈
```

---

## 🚀 5. 실시간 웹캠 라이브 실행 명령어 (신뢰도 0.8 오탐 0% 세팅)

```bash
# 1. 가상환경 활성화 및 실행 경로 이동
source /home/mijung/canlab/.venv/bin/activate
cd ~/canlab/git_communicate/gesture_project/gesture_final/yolov5

# 2. UltraFast 113 FPS 카메라 감지 기동 (신뢰도 0.8 적용)
python3 detect.py --weights ../models/weights_170_320x240_ultrafast/best.engine --img 256 320 --conf 0.8 --source 0 --data ../dataset.yaml
```

---

## 🧹 6. RAM 캐시 및 스왑(Swap) 메모리 100% 완전 초기화 명령어

YOLO 구동 종료 후 램 페이지 캐시와 스왑 잔재를 100% 0으로 비우는 원클릭 콤보 명령어입니다:

```bash
sudo sysctl -w vm.drop_caches=3 && sudo swapoff -a && sudo swapon -a
```

---

## 🔌 7. 아두이노(Arduino) 시리얼 제어 이식 가이드

* **시리얼 통신 포트 / 속도**: `/dev/ttyACM0` (BaudRate: `115200` bps)
* **Python 송신 코드 구조 (`detect.py` 하단)**:
  ```python
  import serial
  py_serial = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
  
  if label == 'fist':
      py_serial.write(b'F\n')  # 주먹 ➔ 모터 접기
  elif label == 'palm':
      py_serial.write(b'P\n')  # 보자기 ➔ 모터 펼치기
  ```
* **Arduino C++ 수신 스케치 구조**:
  ```cpp
  void setup() {
    Serial.begin(115200);
    pinMode(13, OUTPUT);
  }
  void loop() {
    if (Serial.available()) {
      char cmd = Serial.read();
      if (cmd == 'F') digitalWrite(13, HIGH);
      else if (cmd == 'P') digitalWrite(13, LOW);
    }
  }
  ```
