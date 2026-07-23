# 🖐️ YOLOv5 Custom 6-Class Gesture & Person Detection (Jetson Nano Edge AI)

> **Jetson Nano 엣지 디바이스 환경 최적화를 위한 2,400장 데이터셋 기반 YOLOv5 75% 초경량화 커스텀 모델 (mAP50 96.0%)**

---

## 📌 프로젝트 개요 (Overview)

본 프로젝트는 무거운 표준 YOLOv5s 모델(702만 파라미터)을 **Jetson Nano 4GB RAM 및 640x480 웹캠 해상도** 환경에 맞춰 **1.76M 파라미터(75% 감축, 3.9MB)**로 다이어트 설계한 6-클래스 커스텀 객체 탐지 모델입니다.

신규 2,400장 고품질 데이터셋과 공식 사전 학습 뇌(`yolov5n.pt`)의 무게중심을 100% 온전히 승계받아 **전체 평균 mAP50 96.0% (정밀도 97.8%)**의 압도적 정확도를 달성하며, **640x480 직사각형 학습(`--img 640 --rect`) 및 TensorRT FP16 가속을 통해 45~55 FPS의 고속 실시간 추론**을 구현합니다.

---

## ✨ 주요 특징 (Key Features)

* **⚡ 75% 초경량화 사전 학습 계승 모델 (`yolov5_gesture_slim.yaml`):**
  * 파라미터 수: `7.02M` ➔ **`1.76M (1,763,224 개)`** (약 75% 감축)
  * 레이어 수: **`157 개`** (Backbone 100% 계승)
  * 가중치 파일 용량: **`3.9 MB`** (`best.pt`)
* **📹 640x480 웹캠 1대1 직사각형 해상도 최적화 (`--img 640 --rect`):**
  * 4:3 비율 웹캠 영상을 여백 패딩 없이 직관적으로 연산하여 속도 20% 상승 및 메모리 절감.
* **🎯 6개 클래스 동시 정밀 탐지 (mAP50 96.0%):**
  * **전체 정밀도 (Precision):** **`97.8%`**
  * **전체 재현율 (Recall):** **`93.9%`**
  * **전체 평균 mAP50:** **`96.0%`** (사람과 5종류 손 제스처 한 프레임 동시 탐지)
* **🛡️ Jetson Nano OOM(메모리 초과) 완전 차단:**
  * RAM 점유율을 **1.1GB 이하**로 안전하게 통제하여 메모리 폭발 방지.
* **🚀 TensorRT FP16 가속:**
  * Throughput **45 ~ 55 FPS** 실시간 웹캠 추론 가능.

---

## 📂 프로젝트 파일 구조 (Repository Structure)

```text
git_gesture/
├── README.md                           # 📖 프로젝트 메인 설명서
├── guide.md                            # 📘 Jetson Nano 배포 & 트러블슈팅 통합 가이드북
├── weights_170_480x680_newdata/
│   ├── best.pt                         # 🔥 2,400장 6-클래스 640x480 최적 가중치 (3.9MB, mAP 96.0%)
│   └── last.pt                         # 📦 마지막 에포크 가중치 파일
└── yolov5/                             # 🐍 실행 소스코드 및 모델 설정
    └── models/yolov5_gesture_slim.yaml # ⚙️ 1.76M 커스텀 신경망 구조 설정 파일 (nc: 6)
```

---

## 📊 모델 성능 비교 (Performance Comparison)

| 지표 | 기존 YOLOv5s | 커스텀 슬림 모델 (`weights_170_480x680_newdata`) | 개선 및 감축 효과 |
| :--- | :---: | :---: | :---: |
| **파라미터 수 (Parameters)** | 7,025,000 개 (7.02M) | **1,763,224 개 (1.76M)** | **약 75% 감축** 📉 |
| **가중치 용량 (Weight Size)** | ~15.0 MB | **3.9 MB** | **약 74% 다이어트** 📦 |
| **학습 데이터 수 (Dataset)** | 620 장 | **2,400 장 (무결 라벨)** | **데이터 규모 4배 확장** 📈 |
| **탐지 클래스 수 (Classes)** | 3 개 (`person`, `fist`, `palm`) | **6 개 (`fist`, `like`, `no_gesture`, `ok`, `palm`, `person`)** | **다양한 제스처 수용** 🖐️ |
| **정밀도 (Precision)** | ~74.9% | **97.8%** | **오탐률 극소화 (97.8%)** 🔥 |
| **종합 정확도 (mAP50)** | ~73.9% | **96.0%** | **96.0% 극상 달성** 🔥 |
| **Jetson Nano 속도 (FP16)** | ~22 FPS | **45 ~ 55 FPS** | **속도 2배 이상 향상** 🚀 |
| **Jetson RAM 점유율** | ~3.8 GB (OOM 위험) | **~1.1 GB** | **메모리 폭발 완전 통제** 🛡️ |

---

## 🎯 클래스 정보 (Class Labels)

```yaml
0: fist        # 주먹 제스처 ✊
1: like        # 따봉 / 엄지척 👍
2: no_gesture  # 일반 손 / 제스처 없음 ✋
3: ok          # 오케이 👌
4: palm        # 보자기 / 펼친 손 🖐️
5: person      # 사람 전체 / 상반신 👤
```

---

## 🚀 빠른 시작 가이드 (Quick Start)

### 1) 저장소 클론 (Jetson Nano 또는 PC)
```bash
git clone https://github.com/leeseungjae03046-alt/gesture_project.git
cd gesture_project
```

### 2) Jetson Nano TensorRT FP16 가속 엔진 빌드 (640x480)
```bash
# 1. ONNX 변환 (높이 480, 너비 640)
python3 export.py --weights weights_170_480x680_newdata/best.pt --img 480 640 --batch 1 --include onnx

# 2. trtexec 가속 컴파일
/usr/src/tensorrt/bin/trtexec --onnx=weights_170_480x680_newdata/best.onnx --saveEngine=best.engine --fp16 --workspace=1024 --avgRuns=1
```

### 3) 실시간 640x480 웹캠 추론 테스트
```bash
python3 detect.py --weights best.engine --img 480 640 --conf 0.25 --source 0 --data data.yaml
```

---

## 📘 전체 배포 상세 가이드
젯슨 나노 OS 환경 패치 명령어(`numpy==1.19.4`, `tensorrt` 심볼릭 링크 등) 및 트러블슈팅 내역은 **[guide.md](file:///home/daegu/canlab_workspace/git_gesture/guide.md)** 가이드북을 참고해 주세요!
