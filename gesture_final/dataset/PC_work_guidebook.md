# 💻 PC YOLOv5 모델 학습 가이드북 (PC_work_guidebook)

이 문서는 젯슨 나노에서 정돈된 **[사람, 주먹, 보자기] 3클래스 데이터셋**을 사용자님의 고성능 GPU PC 환경(파이참 중심)으로 이식하여 안전하고 빠른 속도로 학습시킨 뒤, 최종 가중치(`best.pt`)를 다시 젯슨 나노로 회수하기 위한 전체 작업 절차서입니다.

---

## 📌 [Step 1] PC 작업공간 구조 설계

압축 파일(`gesture_project_dataset.zip`)을 PC의 임의의 작업 디렉토리(예: `C:\gesture_project\`)에 해제하면 다음과 같은 구조로 파일들이 평면 정렬되어 있어야 합니다.

```text
C:\gesture_project\
├── dataset\                  <-- 젯슨나노에서 넘어온 가공 완료 데이터셋 폴더
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   └── labels/
│       ├── train/
│       └── val/
├── yolov5\                   <-- PC에서 다운받아 병합할 공식 YOLOv5 라이브러리 폴더
│   ├── train.py
│   ├── detect.py
│   └── ...
├── dataset.yaml              <-- 3클래스 경로 설정 파일
├── run_training.py           <-- 원클릭 학습 구동 자동화 스크립트
└── dataset\PC_work_guidebook.md <-- 본 가이드북 파일
```

---

## 📌 [Step 2] PC 파이참(PyCharm) 환경 세팅 및 의존성 설치

1. **PC용 YOLOv5 코드 다운로드**:
   * PC의 `C:\gesture_project\` 폴더 안에서 터미널을 열고 아래 명령어로 YOLOv5 공식 소스코드를 내려받습니다.
     ```bash
     git clone https://github.com/ultralytics/yolov5.git
     ```
2. **파이참 프로젝트 열기**:
   * 파이참을 실행한 뒤, `Open`을 눌러 `C:\gesture_project\` 폴더를 프로젝트 루트로 선택하여 엽니다.
3. **가상환경 연동 및 패키지 설치**:
   * 파이참 하단의 `Terminal` 탭을 열고 가상환경(venv 등)이 활성화되어 있는지 확인한 뒤, 다음 명령어를 실행하여 필수 라이브러리를 설치합니다.
     ```bash
     pip install -r yolov5/requirements.txt
     ```
     *(PyTorch는 사용하시는 PC의 CUDA 버전에 호환되는 버전으로 별도 설치되어 있어야 고속 GPU 학습이 활성화됩니다.)*

---

## 📌 [Step 3] Roboflow '사람(person)' 데이터 수동 추가 병합 방법

현재 젯슨 나노에서 가져온 `dataset` 내에는 `coco128`에서 가져온 약 61장의 사람 데이터가 이미 포함되어 있으나, 데이터 균형을 맞추기 위해 PC에서 고품질 사람 데이터를 추가로 수집하여 합치는 방법입니다.

1. **Roboflow Universe 데이터 다운로드**:
   * PC 브라우저로 [Roboflow Universe](https://universe.roboflow.com/)에 접속하여 `person detection yolo` 키워드로 검색합니다.
   * 이미지 개수가 500장~1,000장 수준인 검증된 프로젝트를 선택하여 **`YOLOv5 PyTorch`** 포맷의 ZIP 파일로 다운로드합니다.
2. **라벨 클래스 번호 보정 확인**:
   * 다운로드받은 사람 데이터셋 폴더 내의 `.txt` 파일 중 아무 파일이나 열어봅니다.
   * 텍스트 라벨 내용의 맨 첫 숫자가 **`0`** (예: `0 0.523 0.412 ...`)으로 되어 있는지 확인합니다. 만약 다른 번호로 되어 있다면, 텍스트 일괄 수정 툴 등을 활용해 첫 행 숫자를 `0`으로 일치시켜 주어야 합니다. (우리 프로젝트의 `0`번 클래스가 `person`이기 때문입니다.)
3. **데이터셋 융합 (드래그 앤 드롭)**:
   * 다운받은 사람 데이터셋 폴더 안의 이미지(`.jpg`)와 텍스트 라벨(`.txt`) 파일들을, 우리 폴더의 경로에 맞추어 마우스로 드래그하여 그대로 집어넣습니다.
     * 사람 `train` 이미지들 $\rightarrow$ `C:\gesture_project\dataset\images\train\`
     * 사람 `train` 라벨들 $\rightarrow$ `C:\gesture_project\dataset\labels\train\`
     * 사람 `val` 이미지들 $\rightarrow$ `C:\gesture_project\dataset\images\val\`
     * 사람 `val` 라벨들 $\rightarrow$ `C:\gesture_project\dataset\labels\val\`
   * *이때 파일명이 겹치지 않도록 주의합니다. (Roboflow 기본 파일명은 고유 UUID 형태이므로 충돌하지 않습니다.)*

---

## 📌 [Step 4] dataset.yaml 파일 세팅 내용 검토

학습이 돌아가기 전에 `C:\gesture_project\dataset.yaml` 파일의 내용이 아래와 같이 정밀 선언되어 있는지 최종 확인합니다.

```yaml
path: C:/gesture_project/dataset  # PC 내 데이터셋 폴더 절대 경로 (슬래시/로 표기 권장)
train: images/train
val: images/val

nc: 3                             # 클래스 총 개수 (person, fist, palm)
names: ['person', 'fist', 'palm'] # 클래스 번호 순서에 따른 한글/영문 식별 이름
```

---

## 📌 [Step 5] run_training.py 원클릭 자동 학습 구동

이 모든 세팅이 완료되었다면 파이참의 좌측 파일 탐색기 트리에서 **`run_training.py`** 파일을 찾아 마우스 우클릭을 한 후, **`Run 'run_training'`** 메뉴를 클릭하여 실행합니다.

학습이 시작되면 터미널 창에 실시간으로 GPU가 사용되는 연산 현황과 Epoch에 따른 손실율(Loss)이 모니터링됩니다.

### 💡 학습 구동 코드 파라미터 기술 상세 가이드

`run_training.py`를 통해 실행되는 YOLOv5 내부 구동 파라미터의 상세 기술 명세입니다.

```bash
python train.py --img 320 --batch 16 --epochs 100 --data C:/gesture_project/dataset.yaml --weights yolov5n.pt --device 0
```

* **핵심 매개변수들의 역할 및 설정값의 의미**:
  * `train.py`: YOLOv5 라이브러리 내의 공식 모델 학습 전용 파이썬 구동 엔진 파일입니다.
  * `--img`: 입력 이미지 크기입니다. 젯슨 나노 임베디드 보드와 아두이노 Uno Q간의 실시간 서보모터 제어 통신 연산 부하를 차단하고 실시간 추론 프레임(FPS)을 최대한 확보하기 위해 **`320`** (320x320 해상도)으로 규격화하여 컴팩트하게 학습시킵니다.
  * `--batch`: 신경망 1회 경사 하강 학습 시 메모리에 한 번에 올리는 이미지의 장수입니다. 일반 사용자 PC GPU 메모리(OOM 방지)와 연산 안정성을 확보하기 위해 표준 가중치 규격인 **`16`**으로 튜닝하였습니다.
  * `--epochs`: 전체 데이터셋을 반복하여 모델을 훈련시키는 총 횟수입니다. 3가지 다른 사물(사람의 몸통 실루엣, 주먹 제스처의 외곽선, 보자기 제스처의 손가락 돌출 특징)의 뼈대 수렴을 안전하게 달성하기 위해 기본 **`100`**회로 설정합니다.
  * `--data`: 데이터셋의 물리적 위치 정보와 3가지 타겟 이름이 기입된 `dataset.yaml` 설정 파일의 절대 경로입니다. 
  * `--weights`: 학습의 모태가 될 전이 학습 가중치 파일입니다. 연산 능력이 제한된 젯슨 나노 보드에서의 실시간 동작 부하를 원천 방제하기 위해 YOLOv5 라인업 중 가장 작고 가벼운 모델인 **`yolov5n.pt`** (Nano 버전)를 백본 구조로 채택했습니다.
  * `--device`: 학습에 사용될 하드웨어 그래픽 카드 장치 번호입니다. PC의 CUDA 가속이 지원되는 주 그래픽카드를 동작시키기 위해 기본 ID 번호인 **`0`**을 사용합니다.

---

## 📌 [Step 6] 학습 완료 후 젯슨 나노로 가중치 회수

1. **`best.pt` 가중치 복사 확인**:
   * 학습이 완전히 성공하여 100 Epoch을 돌파하면, `run_training.py` 스크립트가 알아서 학습 최적 가중치인 `best.pt` 파일을 `C:\gesture_project\` 루트 경로 아래로 자동 복사하여 안전하게 꺼내옵니다.
2. **젯슨 나노로 전송**:
   * 이 생성된 **`best.pt`** 파일을 이메일, USB, 혹은 SFTP 전송 툴(예: FileZilla)을 활용하여 젯슨 나노 보드 내부의 아래 경로에 고스란히 이식해 둡니다.
     * 이식할 젯슨 나노 내 경로: `/home/mijung/canlab/gesture_project/yolov5/best.pt`
3. **다음 단계 구동 테스트**:
   * 가중치 파일 배치가 완료되면 젯슨 나노 보드 환경으로 돌아와서 4단계(ONNX 변환 및 모터 제어 구동 코드 연동 테스트)를 지시해 주시면 됩니다.
