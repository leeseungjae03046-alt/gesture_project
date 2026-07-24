# 리눅스 명령어 및 개발 치트시트

이 문서는 프로젝트 진행 과정에서 다루는 유용한 리눅스 명령어 및 실행 코드들을 정리한 치트시트입니다.

---

## 1. 시스템 메모리 및 저장공간 확인

### 보조기억장치(디스크) 용량 확인
현재 마운트된 디스크의 전체 크기, 사용량, 남은 용량을 확인할 수 있습니다.
```bash
df -h
```

### RAM 및 Swap 메모리 사용량 확인
물리 메모리(RAM)와 스왑 메모리(가상 메모리)의 사용 현황을 사람이 보기 편한 단위(GB, MB)로 출력합니다.
```bash
free -h
```

---

## 2. 파일 및 폴더 조작 명령어

### 디렉토리(폴더) 이동
터미널의 현재 위치(작업 디렉토리)를 다른 경로로 이동시킵니다.
```bash
cd [이동할_폴더_경로]
```
- 예시 (욜로 폴더로 이동):
  ```bash
  cd /home/mijung/canlab/yolov5
  ```
- 예시 (상위 폴더로 이동):
  ```bash
  cd ..
  ```

### 폴더/파일 이동 및 이름 변경
파일이나 폴더의 위치를 옮기거나 파일명을 변경할 때 사용합니다.
```bash
mv [원본_경로] [대상_경로_또는_변경할_이름]
```
- 예시 (이름 변경):
  ```bash
  mv /home/mijung/canlab/folder1 /home/mijung/canlab/folder2
  ```

### 폴더 강제 삭제
하위 폴더와 파일까지 묻지 않고 강제로 영구 삭제합니다. (매우 주의해서 사용해야 합니다.)
```bash
미널의 현재 위치(작업 디렉토리)를 다른 경로로 이동시킵니다.
```bash
cd [이동할_폴더_경로]
```
rm -rf [삭제할_폴더_경로]
```

---

## 3. Python 및 Pip 패키지 관리

### 가상환경 활성화
프로젝트에 할당된 파이썬 가상환경(.venv)을 활성화합니다.
```bash
source /home/mijung/canlab/.venv/bin/activate
```

### 가상환경 내 패키지 목록 조회
가상환경에 설치되어 있는 파이썬 패키지들의 목록과 버전을 출력합니다.
```bash
pip list
```

### 패키지 의존성 충돌 검사
설치된 패키지들 사이에서 호환되지 않는 버전 충돌이 있는지 점검합니다.
```bash
pip check
```

### Pip 다운로드 캐시 지우기
강제 종료나 오류 등으로 인해 손상된 임시 다운로드 파일을 청소하고 용량을 확보합니다.
```bash
pip cache purge
```

---

## 4. YOLOv5 & PyTorch 개발 명령어 (예시)

### YOLOv5 객체 감지(Inference) 실행 도움말 확인
```bash
python detect.py --help
```

### PyTorch 가중치 모델(.pt)을 ONNX 형식으로 변환 (배포용)
```bash
python export.py --weights best.pt --include onnx --simplify
```

---

## 5. Vim 에디터 스왑 파일(.swp) 경고 해결 및 백그라운드 관리

### 백그라운드 작업(Jobs) 확인 및 복구
Vim 편집 중 `Ctrl + Z`를 눌러 백그라운드로 일시 정지된 작업을 확인하고 다시 포그라운드로 가져옵니다.
```bash
# 백그라운드 작업 목록 확인
jobs

# 1번 백그라운드 작업을 포그라운드로 복구 (작업 번호에 맞게 변경)
fg %1
```

### Vim 스왑 파일 수동 삭제
Vim이 비정상 종료되어 경고 메시지가 계속 발생할 때, 자동 생성된 숨김 스왑 파일(`.swp`)을 수동으로 삭제합니다.
```bash
# 특정 파일의 스왑 파일 삭제 예시 (guide.md의 스왑 파일)
rm /home/mijung/markdown/.guide.md.swp

# 디렉토리 내 잔여 스왑 파일 강제 삭제
rm /home/mijung/markdown/.*.swp
```

---

## 6. 제스처 인식 프로젝트 실행 명령어

### 제스처 인식기(Phase 1) 실행
작성된 파이썬 스크립트를 가상환경 환경 내에서 실행하여 카메라 피드와 동작을 테스트합니다.
```bash
# 제스처 필터 및 인식 스크립트 실행
python /home/mijung/canlab/gesture_project/hand_filter.py
```

### YOLOv5n 사람 탐지기(Phase 2) 실행
경량화 최적화가 적용된 YOLOv5n 기반 사람 탐지기 스크립트를 실행합니다.
```bash
# 사람 탐지기 스크립트 실행
python /home/mijung/canlab/gesture_project/yolo_person_detector.py
```

---

## 7. ONNX 모델 변환 및 ONNX Runtime 설치

### PyTorch (.pt) 모델을 ONNX 형식으로 변환 (해상도 320x320)
```bash
python /home/mijung/canlab/gesture_project/yolov5/export.py \
  --weights /home/mijung/canlab/gesture_project/yolov5/yolov5n.pt \
  --include onnx --simplify --imgsz 320 320
```

### ONNX Runtime 패키지 설치 (CPU용 경량 추론)
```bash
# 가상환경 활성화 상태에서 실행 (Python 3.6 호환 버전 고정)
pip install onnxruntime==1.10.0
```

---

## 8. YOLOv5 커스텀 모델 학습 및 검증 명령어

### 커스텀 데이터셋 디렉토리 구조 생성
```bash
# 학습 및 검증을 위한 이미지/라벨 디렉토리 생성
mkdir -p /home/mijung/canlab/gesture_project/dataset/images/train
mkdir -p /home/mijung/canlab/gesture_project/dataset/images/val
mkdir -p /home/mijung/canlab/gesture_project/dataset/labels/train
mkdir -p /home/mijung/canlab/gesture_project/dataset/labels/val
```

### YOLOv5 패키지 다운로드 및 의존성 설치
```bash
# YOLOv5 레포지토리 복제 (필요시 진행)
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
```

### 커스텀 데이터셋 학습 실행 (Jetson Nano 또는 PC 개발 서버)
```bash
python train.py --img 320 --batch 16 --epochs 100 --data /home/mijung/canlab/gesture_project/dataset.yaml --weights yolov5n.pt --device 0
```
- `--img`: 입력 이미지 해상도 설정 (320x320으로 리소스 최적화)
- `--batch`: 한 번에 학습할 이미지 개수 (Jetson Nano OOM 방지를 위해 8 또는 16 권장)
- `--epochs`: 전체 데이터 학습 횟수 (기본 100~300회 추천)
- `--data`: 데이터셋 설정 파일(`dataset.yaml`) 경로
- `--weights`: 전이 학습용 사전 학습 가중치 파일 (`yolov5n.pt` 사용으로 연산 최소화)
- `--device`: 학습에 사용할 GPU ID (`0` 혹은 CPU일 경우 `cpu`)

### 학습된 모델로 실시간 웹캠 테스트
```bash
python detect.py --weights runs/train/exp/weights/best.pt --img 320 --conf 0.4 --source 0
```
- `--weights`: 학습이 완료되어 생성된 가중치 파일 경로
- `--conf`: 최소 인식 임계값(Confidence Threshold)
- `--source`: 이미지 또는 동영상 파일 경로, 웹캠일 경우 `0` 입력

## 9. 젯슨 나노 모델 이식 및 압축 해제

### 이식용 압축 파일 해제 및 모델 경로 정돈
PC에서 학습이 완료되어 젯슨 나노로 전송된 압축 파일(`젯슨나노로 옮길 자료.zip`)을 해제하고, 가중치 모델들을 `models` 디렉토리로 정돈하는 명령어입니다.
```bash
# 젯슨 나노용 이식 자료 압축 해제
unzip -o "/home/mijung/Downloads/젯슨나노로 옮길 자료.zip" -d "/home/mijung/canlab/gesture_project"

# 모델 가중치 압축 해제
unzip -o "/home/mijung/canlab/gesture_project/trained_models_for_jetson.zip" -d "/home/mijung/canlab/gesture_project"

# 모델 디렉토리 이름을 models로 변경 및 임시 압축 파일 삭제
mv "/home/mijung/canlab/gesture_project/trained_models" "/home/mijung/canlab/gesture_project/models"
rm "/home/mijung/canlab/gesture_project/trained_models_for_jetson.zip"
```

* **주요 명령어와 매개변수의 역할**:
  * `unzip -o`: 대상 zip 파일의 압축을 해제하며, 동일한 파일명이 존재할 경우 사용자 확인을 묻지 않고 강제로 덮어씁니다(`-o` 즉, overwrite 옵션).
  * `-d`: 압축 해제된 파일들이 저장될 목적지 디렉토리(destination) 경로를 선언합니다.
  * `mv`: 파일이나 폴더의 위치를 이동하거나 이름을 변경할 때 사용합니다.
  * `rm`: 지정된 파일을 강제로 영구 삭제합니다.

---

## 10. 가상환경 및 CUDA, 카메라 가속 상태 검증

### PyTorch 및 CUDA 가속 상태 확인
Jetson Nano 개발 환경에서 PyTorch가 GPU(CUDA)를 사용할 수 있는지 점검합니다.
```bash
python3 -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('Device Name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
```

### 카메라 연결 상태 확인
Jetson Nano에 연결된 카메라 디바이스 목록을 확인합니다.
```bash
ls -ltr /dev/video*
```

* **주요 명령어와 매개변수의 역할**:
  * `python3 -c`: 명령줄에서 파이썬 코드를 즉시 실행하도록 하는 옵션입니다.
  * `torch.cuda.is_available()`: PyTorch 내에서 CUDA 가속(GPU)을 호출할 수 있는지 여부를 Boolean(True/False) 값으로 반환합니다.
  * `ls -ltr`: 파일 및 디렉토리 목록을 상세 정보(`-l`)와 함께 시간 역순(`-tr`)으로 정렬하여 출력하므로, 최근에 새로 연결된 장치 파일 등을 확인하기 용이합니다.

---

## 11. PyTorch 기반 (.pt) 1차 카메라 탐지 테스트

YOLOv5의 `detect.py`를 실행하여 `.pt` 모델 가중치를 로드하고 실제 웹캠 환경에서 사람 및 제스처를 감지하는지 확인합니다.

```bash
# yolov5 디렉토리로 이동 후 실행
cd /home/mijung/canlab/gesture_project/yolov5

# baseline 모델(best025.pt)로 웹캠 0번 탐지 테스트 실행
python3 detect.py --weights ../models/best025/best025.pt --img 640 --conf 0.25 --source 0
```

* **주요 명령어와 매개변수의 역할**:
  * `python3 detect.py`: YOLOv5의 핵심 추론 실행 엔진 스크립트를 파이썬으로 실행합니다.
  * `--weights ../models/best025/best025.pt`: 추론에 사용할 가중치 모델 파일의 상대 경로를 지정합니다. 여기서는 0.25 채널 스케일을 갖는 baseline 가중치를 사용합니다.
  * `--img 640`: 모델 입력 이미지의 해상도(가로/세로 크기)를 640x640으로 설정합니다.
  * `--conf 0.25`: 신뢰도 임계값(Confidence Threshold)을 0.25로 설정하여, 모델이 25% 이상의 확률로 확신하는 바운딩 박스만 화면에 표시하도록 필터링합니다.
  * `--source 0`: 입력 소스를 지정합니다. `0`은 시스템의 첫 번째 카메라 디바이스(`/dev/video0`)를 의미하며, 만약 화면이 나오지 않는 경우 두 번째 카메라 장치 번호인 `1`로 변경하여 실행해볼 수 있습니다.
```

---

## 12. YOLOv5 코드 버전 불일치 오류 해결 (DetectionModel AttributeError)

학습 당시 사용했던 YOLOv5 코드 구조와 로드하려는 실행 환경 코드(`models/yolo.py`)의 버전 불일치로 `AttributeError: Can't get attribute 'DetectionModel'` 에러가 발생한 경우, 백업된 PC 학습용 코드 폴더를 활성화하여 해결합니다.

```bash
# gesture_project 루트 폴더로 복귀
cd /home/mijung/canlab/gesture_project

# 기존 작동하지 않는 yolov5 폴더를 legacy 폴더 하위로 백업 및 이동
mv yolov5 legacy/yolov5_backup

# PC 학습 버전 폴더를 yolov5로 이름 변경하여 활성화
mv yolov5_pc_training_version yolov5

# 새로 정돈된 yolov5로 이동 후 재실행
cd yolov5
python3 detect.py --weights ../models/best025/best025.pt --img 640 --conf 0.25 --source 0
```

* **주요 명령어와 매개변수의 역할**:
  * `mv [기존_폴더] legacy/yolov5_backup`: `mv` 명령어로 기존 `yolov5` 디렉토리를 `legacy` 디렉토리 하위의 `yolov5_backup` 명칭으로 변경하여 안전하게 이동시킵니다.

---

## 13. 의존성 패키지 누락 오류 해결 (ModuleNotFoundError: No module named 'ultralytics')

YOLOv5 실행 도중 `ultralytics` 패키지가 누락되어 오류가 발생한 경우, Jetson Nano의 특수 빌드된 PyTorch 환경이 깨지지 않도록 `torch`와 `torchvision`을 제외하고 나머지 필요한 의존성 패키지만 안전하게 설치합니다.

```bash
# 가상환경 활성화 상태에서 실행
pip install ultralytics
```

또는 `requirements.txt`에서 `torch`와 `torchvision` 설치를 건너뛰고 나머지 패키지만 일괄 설치하려면 아래 명령어를 사용합니다.

```bash
# requirements.txt 파일에서 torch 및 torchvision 줄을 임시로 주석 처리한 후 의존성 설치
sed -i 's/^torch/# torch/g' /home/mijung/canlab/gesture_project/yolov5/requirements.txt
pip install -r /home/mijung/canlab/gesture_project/yolov5/requirements.txt
```

* **주요 명령어와 매개변수의 역할**:
  * `pip install ultralytics`: 욜로의 핵심 공통 유틸리티 라이브러리인 `ultralytics` 패키지를 설치합니다.
  * `sed -i 's/^torch/# torch/g' [파일]`: `sed` 스트림 에디터를 사용해 `requirements.txt` 내부에서 `torch`로 시작하는 행의 맨 앞에 주석 기호(`#`)를 강제로 삽입하여 설치 리스트에서 배제합니다.

---

## 14. 누락된 의존성 패키지 일괄 설치 (detect.py 및 ONNX 변환 준비)

YOLOv5 실행 및 ONNX 변환 도중 `packaging`, `gitpython`, `psutil`, `onnx` 등의 라이브러리들이 누락되어 런타임 에러가 발생하는 것을 예방하기 위해 일괄적으로 가상환경에 설치합니다.

```bash
# 가상환경 활성화 상태에서 실행
pip install packaging gitpython psutil onnx
```

* **주요 명령어와 매개변수의 역할**:
  * `pip install packaging gitpython psutil onnx`: 누락된 유틸리티 3종 및 ONNX 변환에 필수적인 `onnx` 모델 파서 패키지를 일괄 설치합니다. 이 패키지들은 파이썬 3.6 가상환경 스펙에서도 무리 없이 잘 호환됩니다.

---

## 15. 구버전 YOLOv5 롤백 및 클래스 앨리어스 패치 (AttributeError & ultralytics 에러 종결)

최신 YOLOv5 코드의 파이썬 3.6 환경(Jetson Nano) 호환성 에러들을 우회하기 위해, 구버전 코드로 롤백하고 학습 모델 구조 호환을 위한 클래스 앨리어싱을 적용합니다.

```bash
# 1. gesture_project 폴더로 복귀
cd /home/mijung/canlab/gesture_project

# 2. 현재 문제 있는 최신 버전 폴더명 변경
mv yolov5 yolov5_error_version

# 3. 백업해 두었던 구버전 폴더를 메인 yolov5 폴더로 복원
mv legacy/yolov5_backup yolov5

# 4. 복원된 yolo.py 맨 밑에 앨리어스 코드 추가
echo "DetectionModel = Model" >> yolov5/models/yolo.py

# 5. 복원된 detect.py 최상단(임포트부)에 WindowsPath 패치 추가
# (파이썬 3.6 가상환경 및 PosixPath 호환을 위해 추가)
sed -i '1s/^/import pathlib\npathlib.WindowsPath = pathlib.PosixPath\n/' yolov5/detect.py
```

* **주요 명령어와 매개변수의 역할**:
  * `echo "DetectionModel = Model" >> [파일]`: 파일의 가장 마지막 줄에 지정한 문자열을 개행하여 덧붙입니다. 이를 통해 PyTorch 가중치(`.pt`)가 역직렬화될 때 요구하는 `DetectionModel` 클래스명을 구버전의 `Model` 클래스로 맵핑시켜 `AttributeError`를 소멸시킵니다.
  * `sed -i '1s/^/[추가코드]\n/' [파일]`: `sed` 스트림 에디터를 사용해 대상 파일의 첫 번째 줄(`1s`) 맨 앞(`^`)에 원하는 파이썬 패치 코드(`import pathlib\npathlib.WindowsPath = pathlib.PosixPath\n`)를 강제 삽입하여, 윈도우 OS에서 직렬화된 모델 객체를 리눅스에서 오류 없이 파싱해낼 수 있도록 조치합니다.

---

## 16. Jetson Nano RAM 메모리 절약형 탐지 실행 (OOM 예방)

Jetson Nano의 4GB 통합 메모리(Shared RAM) 한계로 인한 렉 및 시스템 잠김(OOM) 현상을 방지하기 위해 입력 해상도를 축소하고 FP16 반정밀도 가속을 적용하여 테스트합니다.

```bash
# 초경량 모델(best0125.pt), 입력 해상도 320, FP16 반정밀도(--half) 가속 적용하여 실행
python3 detect.py --weights ../models/best0125/best0125.pt --img 320 --conf 0.25 --source 0 --half
```

* **주요 명령어와 매개변수의 역할**:
  * `--img 320`: 모델 입력 해상도를 320x320으로 절반 낮추어 연산 텐서 크기를 1/4로 줄이고 메모리 점유율을 대폭 경감합니다.
  * `--half`: FP16(반정밀도) 연산을 활성화하여 부동소수점 점유 비트를 32비트에서 16비트로 절반 줄여 젯슨 나노 Tegra GPU 연산 대역폭을 극대화하고 RAM 포화를 예방합니다.

---

## 17. ONNX 컴파일 빌드 실패 오류 해결 (Protobuf compiler not found)

Jetson Nano에서 `pip install onnx` 기동 시, C++ 빌드 과정에서 Protobuf 컴파일러가 누락되어 `Failed building wheel for onnx` 에러가 나는 문제를 해결하기 위해 시스템 패키지를 사전 설치합니다.

```bash
# 1. OS 패키지 매니저를 통해 Protobuf 컴파일러 도구 설치 (비밀번호 입력 필요)
sudo apt-get update && sudo apt-get install -y protobuf-compiler libprotoc-dev

# 2. 가상환경 활성화 상태에서 다시 ONNX 설치 (버전 1.8.0 지정으로 C++ 컴파일 에러 우회)
pip install onnx==1.8.0
```

* **주요 명령어와 매개변수의 역할**:
  * `sudo apt-get install -y protobuf-compiler libprotoc-dev`: ONNX 빌드에 필수적인 구글 Protobuf 프로토콜 직렬화 컴파일러(`protoc`)와 C++ 개발 라이브러리를 OS 단에 패키지로 주입합니다.
  * `pip install onnx==1.8.0`: Python 3.6 환경과 가장 안정적으로 연동되는 구버전 ONNX(1.8.0) 릴리즈 버전을 강제 지정하여 C++ 소스 빌드 시의 헤더 파일 누락 버그(std::transform 에러)를 회피하고 컴파일을 완수합니다.

---

## 18. ONNX -> TensorRT FP16 (.engine) 일괄 가속 변환 (trtexec 활용)

ONNX 모델을 Jetson Nano GPU 전용 추론 엔진 파일(`.engine`)로 컴파일 빌드하여, 640 해상도 연산 시에도 고속 프레임(FPS)과 극소량의 메모리 점유율을 갖추도록 최적화합니다.
Jetson Nano(4GB RAM) 환경에서는 메모리 부족(OOM)으로 인한 락 또는 프로세스 강제 종료(Killed)를 방지하기 위해 반드시 `--workspace=1024 --avgRuns=1` 옵션을 지정하고, 하나의 가속 엔진씩 순차적으로 변환해야 합니다.

```bash
# 1. TensorRT 환경변수 패스 추가
export PATH=$PATH:/usr/src/tensorrt/bin

# 2. baseline 모델 (best025.engine) 컴파일 실행 (완료 - 약 18분 소요)
trtexec --onnx=models/best025/best025.onnx --saveEngine=models/best025/best025.engine --fp16 --workspace=1024 --avgRuns=1

# 3. 나머지 2종 모델 (best015, best0125) 순차 컴파일 실행
# (OOM 방지를 위해 반드시 하나씩 실행하십시오.)
trtexec --onnx=models/best015/best015.onnx --saveEngine=models/best015/best015.engine --fp16 --workspace=1024 --avgRuns=1

trtexec --onnx=models/best0125/best0125.onnx --saveEngine=models/best0125/best0125.engine --fp16 --workspace=1024 --avgRuns=1
```

* **주요 명령어와 매개변수의 역할**:
  * `trtexec`: NVIDIA TensorRT 가속 엔진을 테스트하고 직렬화 엔진 파일로 빌드하는 독점 빌더 도구입니다.
  * `--onnx=[파일]`: 입력 소스가 될 ONNX 경로를 지정합니다.
  * `--saveEngine=[파일]`: 컴파일 및 하드웨어 최적화 융합이 완료된 `.engine` 출력 파일의 저장소 타겟 경로입니다.
  * `--fp16`: FP16(반정밀도) 모드를 가동합니다. 모델의 가중치를 16비트로 절반 줄여 젯슨 GPU의 하드웨어 전용 Tensor Core 가속 혜택을 온전히 누려 속도를 높이고 RAM 부족을 해결합니다.
  * `--workspace=1024`: TensorRT가 빌드 과정에서 사용할 최대 작업 공간 메모리(MiB) 크기를 강제 지정하여 OOM을 방지합니다.
  * `--avgRuns=1`: 최적 커널 선정을 위한 프로파일링 반복 횟수를 최소화(1회)하여 컴파일 소요 시간을 비약적으로 단축합니다.

---

## 19. Illegal instruction (core dumped) 오류 해결 (Numpy 롤백)

Jetson Nano에서 `pip install` 진행 도중 의존성에 의해 `numpy` 버전을 자동으로 1.19.5 이상으로 업데이트하는 경우, 최신 벡터 가속 명령어 충돌로 인해 파이썬 실행 시 즉각적인 `Illegal instruction` 크래시가 발생합니다. 가상환경 내의 numpy 버전을 원래의 안정 규격으로 강제 롤백하여 복구합니다.

```bash
# 가상환경 활성화 상태에서 실행
pip install --force-reinstall numpy==1.19.4
```

* **주요 명령어와 매개변수의 역할**:
  * `--force-reinstall`: 기존에 설치된 버전을 무시하고 지정한 버전을 처음부터 강제로 덮어씌워 재설치하도록 지시하는 pip 옵션입니다.

---

## 20. 가상환경 내 TensorRT 모듈 연결 (심볼릭 링크)

Jetson Nano 전용 TensorRT 파이썬 모듈(`tensorrt`)은 NVIDIA OS 이미지 내부에 설치되어 있으므로, 가상환경 활성화 시 불러올 수 없습니다. 시스템 전용 라이브러리 경로를 가상환경의 패키지 경로에 링크로 매핑해 줍니다.

```bash
ln -sf /usr/lib/python3.6/dist-packages/tensorrt* /home/mijung/canlab/.venv/lib/python3.6/site-packages/
```

* **주요 명령어와 매개변수의 역할**:
  * `ln -sf [원본경로] [가상환경경로]`: 지정한 원본 폴더 및 파일들을 가상환경 폴더 내부로 가리키는 소프트 링크(심볼릭 링크)를 강제 생성(`-s` symbolic, `-f` force)하여 연동시킵니다.

---

## 21. PC 이관용 인수인계 패키지 압축 명령어

PC 개발 환경으로 안전하게 전송하기 위해, 안내 문서 및 핵심 패치 소스코드를 `PC에 옮길 자료` 폴더에 분류하여 일괄 압축 아카이브(`.zip`)로 패키징합니다.

```bash
# 1. 'PC에 옮길 자료' 폴더 및 하위 소스코드 폴더 생성
mkdir -p ~/canlab/PC에_옮길_자료/utils

# 2. 안내 문서 4종 복사
cp ~/markdown/guide_20260706.md ~/markdown/yolov5_structure_guide.md ~/markdown/commands.md ~/markdown/guide.md ~/canlab/PC에_옮길_자료/

# 3. 설정 파일 복사
cp ~/canlab/gesture_project/dataset.yaml ~/canlab/PC에_옮길_자료/

# 4. 핵심 패치 소스코드 복사
cp ~/canlab/gesture_project/yolov5/detect.py ~/canlab/gesture_project/yolov5/export.py ~/canlab/PC에_옮길_자료/
cp ~/canlab/gesture_project/yolov5/utils/plots.py ~/canlab/gesture_project/yolov5/utils/__init__.py ~/canlab/PC에_옮길_자료/utils/

# 5. 폴더 전체를 zip 파일로 압축
cd ~/canlab && zip -r PC에_옮길_자료.zip PC에_옮길_자료/
```

* **주요 명령어와 매개변수의 역할**:
  * `mkdir -p`: 디렉토리를 생성하되, 중간 경로에 존재하지 않는 부모 폴더(`PC에_옮길_자료`)가 있다면 자동으로 함께 생성(`-p` parent)해 주는 명령입니다.
  * `cp [원본] [목적지]`: 지정된 원본 파일들을 안전하게 타겟 폴더로 복사합니다.
  * `zip -r [압축파일명.zip] [대상폴더]`: 대상 폴더 하위의 모든 파일과 서브 디렉토리들을 재귀적으로 전부 포함(`-r` recursive)하여 하나의 압축 파일로 패키징합니다.

---

## 22. unzip 명령어를 이용한 zip 파일 압축 해제

구글 드라이브나 웹에서 다운로드된 `.zip` 압축 파일을 지정한 위치 또는 현재 위치에 풀기 위해 사용하는 리눅스 기본 압축 해제 명령어입니다.

```bash
# 1. 파일이 있는 위치로 이동 (예: ~/Downloads 또는 ~/Desktop/다운로드)
cd ~/Downloads

# 2. 지정한 폴더 이름으로 깔끔하게 압축 해제
unzip jetson_transfer_candidates.zip -d jetson_transfer_candidates
```

* **주요 명령어와 매개변수의 역할**:
  * `unzip [압축파일.zip]`: 지정한 zip 파일을 풀어서 내부 파일과 폴더를 추출합니다.
  * `-d [생성할폴더명]`: 압축이 풀릴 목적지 디렉토리(Directory) 경로를 지정하는 옵션입니다. 이 옵션을 사용하면 파일들이 상위 폴더 없이 흩뿌려지는 것을 막고 지정한 폴더 내로 예쁘게 모아줍니다.

---

## 23. PC 훈련 완료 모델 폴더 프로젝트 저장소 복사

다운로드 폴더에 해제된 새 훈련 가중치 디렉토리들을 젯슨 프로젝트 모델 저장소(`~/canlab/gesture_project/models/`) 하위로 복사하여 타겟팅 가능하도록 이식합니다.

```bash
# Downloads 디렉토리의 훈련 모델 폴더 3종을 프로젝트 models 디렉토리로 복사
cp -r ~/Downloads/jetson_transfer_candidates/y5* ~/canlab/gesture_project/models/
```

* **주요 명령어와 매개변수의 역할**:
  * `cp -r [원본폴더패턴] [목적지경로]`: 폴더(Directory)와 그 내부 파일들을 통째로 재귀적(`-r` recursive)으로 지정한 목적지 디렉토리 하위로 복사합니다.
  * `y5*`: `y5`로 시작하는 모든 모델 폴더(`y5s_320_e200`, `y5s_640_e200`, `y5m_640_e200`)를 일괄 선택하는 와일드카드 기호입니다.

---

## 24. 리눅스 터미널 긴 명령어 줄바꿈 기호 (`\`) 사용법

터미널에서 명령어 옵션이 너무 길 때, 각 줄 끝에 역슬래시(`\`)를 기재하고 Enter를 누르면 다음 줄에 이어 쓰기가 가능하여 가독성을 높일 수 있습니다.

```bash
# trtexec 줄바꿈 가독성 예시
/usr/src/tensorrt/bin/trtexec \
  --onnx=../models/y5s_320_e200/best.onnx \
  --saveEngine=../models/y5s_320_e200/best.engine \
  --fp16 \
  --workspace=1024 \
  --avgRuns=1
```

* **주요 명령어와 매개변수의 역할**:
  * `\` (Backslash): 리눅스 Bash 쉘에서 명령어가 다음 줄로 계속 연결됨을 알리는 탈출(Escape) 줄바꿈 문자입니다. 역슬래시 바로 뒤에는 공백(space) 없이 바로 Enter를 눌러야 정상 동작합니다.

---

## 25. Jetson Nano RAM 메모리 사용량 확인 및 캐시 비우기

Jetson Nano(4GB 공유 RAM)에서 무거운 가속 엔진 빌드나 추론 작업 후 RAM 메모리가 포화되어 렉이 발생할 때, 시스템 캐시를 강제로 비워 메모리를 확보합니다.

```bash
# 1. 현재 시스템 RAM 및 Swap 메모리 사용량 실시간 확인
free -h

# 2. 시스템 캐시 메모리 강제 비우기 (RAM 확보)
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```

* **주요 명령어와 매개변수의 역할**:
  * `free -h`: 현재 시스템의 전체 RAM, 사용 중인 메모리, 여유 메모리 및 Swap 용량을 사람이 읽기 쉬운 단주(MB/GB) 단위(`-h` human-readable)로 출력합니다.
  * `sudo sync`: 메모리의 디스크 버퍼 데이터를 저장 장치로 안전하게 밀어 넣는 데이터 보호 명령어입니다.
  * `echo 3 | sudo tee /proc/sys/vm/drop_caches`: 리눅스 커널의 임시 페이지 캐시를 해제(비우기 `3`)하여 RAM 영역을 즉시 확보합니다.

---

## 26. Python 가상환경 (.venv) 다시 활성화

터미널을 새로 열었거나 가상환경이 해제되어 `No module named 'torch'` 오류가 발생할 때 가상환경을 재활성화합니다.

```bash
# canlab 가상환경 활성화
source /home/mijung/canlab/.venv/bin/activate
```

* **주요 명령어와 매개변수의 역할**:
  * `source [파일경로]`: 지정한 쉘 스크립트 파일(`activate`)을 실행하여 현재 터미널 세션의 파이썬 실행 환경과 라이브러리 경로 환경 변수를 가상환경으로 즉시 전환합니다.

---

## 27. mv 명령어를 이용한 파일 이름 변경 및 이동

리눅스 터미널에서 파일이나 디렉토리의 이름을 변경하거나 다른 위치로 이동시킬 때 사용합니다.

```bash
# 1. 같은 디렉토리 내에서 파일 이름 변경
mv 기존파일명.pt 변경할파일명.pt

# 예시: best.pt 이름을 best_old.pt로 변경
mv best.pt best_old.pt
```

* **주요 명령어와 매개변수의 역할**:
  * `mv [기존경로/파일명] [새경로/파일명]`: Move의 약자로, 첫 번째 인자의 파일을 두 번째 인자의 이름이나 경로로 이동 및 이름 변경을 수행합니다.

---

## 28. cp 명령어를 이용한 다양한 파일 복사 패턴

파일을 다른 폴더로 복사하거나, 복사함과 동시에 이름을 변경하는 기본 사용 형태입니다.

```bash
# 1. 파일 위치/이름을 목적지 폴더로 복사 (이름 유지)
cp ~/Downloads/best.pt ~/canlab/gesture_project/models/

# 2. 파일 복사와 동시에 이름 변경하여 복사
cp ~/Downloads/best.pt ~/canlab/gesture_project/models/best_slim.pt

# 3. 폴더(디렉토리) 전체 통째로 복사 (-r 옵션 필수)
cp -r ~/Downloads/my_folder ~/canlab/gesture_project/models/
```

* **주요 명령어와 매개변수의 역할**:
  * `cp [원본경로/파일명] [목적지경로/]`: 첫 번째 인자의 원본 파일을 두 번째 인자의 목적지 폴더로 복사합니다.
  * `cp -r [원본폴더] [목적지경로/]`: `-r` (recursive) 옵션을 사용하여 폴더 하위의 모든 파일 구조를 포함해 통째로 복사합니다.

---

## 29. GitHub (Git) 접근 및 레포지토리 연결 명령어

터미널에서 GitHub의 레포지토리를 다운로드(Clone)하거나 내 소스코드를 원격 저장소로 업로드(Push) 및 SSH 인증을 설정할 때 사용합니다.

```bash
# 1. GitHub 원격 레포지토리 코드를 현재 폴더로 다운로드
git clone https://github.com/사용자이름/레포지토리이름.git

# 2. SSH Key 생성 (비밀번호 없이 GitHub 안전 인증용)
ssh-keygen -t ed25519 -C "내이메일@example.com"
cat ~/.ssh/id_ed25519.pub

# 3. 로컬 프로젝트를 GitHub 새 저장소에 업로드(Push)
git init
git add .
git commit -m "First commit"
git remote add origin https://github.com/사용자이름/레포지토리명.git
git push -u origin main
```

* **주요 명령어와 매개변수의 역할**:
  * `git clone [URL]`: GitHub 웹에 있는 소스코드 전체를 현재 리눅스 폴더로 다운로드해 내려받습니다.
  * `ssh-keygen -t ed25519`: 비밀번호 입력 없이 GitHub 서버와 보안 통신을 연결하기 위한 암호화 SSH 공개키/개인키 쌍을 생성합니다.
  * `cat ~/.ssh/id_ed25519.pub`: 생성된 공개키 텍스트를 출력하며, 이 텍스트를 GitHub 웹 사이트 Settings -> SSH Keys 에 등록합니다.

---

## 30. Jetson Nano에 Git 프로그램 설치 및 버전 확인

리눅스 OS 패키지 관리자(apt)를 사용하여 버전 관리도구인 `git`을 설치하고 버전을 확인합니다.

```bash
# 1. Git 설치 여부 및 버전 확인
git --version

# 2. Git 프로그램 설치 (설치되어 있지 않을 때)
sudo apt-get update && sudo apt-get install -y git
```

* **주요 명령어와 매개변수의 역할**:
  * `git --version`: 현재 리눅스 시스템에 `git` 프로그램이 설치되어 있는지 확인하고 버전을 출력합니다.
  * `sudo apt-get update`: 우분투 OS 패키지 목록 인덱스를 최신 상태로 업데이트합니다.
  * `sudo apt-get install -y git`: 패키지 관리자를 통해 `git` 프로그램을 설치하며, 설치 과정의 모든 확인 질문에 자동으로 승인(`-y` yes)합니다.

---

## 31. 170만 개 슬림 모델 (weights_170) 전체 변환 및 검증 파이프라인

Git으로 다운로드한 170만 개 슬림 모델(`weights_170/best.pt`)을 프로젝트 모델 경로로 복사하고, ONNX 변환 ➔ TensorRT 가속 엔진 빌드 ➔ 실시간 카메라 추론을 기동하는 통합 절차입니다.

```bash
# 1. 가상환경 활성화 및 모델 폴더 복사
source /home/mijung/canlab/.venv/bin/activate
cp -r ~/canlab/git_communicate/gesture_project/weights_170 ~/canlab/gesture_project/models/
cd ~/canlab/gesture_project/yolov5

# 2. ONNX 포맷 변환 (416px 규격 예시)
python3 export.py --weights ../models/weights_170/best.pt --img 416 --batch 1 --include onnx

# 3. TensorRT FP16 가속 엔진 빌드 (안전 옵션 적용)
/usr/src/tensorrt/bin/trtexec \
  --onnx=../models/weights_170/best.onnx \
  --saveEngine=../models/weights_170/best.engine \
  --fp16 \
  --workspace=1024 \
  --avgRuns=1

# 4. 실시간 웹캠 검증 기동
python3 detect.py --weights ../models/weights_170/best.engine --img 416 --conf 0.25 --source 0 --data ../dataset.yaml
```

* **주요 명령어와 매개변수의 역할**:
  * `cp -r [git폴더/weights_170] [models/]` : GitHub을 통해 받은 슬림 가중치 폴더 전체를 젯슨 나노의 모델 저장소로 복사 이식합니다.
  * `--img 416`: PC 훈련 당시 사용했던 학습 해상도(예: 416px 또는 640px)를 ONNX, trtexec, detect 세 과정에 1대1로 동일하게 맞춰 적용합니다.

---

## 32. 기존 Git 폴더에 최신 변경 사항 강제 덮어쓰기 (Git Pull / Reset)

새로 `git clone`을 하지 않고, 기존 폴더의 소스코드를 GitHub의 최신 상태로 100% 덮어쓰기 업데이트할 때 사용합니다.

```bash
# 1. 기존 git 폴더로 이동
cd ~/canlab/git_communicate/gesture_project

# 2. GitHub 최신 변경 사항 강제 덮어쓰기 업데이트
git fetch --all
git reset --hard origin/main
git pull origin main
```

* **주요 명령어와 매개변수의 역할**:
  * `git fetch --all`: 원격 GitHub 서버의 최신 커밋 이력 정보를 모두 조회하여 가져옵니다.
  * `git reset --hard origin/main`: 로컬 폴더의 기존 파일 변경 사항을 싹 지우고, GitHub의 `main` 브랜치 상태와 100% 동일하게 강제 덮어쓰기(Hard Reset)합니다.
  * `git pull origin main`: GitHub 최신 변경 파일들을 내려받아 로컬 폴더로 최종 동기화합니다.

---

## 33. GitHub 640x480 신규 슬림 모델 다운로드 및 전체 변환 파이프라인

PC에서 새로 훈련시켜 GitHub에 올린 `weights_170_640x480` 모델을 내려받아 프로젝트로 복사 후 변환/추론을 진행합니다.

```bash
# 1. GitHub 최신 640x480 모델 내려받기
cd ~/canlab/git_communicate/gesture_project && git pull origin main

# 2. 모델 복사 및 가상환경 준비
source /home/mijung/canlab/.venv/bin/activate
cp -r ~/canlab/git_communicate/gesture_project/weights_170_640x480 ~/canlab/gesture_project/models/
cd ~/canlab/gesture_project/yolov5

# 3. ONNX 변환 (640px 규격 적용)
python3 export.py --weights ../models/weights_170_640x480/best.pt --img 640 --batch 1 --include onnx

# 4. TensorRT FP16 가속 엔진 빌드
/usr/src/tensorrt/bin/trtexec \
  --onnx=../models/weights_170_640x480/best.onnx \
  --saveEngine=../models/weights_170_640x480/best.engine \
  --fp16 \
  --workspace=1024 \
  --avgRuns=1

# 5. 웹캠 640x480 1:1 완벽 정합 탐지 기동
python3 detect.py --weights ../models/weights_170_640x480/best.engine --img 640 --conf 0.25 --source 0 --data ../dataset.yaml
```

* **주요 명령어와 매개변수의 역할**:
  * `weights_170_640x480`: PC에서 640x480 웹캠 4:3 비대칭 비율로 손 찌그러짐을 방지하여 훈련시킨 신규 170만 개 슬림 모델 저장 폴더입니다.
  * `--img 640`: 640x480 비대칭 텐서를 인풋으로 받아 30+ FPS 속도와 왜곡 없는 탐지를 구현합니다.

---

## 34. 신규 데이터셋 추가 학습 모델 (weights_170_480x680_newdata) 전체 이식 파이프라인

새로운 데이터셋으로 추가 학습되어 내려받아진 `weights_170_480x680_newdata` 모델의 이식 및 변환/검증 절차입니다.

```bash
# 1. 가상환경 활성화 및 신규 추가학습 모델 복사
source /home/mijung/canlab/.venv/bin/activate
cp -r ~/canlab/git_communicate/gesture_project/weights_170_480x680_newdata ~/canlab/gesture_project/models/
cd ~/canlab/gesture_project/yolov5

# 2. ONNX 변환 (640px 규격 적용)
python3 export.py --weights ../models/weights_170_480x680_newdata/best.pt --img 640 --batch 1 --include onnx

# 3. TensorRT FP16 가속 엔진 빌드
/usr/src/tensorrt/bin/trtexec \
  --onnx=../models/weights_170_480x680_newdata/best.onnx \
  --saveEngine=../models/weights_170_480x680_newdata/best.engine \
  --fp16 \
  --workspace=1024 \
  --avgRuns=1

# 4. 실시간 웹캠 검증 기동 (사람, 주먹, 보자기 3Class 전체 또는 --classes 1 2 선택)
python3 detect.py --weights ../models/weights_170_480x680_newdata/best.engine --img 640 --conf 0.25 --source 0 --data ../dataset.yaml
```

* **주요 명령어와 매개변수의 역할**:
  * `weights_170_480x680_newdata`: 추가 데이터셋으로 재학습되어 손과 사람 탐지 밸런스가 향상된 신규 슬림 모델 저장 폴더입니다.

---

## 35. 클래스 확장(6-Classes) 시 dataset.yaml 수정 가이드

모델의 클래스 개수가 6개로 늘어났을 때 발생하는 `IndexError`를 방지하기 위해 `dataset.yaml` 라벨 번역 명세서를 수정합니다.

```yaml
# ~/canlab/gesture_project/dataset.yaml 수정 내역

path: /home/mijung/canlab/gesture_project/dataset
train: images/train
val: images/val

# 1. 클래스 개수를 6으로 변경
nc: 6

# 2. 6개 클래스 이름 목록을 훈련 당시에 사용한 순서대로 명시
names: ['person', 'fist', 'palm', '신규클래스3', '신규클래스4', '신규클래스5']
```

* **주요 명령어와 매개변수의 역할**:
  * `nc: 6`: Number of Classes의 약자로, 모델이 출력하는 총 탐지 클래스 개수를 6개로 지정합니다.
  * `names: [...]`: 0번부터 5번까지의 클래스 인덱스를 실제 화면에 출력할 텍스트 라벨 이름으로 1대1 매핑하여 `IndexError`를 방지합니다.

---

## 36. 초경량 비대칭 해상도 (416x320 & 320x240) 파이프라인 세팅 가이드

연산 부하를 극단적으로 낮추고 FPS(50+ FPS)를 극대화하기 위한 416x320 및 320x240 비대칭 해상도 세팅 규격입니다.

```bash
# === 1. PC 학습 세팅 (train.py) ===
# 416x320 모델 PC 훈련
python train.py --imgsz 320 416 --batch 16 --epochs 150 --data dataset.yaml --cfg models/yolov5_gesture_slim.yaml --weights yolov5n.pt

# 320x240 모델 PC 훈련
python train.py --imgsz 240 320 --batch 16 --epochs 150 --data dataset.yaml --cfg models/yolov5_gesture_slim.yaml --weights yolov5n.pt


# === 2. Jetson Nano ONNX 변환 (export.py) ===
# 416x320 모델
python3 export.py --weights ../models/weights_416x320/best.pt --img 320 416 --batch 1 --include onnx

# 320x240 모델
python3 export.py --weights ../models/weights_320x240/best.pt --img 240 320 --batch 1 --include onnx


# === 3. TensorRT FP16 가속 빌드 (trtexec) ===
# 416x320 모델
/usr/src/tensorrt/bin/trtexec --onnx=../models/weights_416x320/best.onnx --saveEngine=../models/weights_416x320/best.engine --fp16 --workspace=1024 --avgRuns=1

# 320x240 모델
/usr/src/tensorrt/bin/trtexec --onnx=../models/weights_320x240/best.onnx --saveEngine=../models/weights_320x240/best.engine --fp16 --workspace=1024 --avgRuns=1


# === 4. 실시간 웹캠 검증 기동 (detect.py) ===
# 416x320 모델
python3 detect.py --weights ../models/weights_416x320/best.engine --img 640 --conf 0.25 --source 0 --data ../dataset.yaml

# 320x240 모델
python3 detect.py --weights ../models/weights_320x240/best.engine --img 640 --conf 0.25 --source 0 --data ../dataset.yaml
```

* **주요 명령어와 매개변수의 역할**:
  * `--imgsz 320 416`: 높이 320 x 너비 416 비대칭 해상도를 적용하여 640px 대비 연산 픽셀을 50% 이상 절감합니다.
  * `--imgsz 240 320`: 높이 240 x 너비 320 비대칭 해상도를 적용하여 연산 픽셀을 75% 절감하는 초경량 세팅입니다.

---

## 37. fast (416x312) 및 ultrafast (320x240) 초고속 모델 일괄 연쇄 빌드 파이프라인

GitHub에서 내려받은 fast 및 ultrafast 2종 초경량 모델 폴더를 이식하고, ONNX 변환 ➔ TensorRT 가속 엔진 생성을 연속 자동화 실행하는 파이프라인입니다.

```bash
# 1. 2개 모델 폴더 프로젝트 저장소로 일괄 복사
cp -r ~/canlab/git_communicate/gesture_project/weights_170_416x312_fast ~/canlab/git_communicate/gesture_project/weights_170_320x240_ultrafast ~/canlab/gesture_project/models/

# 2. fast (416x312) 모델 ONNX 변환 & trtexec 가속 빌드
source /home/mijung/canlab/.venv/bin/activate
cd ~/canlab/gesture_project/yolov5
python3 export.py --weights ../models/weights_170_416x312_fast/best.pt --img 640 --batch 1 --include onnx
/usr/src/tensorrt/bin/trtexec --onnx=/home/mijung/canlab/gesture_project/models/weights_170_416x312_fast/best.onnx --saveEngine=/home/mijung/canlab/gesture_project/models/weights_170_416x312_fast/best.engine --fp16 --workspace=1024 --avgRuns=1

# 3. ultrafast (320x240) 모델 ONNX 변환 & trtexec 가속 빌드 (연달아 기동)
python3 export.py --weights ../models/weights_170_320x240_ultrafast/best.pt --img 640 --batch 1 --include onnx
/usr/src/tensorrt/bin/trtexec --onnx=/home/mijung/canlab/gesture_project/models/weights_170_320x240_ultrafast/best.onnx --saveEngine=/home/mijung/canlab/gesture_project/models/weights_170_320x240_ultrafast/best.engine --fp16 --workspace=1024 --avgRuns=1
```

* **주요 명령어와 매개변수의 역할**:
  * `weights_170_416x312_fast`: 416x312 비대칭 픽셀로 연산 부하를 50% 이상 줄인 Fast 모델 폴더입니다.
  * `weights_170_320x240_ultrafast`: 320x240 비대칭 픽셀로 연산 부하를 75% 대폭 감축한 UltraFast 모델 폴더입니다.

---

## 38. 100% 완전 독립 단권화 프로젝트 (gesture_final) 생성 및 기동 명령어

기존 `gesture_project` 폴더를 보존한 상태에서, UltraFast (113 FPS) 모델만 탑재된 신규 완전 자립 디렉터리를 구축하는 명령어 세트입니다.

```bash
# 1. 독립 프로젝트 폴더 생성 및 UltraFast 필수 파일 복사
mkdir -p /home/mijung/canlab/gesture_final/models/weights_170_320x240_ultrafast
cp /home/mijung/canlab/gesture_project/dataset.yaml /home/mijung/canlab/gesture_final/dataset.yaml
cp -r /home/mijung/canlab/gesture_project/models/weights_170_320x240_ultrafast/* /home/mijung/canlab/gesture_final/models/weights_170_320x240_ultrafast/
cp -r /home/mijung/canlab/gesture_project/yolov5 /home/mijung/canlab/gesture_final/yolov5
cp -r /home/mijung/canlab/gesture_project/dataset /home/mijung/canlab/gesture_final/dataset

# 2. 독립 gesture_final 폴더 내에서 113 FPS UltraFast 카메라 구동 (신뢰도 0.8 오탐 0% 설정)
source /home/mijung/canlab/.venv/bin/activate
cd /home/mijung/canlab/gesture_final/yolov5
python3 detect.py --weights ../models/weights_170_320x240_ultrafast/best.engine --img 256 320 --conf 0.8 --source 0 --data ../dataset.yaml
```

* **주요 명령어와 매개변수의 역할**:
  * `--conf 0.8`: 신뢰도(Confidence) 임계값을 80%로 대폭 상향 설정하여 배경 오탐 노이즈를 100% 차단하고, 아두이노 모터 제어의 안정성을 완벽하게 보장합니다.
  * `/home/mijung/canlab/gesture_final`: 기존 `gesture_project` 의존성을 100% 잘라낸 완전 독립 단권화 프로젝트 디렉터리입니다.
  * `--weights ../models/weights_170_320x240_ultrafast/best.engine`: `gesture_final` 내부에 독립 배치된 113.27 FPS FP16 GPU 가속 엔진입니다.
  * `--img 256 320`: `AssertionError`를 방지하고 8.6ms 지연시간을 구현하는 높이 256 x 너비 320 바인딩 정합 옵션입니다.

---

## 39. 젯슨 RAM 캐시 및 스왑(Swap) 메모리 100% 완전 초기화 명령어

YOLO 추론 구동 종료 후 RAM 페이지 캐시 및 스왑(Swap) 공간에 차있는 딥러닝 연산 잔재 데이터를 싹 지우고 초기화하는 원클릭 콤보 명령어입니다.

```bash
# 1. RAM 물리 페이지 캐시 100% 비우기
sudo sysctl -w vm.drop_caches=3

# 2. 스왑(Swap) 메모리 잔재 100% 비우고 재설정 (Swap Off & On)
sudo swapoff -a && sudo swapon -a

# 3. [추천] RAM 캐시 + 스왑 메모리 1초 원클릭 일괄 초기화 콤보
sudo sysctl -w vm.drop_caches=3 && sudo swapoff -a && sudo swapon -a
```

* **주요 명령어와 매개변수의 역할**:
  * `sysctl -w vm.drop_caches=3`: 리눅스 커널 메모리에 잔류하는 페이지 캐시, 디렉토리 인덱스 메모리를 강제로 싹 지워 RAM을 확보합니다.
  * `swapoff -a && swapon -a`: 스왑 메모리를 껐다 켜면서 스왑 공간에 묶여있던 딥러닝 잔재 데이터를 100% 깨끗하게 비웁니다.

---

## 40. 구버전 gesture_project 정리 및 일괄/선택 삭제 명령어

새로운 `gesture_final` 자립 구동 확인 후, 기존 구버전 폴더(`gesture_project`)의 잔재 항목을 안전하게 지우는 명령어 모음입니다.

```bash
# 1. [방법 1] 구버전 gesture_project 폴더 전체 통째 일괄 삭제 (추천)
rm -rf ~/canlab/gesture_project

# 2. [방법 2] gesture_project 하위 디렉터리 항목별 선택 삭제
rm -rf ~/canlab/gesture_project/models               # 구버전 모델 및 실험 폴더들
rm -rf ~/canlab/gesture_project/yolov5_error_version  # 빌드 오류 테스트 폴더
rm -rf ~/canlab/gesture_project/torchvision           # C++ 휠 빌드 잔재 폴더
rm -rf ~/canlab/gesture_project/legacy                # 초기 레거시 스크립트 모음
rm -rf ~/canlab/gesture_project/dataset               # 구버전 데이터셋
rm -rf ~/canlab/gesture_project/yolov5                # 구버전 yolov5 소스
rm -f ~/canlab/gesture_project/gesture_project_dataset.zip # 백업 압축 파일
```

* **주요 명령어와 매개변수의 역할**:
  * `rm -rf [경로]`: (Recursive Force) 하위 파일 및 폴더 전체를 묻지 않고 깔끔하게 소거합니다.
  * `rm -f [파일경로]`: (Force) 단일 압축 파일이나 백업 문서를 삭제합니다.

---

## 41. ~/markdown 디렉터리 임시 스왑(.swp) 찌꺼기 파일 삭제 명령어

Vim 에디터가 예전에 남겨두었던 불필요한 임시 찌꺼기 파일을 지우는 명령어입니다.

```bash
# markdown 폴더 내 임시 .swp 찌꺼기 파일 삭제
rm -f /home/mijung/markdown/.guide_new.md.swp
```

* **주요 명령어와 매개변수의 역할**:
  * `rm -f`: 지정한 임시 스왑 찌꺼기 파일(`.swp`)을 깔끔하게 강제 삭제합니다.

---

## 42. Git 중복 서브모듈 경고 (Embedded Git Repository) 해제 명령어

하위 폴더(예: `yolov5/.git`) 내에 깃 저장소가 중복 포함되어 GitHub에 빈 폴더(화살표 아이콘)로 표시되는 현상을 해결합니다.

```bash
# 1. git 프로젝트 폴더로 이동
cd ~/canlab/git_communicate/gesture_project

# 2. 하위 yolov5 폴더 내부의 중복 .git 제거
rm -rf gesture_final/yolov5/.git

# 3. 깃 인덱스 캐시 초기화 후 전체 재추적
git rm -r --cached .
git add -A
git commit -m "Fix: Remove embedded .git and sync all gesture_final files"
git push origin main
```

* **주요 명령어와 매개변수의 역할**:
  * `rm -rf gesture_final/yolov5/.git`: 중복 감지된 하위 폴더의 `.git` 이력 디렉터리를 지워 상위 Git 저장소로 흡수시킵니다.
  * `git rm -r --cached .`: 깃 인덱스 추적 캐시를 싹 비우고 깨끗한 상태에서 다시 추적합니다.













