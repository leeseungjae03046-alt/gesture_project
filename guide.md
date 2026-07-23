# 📘 Jetson Nano YOLOv5 6-Class 슬림 제스처 모델 통합 작업 & 배포 가이드북

> **최종 수정일:** 2026년 7월 23일  
> **대상 장비:** Windows PC ➔ Linux 학습 서버 ➔ Jetson Nano (4GB RAM)

---

## 1. 📌 프로젝트 개요 및 해상도별 스펙

본 프로젝트는 Jetson Nano 4GB RAM의 메모리 초과(OOM) 현상을 방지하고 다양한 카메라 환경에 맞추어 **실시간(45~100+ FPS) 제스처 탐지**를 구현하기 위해 개발된 초경량 커스텀 신경망 프로젝트입니다.

### 📊 해상도별 가중치 스펙 요약
1. **`weights_170_480x680_newdata/best.pt` (640x480):** mAP50 **96.0%**, 정밀도 97.8% (45 FPS)
2. **`weights_170_416x312_fast/best.pt` (416x312 ⭐ 추천):** mAP50 **95.2%**, 연산량 58% 감축 (75 FPS)
3. **`weights_170_320x240_ultrafast/best.pt` (320x240):** mAP50 **93.5%**, 연산량 75% 감축 (100+ FPS)

---

## 2. 📡 Remote Server ➔ Windows PC 파일 전송 (`scp`)

```cmd
:: 1. 416x312 추천 가중치 파일 (3.9 MB) 다운로드
scp -P 30001 -i "C:\키경로\키이름.pem" daegu@10.45.42.130:/home/daegu/canlab_workspace/git_gesture/weights_170_416x312_fast/best.pt "C:\Users\User\Desktop\"

:: 2. 통합 가이드북 다운로드
scp -P 30001 -i "C:\키경로\키이름.pem" daegu@10.45.42.130:/home/daegu/canlab_workspace/git_gesture/guide.md "C:\Users\User\Desktop\"
```

---

## 3. 🤖 Jetson Nano 이식 및 배포 상세 절차 (416x312 예시)

### 1단계: Windows PC ➔ Jetson Nano 파일 전송
```cmd
scp -r "C:\Users\User\Desktop\best.pt" jetson@<Jetson_IP>:/home/jetson/gesture_project/
```

### 2단계: Jetson Nano 필수 사전 환경 패치 (Python 3.6 가상환경)
```bash
# 1. ARM CPU Illegal Instruction 방지 (Numpy 버전 고정)
pip install numpy==1.19.4

# 2. TensorRT 파이썬 심볼릭 링크 연동
sudo ln -s /usr/include/x86_64-linux-gnu/NvInfer.h /usr/include/NvInfer.h
```

### 3단계: ONNX 모델 변환 (높이 312, 너비 416)
```bash
cd /home/jetson/gesture_project/yolov5
python3 export.py --weights best.pt --img 312 416 --batch 1 --include onnx
```

### 4단계: `trtexec` FP16 TensorRT 엔진 컴파일 (75 FPS 속도 향상)
```bash
/usr/src/tensorrt/bin/trtexec \
  --onnx=best.onnx \
  --saveEngine=best.engine \
  --fp16 \
  --workspace=1024 \
  --avgRuns=1
```

### 5단계: 실시간 웹캠 제스처 & 사람 동시 탐지 구동
```bash
python3 detect.py \
  --weights best.engine \
  --img 312 416 \
  --conf 0.25 \
  --source 0 \
  --data data.yaml
```

---

## 4. 🌐 GitHub 레포지토리 관리 명령어

```bash
cd /home/daegu/canlab_workspace/git_gesture

git add .
git commit -m "Feat: 416x312 및 320x240 해상도 경량 모델 가중치 추가 및 가이드 최신화"
git push -u origin main
```
