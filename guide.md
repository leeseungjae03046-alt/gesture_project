# 📘 Jetson Nano YOLOv5 슬림 제스처 모델 통합 작업 & 배포 가이드북

> **최종 수정일:** 2026년 7월 22일  
> **대상 장비:** Windows PC ➔ Linux 학습 서버 ➔ Jetson Nano (4GB RAM)

---

## 1. 📌 프로젝트 개요 및 커스텀 슬림 모델 스펙

본 프로젝트는 Jetson Nano 4GB RAM의 메모리 초과(OOM) 현상을 방지하면서, 실시간(40~50 FPS) 제스처 탐지를 구현하기 위해 개발된 초경량 커스텀 신경망 프로젝트입니다.

### 📊 최종 완성 모델 스펙 (`gesture_slim177M_perfect_full`)
* **신경망 구조:** `yolov5_gesture_slim.yaml` (`width_multiple: 0.25`, `depth_multiple: 0.33`)
* **사전 학습 뇌 계승:** 공식 `yolov5n.pt` 가중치 **100% 완전 계승**
* **파라미터 수:** **`1,763,224 개` (1.76M)** (기존 7.02M 대비 **75% 감축**)
* **가중치 파일 용량:** **`3.9 MB`** (`best.pt`)
* **Jetson Nano RAM 점유율:** **`1.2 GB 이하`** (OOM 위험 0%)
* **검증 탐지 성과:**
  * **주먹(`fist`) mAP50:** **`97.6%`** (Recall 100% 탐지)
  * **보자기(`palm`) mAP50:** **`99.1%`** (Precision 99.3%)

---

## 2. 📡 Remote Server ➔ Windows PC 파일 전송 (`scp`)

### 📥 1) Windows CMD에서 서버 파일 가져오기
Windows 터미널(CMD)에서 아래 명령어를 실행하여 최적 가중치(`best.pt`) 및 가이드북을 내 PC로 전송합니다.

```cmd
:: 1. 최적 가중치 파일 (3.9 MB) 다운로드
scp -P 30001 -i "C:\키경로\키이름.pem" daegu@10.45.42.130:/home/daegu/canlab_workspace/git_gesture/weights/best.pt "C:\Users\User\Desktop\"

:: 2. 통합 가이드북 다운로드
scp -P 30001 -i "C:\키경로\키이름.pem" daegu@10.45.42.130:/home/daegu/canlab_workspace/guide.md "C:\Users\User\Desktop\"
```

---

## 3. 🐍 Linux 학습 서버 재학습 명령어

데이터셋 1,728장 전체가 복원된 환경에서 1.76M 파라미터 사전 학습 모델을 재학습시키는 세팅입니다.

```bash
cd /home/daegu/canlab_workspace/yolov5
source /home/daegu/canlab_workspace/.venv/bin/activate

python train.py \
  --img 640 \
  --batch 16 \
  --epochs 150 \
  --data ../dataset.yaml \
  --cfg models/yolov5_gesture_slim.yaml \
  --weights yolov5n.pt \
  --name gesture_slim177M_perfect_full
```

---

## 4. 🛠️ 파이토치 / 토치비전 & 데이터셋 트러블슈팅 내역

### 🚨 트러블슈팅 1: `RuntimeError: operator torchvision::nms does not exist`
* **원인:** PyTorch와 Torchvision 간의 CUDA C++ 바이너리 버전 불일치.
* **해결:** CUDA 13.0 지원 무결성 파이토치 재설치 (`torch-2.13.0+cu130`, `torchvision-0.28.0+cu130`).

### 🚨 트러블슈팅 2: 라벨 누락으로 인한 시각화 박스 미출력 현상
* **원인:** 데이터 전송 중 라벨 폴더 일부가 끊겨 80%의 이미지에 `.txt` 라벨 파일이 누락되어 배경 이미지로 오인됨.
* **해결:** PC에서 1,728개 train / 261개 val 라벨 전체를 `.zip` 파일로 묶어 서버 전송 후 100% 덮어쓰기 복원 (mAP50 99.1% 달성).

---

## 5. 🤖 Jetson Nano 이식 및 배포 상세 절차

### 1단계: Windows PC ➔ Jetson Nano 파일 전송
```cmd
scp -r "C:\Users\User\Desktop\best.pt" jetson@<Jetson_IP>:/home/jetson/gesture_project/
```

### 2단계: Jetson Nano 필수 사전 환경 패치 (Python 3.6가상환경)
```bash
# 1. ARM CPU Illegal Instruction 방지 (Numpy 버전 고정)
pip install numpy==1.19.4

# 2. TensorRT 파이썬 심볼릭 링크 연동
sudo ln -s /usr/include/x86_64-linux-gnu/NvInfer.h /usr/include/NvInfer.h
```

### 3단계: ONNX 모델 변환 (640px)
```bash
cd /home/jetson/gesture_project/yolov5
python3 export.py --weights best.pt --img 640 --batch 1 --include onnx
```

### 4단계: `trtexec` FP16 TensorRT 엔진 컴파일 (40~50 FPS 속도 향상)
```bash
/usr/src/tensorrt/bin/trtexec \
  --onnx=best.onnx \
  --saveEngine=best.engine \
  --fp16 \
  --workspace=1024 \
  --avgRuns=1
```

### 5단계: 실시간 카메라 제스처 탐지 구동
```bash
python3 detect.py \
  --weights best.engine \
  --img 640 \
  --conf 0.25 \
  --source 0 \
  --data dataset.yaml \
  --classes 1 2
```

---

## 6. 🌐 GitHub 레포지토리 관리 명령어

```bash
cd /home/daegu/canlab_workspace/git_gesture

git add .
git commit -m "Feat: Final 1.76M slim gesture model (best.pt 3.9MB, mAP 99.1%)"
git push -u origin main
```
