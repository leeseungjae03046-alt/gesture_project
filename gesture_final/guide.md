# 📘 Jetson Nano UltraFast (113 FPS) 최종 구동 마스터 가이드북 (gesture_final)

> **프로젝트 위치:** `/home/mijung/canlab/gesture_final`  
> **최종 수정일:** 2026년 7월 24일  
> **구동 모델:** UltraFast 320x240 (`weights_170_320x240_ultrafast/best.engine`)  
> **실측 성능:** 지연시간 **`8.6 ms` (0.008초)**, **`113.27 FPS`**, RAM 점유율 **`1.2 GB 이하`** (OOM 렉 0%)

---

## 📌 1. 최종 독립 프로젝트 디렉터리 구조

`gesture_final` 폴더는 기존 폴더와의 의존성을 100% 끊어낸 완전 자립형 단권화 디렉터리입니다.

```text
/home/mijung/canlab/gesture_final/
├── dataset/                            # 테스트 및 검증용 독립 데이터셋
├── dataset.yaml                        # 6개 클래스 라벨 매핑 명세서
├── guide.md                            # [본 문서] UltraFast 전용 단일 통합 가이드북
├── models/
│   └── weights_170_320x240_ultrafast/  # UltraFast 전용 가속 엔진 저장소 (113 FPS)
│       ├── best.pt                     # 파이토치 가중치 (3.7 MB)
│       ├── best.onnx                   # ONNX 변환 모델 (7.1 MB)
│       └── best.engine                 # [핵심] TensorRT FP16 가속 엔진 (6.9 MB)
└── yolov5/                             # 경량화된 실행 소스 코드
    ├── detect.py                       # 카메라 및 아두이노 송신 메인 실행 파일
    ├── export.py                       # ONNX 변환 도구
    ├── models/                         # 슬림 신경망 구조 레이어 정의
    └── utils/                          # 전처리 및 시각화 모듈
```

---

## 🎯 2. 6개 클래스 ID 매핑표 (Class Specifications)

`dataset.yaml` 파일에 명시된 6개 클래스 라벨 정보입니다:

```yaml
0: fist        # 주먹 ✊ (Arduino Command 'F')
1: like        # 따봉 👍 (Arduino Command 'L')
2: no_gesture  # 일반 손 ✋ (Arduino Command 'N')
3: ok          # 오케이 👌 (Arduino Command 'O')
4: palm        # 보자기 🖐️ (Arduino Command 'P')
5: person      # 사람 👤 (Arduino Command 'X')
```

---

## 🚀 3. 독립 실행 및 아두이노 테스트 명령어

기존 폴더와 완전히 독립되어 `/home/mijung/canlab/gesture_final/yolov5` 경로에서 아래 단 1 줄의 명령어로 즉시 기동됩니다!

```bash
# 1. 가상환경 활성화 및 실행 폴더 이동
source /home/mijung/canlab/.venv/bin/activate
cd /home/mijung/canlab/gesture_final/yolov5

# 2. UltraFast (113 FPS) 카메라 감지 기동 (AssertionError 0%)
python3 detect.py --weights ../models/weights_170_320x240_ultrafast/best.engine --img 256 320 --conf 0.8 --source 0 --data ../dataset.yaml
```

---

## 🔍 4. 주요 매개변수(Parameter) 및 설정값 상세 설명

* **`--weights ../models/weights_170_320x240_ultrafast/best.engine`**: `gesture_final` 내부에 독립 보관된 113 FPS 실측 초고속 GPU 가속 엔진입니다.
* **`--img 256 320`**: **(핵심 정합 옵션)** UltraFast 가속 엔진의 실제 텐서 바인딩 크기(높이 256 x 너비 320)와 1대1로 정확히 정합시켜 `AssertionError`를 원천 차단하고 113 FPS 속도를 유지합니다.
* **`--conf 0.25`**: 25% 이상 확신하는 뚜렷한 6개 클래스 상자만 시각화합니다.
* **`--data ../dataset.yaml`**: `gesture_final` 내부의 6개 클래스 라벨 번역 파일입니다.

---

## 🔌 5. 아두이노(Arduino) 시리얼 제어 연동 가이드

`detect.py` 하단에 시리얼 송신 코드를 연동하여 탐지 결과를 아두이노로 송신합니다:

* **시리얼 설정**: Port `/dev/ttyACM0` (또는 `/dev/ttyUSB0`), BaudRate `115200`
* **송신 규격**:
  * `fist` 탐지 ➔ `'F'\n` 전송
  * `palm` 탐지 ➔ `'P'\n` 전송
  * `ok` 탐지 ➔ `'O'\n` 전송
  * `like` 탐지 ➔ `'L'\n` 전송
