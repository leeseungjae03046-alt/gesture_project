# Jetson Nano YOLOv5 제스처 탐지 슬림 모델 재학습 및 전송 통합 가이드

본 문서는 **Windows PC에서 원격 Linux 서버로의 파일 전송 방법**, **YOLOv5 슬림 신경망 설계 및 직접 수정 방법**, **Linux 환경에서의 재학습 진행 절차**, **데이터셋 및 환경 트러블슈팅**, 그리고 **Jetson Nano 배포 및 TensorRT 가속화 전체 파이프라인**을 지속적으로 기록·관리하는 프로젝트 가이드북입니다.

---

## 1. 💻 Windows PC ➔ Linux 원격 서버 파일 전송 (`scp`)

SSH Key(.pem)와 전용 포트를 사용하여 Windows PC에서 Linux 서버로 디렉터리 전체를 전송하는 명령어입니다.

### 📌 Windows CMD / PowerShell 실행 명령어
```cmd
scp -P 30001 -i "C:\키파일경로\키이름.pem" -r "C:\보낼폴더경로\gesture_project_dataset" daegu@10.45.42.130:/home/daegu/canlab_workspace/
```

* **`-P 30001`**: 대문자 P. 원격 서버 SSH 포트 번호
* **`-i "키경로"`**: 소문자 i. `.pem` 키 파일 경로
* **`-r`**: 폴더(디렉터리) 전체 전송
* **`daegu@10.45.42.130`**: 서버 계정 ID 및 IP 주소
* **`:/home/daegu/canlab_workspace/`**: 원격 서버 내 저장 경로

---

## 2. ⚙️ YOLOv5 슬림 신경망 파일 직접 수정 방법

파라미터 수를 702만 개에서 **약 210만 개(약 70% 감축)**로 줄여 640px 해상도에서도 메모리 폭발 없이 고속·고정밀 추론이 가능하도록 설정 파일을 수정했습니다.

### 1) 수정할 파일 위치
`yolov5` 디렉터리 내부 `models` 폴더의 커스텀 설정 파일(`yolov5_gesture_slim.yaml`)

* **파일 경로:** [yolov5_gesture_slim.yaml](file:///home/daegu/canlab_workspace/gesture_project_dataset/yolov5/models/yolov5_gesture_slim.yaml)

### 2) 파일 수정 내용 (yaml 설정 값)
```yaml
# YOLOv5 Gesture Slim Model Configuration for 3-Classes (~2.10M Params)

# 1. 클래스 개수 설정 (0: person, 1: fist, 2: palm)
nc: 3

# 2. 신경망 깊이 및 채널 폭 슬림화 (147개 레이어 / 2,109,764 파라미터 / 5.2 GFLOPs)
depth_multiple: 0.20  # 기존 0.33 -> 0.20 (C3 레이어 깊이 축소)
width_multiple: 0.27  # 기존 0.50 -> 0.27 (채널 폭 조정으로 ~2.10M 파라미터 완성)

# 3. 앵커 박스 설정 (기존 COCO 앵커 유지)
anchors:
  - [10,13, 16,30, 33,23]  # P3/8
  - [30,61, 62,45, 59,119]  # P4/16
  - [116,90, 156,198, 373,326]  # P5/32

# YOLOv5 backbone & head 구조 정의
backbone:
  # [from, number, module, args]
  [[-1, 1, Conv, [64, 6, 2, 2]],  # 0-P1/2
   [-1, 1, Conv, [128, 3, 2]],     # 1-P2/4
   [-1, 3, C3, [128]],
   [-1, 1, Conv, [256, 3, 2]],     # 3-P3/8
   [-1, 6, C3, [256]],
   [-1, 1, Conv, [512, 3, 2]],     # 5-P4/16
   [-1, 9, C3, [512]],
   [-1, 1, Conv, [1024, 3, 2]],    # 7-P5/32
   [-1, 3, C3, [1024]],
   [-1, 1, SPPF, [1024, 5]],       # 9
  ]

head:
  [[-1, 1, Conv, [512, 1, 1]],
   [-1, 1, nn.Upsample, [None, 2, 'nearest']],
   [[-1, 6], 1, Concat, [1]],      # cat backbone P4
   [-1, 3, C3, [512, False]],      # 13

   [-1, 1, Conv, [256, 1, 1]],
   [-1, 1, nn.Upsample, [None, 2, 'nearest']],
   [[-1, 4], 1, Concat, [1]],      # cat backbone P3
   [-1, 3, C3, [256, False]],      # 17 (P3/8-small)

   [-1, 1, Conv, [256, 3, 2]],
   [[-1, 14], 1, Concat, [1]],     # cat head P4
   [-1, 3, C3, [512, False]],      # 20 (P4/16-medium)

   [-1, 1, Conv, [512, 3, 2]],
   [[-1, 10], 1, Concat, [1]],     # cat head P5
   [-1, 3, C3, [1024, False]],     # 23 (P5/32-large)

   [[17, 20, 23], 1, Detect, [nc, anchors]],  # Detect(P3, P4, P5)
  ]
```

---

## 3. 🐧 Linux 환경에서 YOLOv5 재학습 실행 결과

### 1단계: 가상환경 위치 확인 및 활성화
서버에 구축된 전용 가상환경 경로: `/home/daegu/canlab_workspace/.venv`

```bash
# 1. yolov5 디렉터리로 이동
cd /home/daegu/canlab_workspace/gesture_project_dataset/yolov5

# 2. 가상환경 활성화
source /home/daegu/canlab_workspace/.venv/bin/activate
```

### 2단계: 640px 해상도 ~2.10M 슬림 모델 재학습 기동 및 완료
```bash
python train.py \
  --img 640 \
  --batch 16 \
  --epochs 200 \
  --data ../PC에_옮길_자료/dataset.yaml \
  --cfg models/yolov5_gesture_slim.yaml \
  --weights yolov5n.pt \
  --name gesture_slim2M_640_e200
```

#### 📊 학습 완료 수치 및 파일 위치 (200 에포크 완료)
* **소요 시간:** 약 26분 (0.445 시간)
* **레이어 수:** **147개** (Fused 레이어 기준)
* **파라미터 수:** **2,109,764 개 (약 210만 개)** (파일 용량: 4.6MB)
* **연산량 (GFLOPs):** **5.2 GFLOPs**
* **최적 가중치 파일 저장 경로 (`best.pt`):**
  `/home/daegu/canlab_workspace/gesture_project_dataset/yolov5/runs/train/gesture_slim2M_640_e200/weights/best.pt`

---

## 4. 🛠️ 트러블슈팅 가이드 및 주의사항

1. **데이터셋 경로 에러 (`Dataset not found`)**
   * **원인:** `dataset.yaml` 파일 내 `path:` 속성이 예전 계정(`/home/mijung/...`)으로 고정되어 발생.
   * **해결:** `dataset.yaml` 파일의 `path:` 속성을 **`path: ../dataset` (상대 경로)**로 변경하여 해결.

2. **가중치 파일 에러 (`yolov5.pt not found`)**
   * **원인:** 존재하지 않는 파일명 `yolov5.pt`를 입력하면 깃허브에서 새로 다운로드를 시도하다 에러 발생.
   * **해결:** 서버 내에 이미 존재하는 **`yolov5n.pt`**를 `--weights yolov5n.pt`로 지정하여 해결.

3. **`RuntimeError: operator torchvision::nms does not exist`**
   * **원인:** C++ 연산자 불일치 패키지 에러.
   * **해결:** `.venv` 가상환경 내에 호환되는 `torch 2.13` 및 `torchvision 0.28` CUDA 가속 패키지 재설치로 해결.

---

## 5. 🤖 Jetson Nano 이식 및 배포 상세 절차 (단계별 가이드)

학습 완료된 최적 가중치(`best.pt`, 4.6MB)를 Jetson Nano로 옮긴 후 실시간 가속 엔진을 구동하는 **단계별 상세 가이드**입니다.

### 1단계: Windows PC ➔ Jetson Nano 파일 전송 (`scp`)
내 PC 바탕화면에 다운로드받은 `best.pt` 및 `guide.md` 파일 또는 폴더를 Jetson Nano로 전송합니다.

```cmd
# Windows CMD에서 실행
scp -i "C:\키경로\jetson_key.pem" "C:\Users\User\Desktop\best.pt" mijung@젯슨IP:/home/mijung/canlab/gesture_project/models/
```

---

### 2단계: Jetson Nano 사전 환경 세팅 및 패치 (최초 1회 필수)

Jetson Nano(Python 3.6 / JetPack) 특유의 오류를 방지하기 위한 패치 명령 모음입니다.

1. **가상환경 활성화 및 TensorRT 모듈 연결:**
   ```bash
   source /home/mijung/canlab/.venv/bin/activate
   ln -sf /usr/lib/python3.6/dist-packages/tensorrt* /home/mijung/canlab/.venv/lib/python3.6/site-packages/
   ```

2. **Numpy 다운그레이드 패치 (CPU Crash `Illegal instruction` 방지):**
   ```bash
   pip install --force-reinstall numpy==1.19.4
   ```

3. **ONNX 변환 패키지 설치:**
   ```bash
   sudo apt-get install -y protobuf-compiler libprotoc-dev
   pip install onnx==1.8.0
   ```

---

### 3단계: ONNX 모델 변환 (640px 1대1 매칭)

Jetson Nano 가상환경 활성화 상태에서 `yolov5` 디렉터리로 이동 후 변환 스크립트를 기동합니다.

```bash
cd /home/mijung/canlab/gesture_project/yolov5

python3 export.py \
  --weights ../models/best.pt \
  --img 640 \
  --batch 1 \
  --include onnx
```
* **결과물:** `../models/best.onnx` 파일 생성 완료.

---

### 4단계: `trtexec`를 이용한 TensorRT FP16 가속 엔진 컴파일

Jetson Nano 전용 GPU 하드웨어 가속기(`.engine`)를 컴파일합니다. (약 10~15분 소요)

```bash
/usr/src/tensorrt/bin/trtexec \
  --onnx=../models/best.onnx \
  --saveEngine=../models/best.engine \
  --fp16 \
  --workspace=1024 \
  --avgRuns=1
```

* **`--fp16`**: 16비트 반정밀도 가속으로 35~45 FPS 고속 프레임 달성.
* **`--workspace=1024`**: 4GB RAM 한도 내에서 메모리 폭발(OOM) 방지.

---

### 5단계: 실시간 비디오/카메라 추론 테스트

가속 엔진(`best.engine`)을 사용하여 실시간 카메라 제스처 탐지를 기동합니다.

```bash
python3 detect.py \
  --weights ../models/best.engine \
  --img 640 \
  --conf 0.25 \
  --source 0 \
  --data ../dataset.yaml \
  --classes 1 2
```

#### ⚠️ 주요 옵션 주의사항:
* **`--data ../dataset.yaml`**: 반드시 지정해야 0번(사람)을 빼고 1번(`fist`, 주먹)과 2번(`palm`, 보자기) 라벨이 정상 번역되어 표기됩니다.
* **`--classes 1 2`**: 주먹과 보자기 제스처만 집중 탐지하도록 필터링.

---

## 📝 요약 체크리스트
- [x] Windows ➔ 서버 `scp` 전송 명령어 포트(`-P 30001`) 및 키(`-i`) 세팅 완료
- [x] `yolov5_gesture_slim.yaml` 설정 적용 (**2,109,764 파라미터 / 147개 레이어**)
- [x] 2.10M 파라미터 슬림 모델 200 에포크 재학습 완수 (`gesture_slim2M_640_e200`)
- [x] 최적 가중치 `best.pt` (4.6MB) 생성 완료 및 경로 정리 완료
- [x] **Jetson Nano 이식 후 세팅, ONNX 변환, TensorRT FP16 컴파일, 카메라 추론 명령어 단계별 가이드 수록 완료**
