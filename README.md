# 🖐️ YOLOv5 Custom 6-Class Gesture & Person Detection (Jetson Nano Edge AI)

> **Jetson Nano 엣지 디바이스 및 초고속 실시간 탐지를 위한 해상도별(640x480 / 416x312 / 320x240) YOLOv5 75% 초경량 커스텀 모델 프로젝트**

---

## 📌 프로젝트 개요 (Overview)

본 프로젝트는 표준 YOLOv5s 모델(702만 파라미터)을 **Jetson Nano 4GB RAM 및 엣지 환경**에 최적화하여 **1.76M 파라미터(75% 감축, 3.9MB)**로 다이어트 설계한 6-클래스 커스텀 객체 탐지 모델 프로젝트입니다.

2,400장 고품질 무결 데이터셋으로 학습되었으며, 다양한 엣지 환경 요구사항에 맞추어 **640x480(고정밀), 416x312(균형형), 320x240(초고속)** 3가지 해상도 가중치를 제공합니다.

---

## ✨ 주요 특징 (Key Features)

* **⚡ 75% 초경량화 사전 학습 계승 모델 (`yolov5_gesture_slim.yaml`):**
  * 파라미터 수: `7.02M` ➔ **`1.76M (1,763,224 개)`** (약 75% 감축)
  * 가중치 파일 용량: **`3.9 MB`** (`best.pt`)
* **📹 해상도별 맞춤 가중치 제공 (직사각형 `--rect` 4:3 비율 최적화):**
  1. **`weights_170_480x680_newdata/` (640x480):** mAP50 **96.0%**, 최고 정밀도 (~45 FPS)
  2. **`weights_170_416x312_fast/` (416x312):** mAP50 **95.2%**, 연산량 58% 감축 (~75 FPS)
  3. **`weights_170_320x240_ultrafast/` (320x240):** mAP50 **93.5%**, 연산량 75% 감축 (~100+ FPS)
* **🎯 6개 클래스 한 프레임 동시 정밀 탐지:**
  * 사람(`person`) 및 5가지 손 제스처(`fist`, `like`, `no_gesture`, `ok`, `palm`) 동시 탐지.
* **🛡️ Jetson Nano OOM(메모리 초과) 완전 차단:**
  * RAM 점유율을 **1.0GB ~ 1.1GB**로 제어하여 메모리 폭발 완전 방지.

---

## 📊 해상도별 성능 및 연산량 비교 (Resolution Comparison)

| 구분 | 640x480 (고정밀) | 416x312 (균형형 ⭐) | 320x240 (초고속 🚀) |
| :--- | :---: | :---: | :---: |
| **가중치 디렉터리** | `weights_170_480x680_newdata/` | `weights_170_416x312_fast/` | `weights_170_320x240_ultrafast/` |
| **파라미터 수** | 1.76M (3.9MB) | 1.76M (3.9MB) | 1.76M (3.9MB) |
| **연산량 (GFLOPs)** | 4.1 GFLOPs | **1.7 GFLOPs (58%↓)** | **1.0 GFLOPs (75%↓)** |
| **mAP50 종합 정확도** | **96.0%** | **95.2%** | **93.5%** |
| **정밀도 (Precision)** | **97.8%** | **96.5%** | **94.8%** |
| **Jetson Nano FPS (FP16)** | ~45 FPS | **~75 FPS** | **~100+ FPS** |
| **권장 사용 환경** | 정밀 분석 및 정지 장면 | 일반 실시간 탐지 (추천) | 로봇/드론 초고속 반응 |

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

### 2) Jetson Nano TensorRT FP16 가속 엔진 빌드 (예: 416x312 기준)
```bash
# 1. ONNX 변환 (높이 312, 너비 416)
python3 export.py --weights weights_170_416x312_fast/best.pt --img 312 416 --batch 1 --include onnx

# 2. trtexec 가속 컴파일
/usr/src/tensorrt/bin/trtexec --onnx=weights_170_416x312_fast/best.onnx --saveEngine=best.engine --fp16 --workspace=1024 --avgRuns=1
```

### 3) 실시간 웹캠 추론 테스트
```bash
python3 detect.py --weights best.engine --img 312 416 --conf 0.25 --source 0 --data data.yaml
```

---

## 📘 상세 가이드
젯슨 나노 OS 환경 패치 및 전체 이식 절차는 **[guide.md](file:///home/daegu/canlab_workspace/git_gesture/guide.md)** 가이드북을 참고해 주세요!
