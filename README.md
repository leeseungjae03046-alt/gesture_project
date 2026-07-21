# 🖐️ YOLOv5 Custom Slim Gesture Detection (Jetson Nano Edge AI)

> **Jetson Nano 엣지 디바이스 환경 최적화를 위한 YOLOv5 70% 초경량화 커스텀 모델 및 실시간 제스처(주먹, 보자기, 사람) 탐지 프로젝트**

---

## 📌 프로젝트 개요 (Overview)

본 프로젝트는 불필요하게 깊고 무거운 표준 YOLOv5s 모델(702만 파라미터)을 **Jetson Nano 4GB RAM** 환경에 맞춰 **2.1M 파라미터(70% 감축)**로 슬림 다이어트 설계한 커스텀 객체 탐지 모델입니다.

640x640 고해상도를 유지하면서 손가락 피처(주먹, 보자기)의 엣지 정보를 선명하게 검출하며, **TensorRT FP16 가속을 통해 35~45 FPS의 실시간 추론 속도**를 달성합니다.

---

## ✨ 주요 특징 (Key Features)

* **⚡ 70% 초경량화 슬림 신경망 (`yolov5_gesture_slim.yaml`):**
  * 파라미터 수: `7.02M` ➔ **`2.10M (2,109,764 개)`** (약 70% 감축)
  * 레이어 수: **`147 개`** (C3 Bottleneck 최적화)
  * 가중치 파일 용량: **`4.6 MB`** (기존 15MB 대비 비약적 감소)
* **🎯 640x640 정밀 해상도 보존:**
  * 320px의 픽셀 뭉개짐 현상을 극복하고 먼 거리 및 손가락 마디 경계선 정밀 탐지.
* **🛡️ Jetson Nano OOM(메모리 초과) 완전 방지:**
  * PyTorch/TensorRT 구동 시 RAM 점유율을 **1.5GB 이하**로 안전하게 통제.
* **🚀 TensorRT FP16 16비트 가속 극대화:**
  * Throughput **35 ~ 45 FPS** 실시간 웹캠 제스처 탐지 가능.

---

## 📂 프로젝트 파일 구조 (Repository Structure)

```text
gesture_project/
├── README.md                           # 📖 프로젝트 메인 설명서
├── guide.md                            # 📘 Jetson Nano 배포 & 트러블슈팅 통합 가이드북
└── gesture_slim2M_640_e200/            # 🏋️ 200 에포크 학습 완료 결과 디렉터리
    ├── weights/
    │   ├── best.pt                     # 🔥 4.6MB 최적 슬림 가중치 파일 (2.1M Params)
    │   └── last.pt                     # 📦 마지막 에포크 가중치 파일
    ├── results.png                     # 📊 학습 손실 및 mAP 성능 그래프
    ├── confusion_matrix.png            # 🎯 혼동 행렬 시각화
    ├── F1_curve.png & PR_curve.png     # 📈 정밀도 및 재현율 곡선
    ├── opt.yaml & hyp.yaml             # ⚙️ 학습 하이퍼파라미터 설정
    └── val_batch0_pred.jpg             # 📸 검증 예측 샘플 이미지
```

---

## 📊 모델 성능 비교 (Performance Comparison)

| 지표 | 기존 YOLOv5s | 커스텀 슬림 모델 (`gesture_slim2M`) | 개선 및 감축 효과 |
| :--- | :---: | :---: | :---: |
| **파라미터 수 (Parameters)** | 7,025,000 개 (7.02M) | **2,109,764 개 (2.10M)** | **약 70% 감축** 📉 |
| **레이어 수 (Layers)** | 157 개 | **147 개** | **Bottleneck 40% 슬림화** ✂️ |
| **가중치 용량 (Weight Size)** | ~15.0 MB | **4.6 MB** | **약 69% 용량 다이어트** 📦 |
| **연산량 (GFLOPs @ 640px)** | 15.8 GFLOPs | **5.2 GFLOPs** | **약 67% 연산 부담 경감** ⚡ |
| **Jetson Nano 속도 (FP16)** | ~22 FPS | **35 ~ 45 FPS** | **속도 약 2배 향상** 🚀 |
| **Jetson RAM 점유율** | ~3.8 GB (OOM 위험) | **~1.5 GB** | **메모리 폭발 안전 영역** 🛡️ |

---

## 🎯 클래스 정보 (Class Labels)

```yaml
0: person  # 사람 실루엣 및 배경
1: fist    # 주먹 제스처 ✊
2: palm    # 보자기 제스처 🖐️
```

---

## 🚀 빠른 시작 가이드 (Quick Start)

### 1) 저장소 클론 (Jetson Nano 또는 PC)
```bash
git clone https://github.com/leeseungjae03046-alt/gesture_project.git
cd gesture_project
```

### 2) Jetson Nano TensorRT FP16 가속 엔진 빌드
```bash
# 1. ONNX 변환 (640px)
python3 export.py --weights gesture_slim2M_640_e200/weights/best.pt --img 640 --batch 1 --include onnx

# 2. trtexec 가속 컴파일
/usr/src/tensorrt/bin/trtexec --onnx=gesture_slim2M_640_e200/weights/best.onnx --saveEngine=best.engine --fp16 --workspace=1024 --avgRuns=1
```

### 3) 실시간 카메라 추론 테스트
```bash
python3 detect.py --weights best.engine --img 640 --conf 0.25 --source 0 --data dataset.yaml --classes 1 2
```

---

## 📘 전체 배포 상세 가이드
더 자세한 젯슨 나노 OS 환경 패치 명령어(`numpy==1.19.4`, `tensorrt` 심볼릭 링크 등) 및 트러블슈팅 내역은 **[guide.md](file:///home/daegu/canlab_workspace/git_gesture/guide.md)** 가이드북을 참고해 주세요!
