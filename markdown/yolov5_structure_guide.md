# Jetson Nano YOLOv5 디렉토리 구조 및 패치 현황 가이드

본 문서는 Jetson Nano(Python 3.6 가상환경)에 배포된 YOLOv5 실행 환경의 디렉토리 구조와, 최신 가중치 모델 로딩 및 패키지 충돌 우회를 위해 수정(패치)된 파일들의 현황을 정리한 안내서입니다. 

PC에서 학습 완료 후 가중치(`.pt`)를 들고 젯슨 나노로 복귀할 때 참고하는 구조 인수인계서로 활용하십시오.

---

## 1. YOLOv5 핵심 디렉토리 구조 및 파일 역할

현재 [~/canlab/gesture_project/yolov5](file:///home/mijung/canlab/gesture_project/yolov5) 경로는 다음과 같이 구조화되어 있습니다:

```text
yolov5/
├── data/
│   └── coco128.yaml          # default 데이터셋 설정 (--data 미지정 시 자동 로드)
├── models/
│   ├── common.py             # [★패치 완료] 모델의 다양한 백엔드(TensorRT 등) 로딩 및 포워딩 클래스 정의
│   ├── yolo.py               # 역직렬화 호환을 위해 파일 최하단에 DetectionModel = Model 패치 적용
│   └── yolov5n.yaml          # 0.25배 Nano 모델 뼈대 구조 정의 파일 (학습/변환용)
├── utils/
│   ├── __init__.py           # [★패치 완료] ultralytics 이모지/스레드 종속성 우회 가상 함수 패치
│   ├── dataloaders.py        # [★패치 완료] 데이터 로딩 모듈 (:= 연산자 제거 완료)
│   ├── general.py            # [★패치 완료] YOLOv5 핵심 유틸리티 (:= 제거 및 future annotations 주석 완료)
│   ├── loss.py               # [★패치 완료] 손실 함수 모듈 (:= 연산자 제거 완료)
│   ├── plots.py              # [★패치 완료] 검출 상자 그리기 모듈 (Annotator 클래스 직접 복사 이식 완료)
│   └── triton.py             # [★패치 완료] future annotations 주석 처리 완료
├── detect.py                 # [★패치 완료] 실시간 비디오 및 웹캠 추론 메인 실행 파일 (ultralytics 임포트 우회)
├── export.py                 # [★패치 완료] 파이토치(.pt) 모델을 ONNX로 변환해주는 내보내기 스크립트
└── requirements.txt          # 패키지 의존성 정의 파일
```

---

## 2. 젯슨 나노 맞춤형 파일별 패치(수정) 내역 요약

Python 3.6 환경과의 문법 호환성 확보 및 `ultralytics` 패키지 미설치 이슈 해결을 위해 젯슨 나노 폴더 내에서 수정한 상세 이력입니다:

| 파일명 | 패치 적용 라인 | 주요 수정 이유 및 조치 사항 |
| :--- | :--- | :--- |
| **`detect.py`** | 최상단 / 47라인 부근 | * WindowsPath 에러 우회를 위한 PosixPath 강제 매핑 추가.<br>* `ultralytics.utils.plotting` 대신 로컬 `utils.plots`에서 Annotator를 가져오도록 수정. |
| **`export.py`** | 최상단 | * WindowsPath 로딩 오류 해결을 위해 PosixPath 매핑 코드 추가. |
| **`models/yolo.py`** | 최하단 | * PC에서 저장된 모델의 역직렬화 클래스 매핑 호환성 유지를 위해 `DetectionModel = Model` 클래스 앨리어스(Alias) 코드 주입. |
| **`models/common.py`** | 338라인 부근 | * TensorRT 엔진 추론 시 가상환경 내 `tensorrt` 바인딩 모듈을 정상적으로 import 할 수 있도록 구조 검증. |
| **`utils/plots.py`** | 16라인 / 최하단 | * `ultralytics` 임포트문을 제거.<br>* Pillow 및 cv2 기반의 순정 `Annotator` 그리기 클래스 및 `save_one_box` 함수 소스코드를 파일 최하단에 직접 복사 이식하여 자체 구현. |
| **`utils/__init__.py`** | 6라인 부근 | * `from ultralytics.utils import emojis, threaded` 구문 주석 처리.<br>* 로컬 비동기 멀티스레드 구현용 `threaded` 데코레이터 및 `emojis` 가상 함수 직접 구현. |
| **`utils/general.py`** | 4라인 / 178라인 | * `from __future__ import annotations` (Python 3.7+) 문법 에러 주석 차단.<br>* `:=` (바다코끼리 연산자, Python 3.8+) 문법을 일반 변수 할당문 및 `if` 조건절로 리팩토링. |
| **`utils/triton.py`** | 4라인 | * `from __future__ import annotations` 문법 에러 주석 차단. |
| **기타 loss, dataloaders 등** | 파일 내부 곳곳 | * `:=` (바다코끼리 연산자) 문법 오류 발생 라인들을 모두 하향 문법(`n = len(targets)` 형태)으로 변경 완료. |

---

## 3. PC 작업 완료 후 젯슨 나노 복귀 시 이식 및 변환 매뉴얼

PC에서 모델 훈련이 끝난 가중치 파일(`.pt`)을 들고 젯슨 나노로 복귀할 때의 작업 흐름입니다.

1. **가중치 파일 전송**: PC에서 학습 완료된 `best.pt` 파일을 젯슨 나노의 `~/canlab/gesture_project/models/[모델명]/` 폴더로 복사합니다.
2. **ONNX 변환**: 젯슨의 `yolov5` 폴더 위치에서 아래 명령을 기동합니다. (※ 학습 해상도를 1대1로 일치시켜야 함)
   ```bash
   python3 export.py --weights ../models/[모델명]/best.pt --img 320 --batch 1 --include onnx
   ```
3. **TensorRT 가속 빌드**: `trtexec`를 기동하여 젯슨 나노 전용 엔진 가중치를 컴파일합니다. (OOM 방지 옵션 필수 적용)
   ```bash
   /usr/src/tensorrt/bin/trtexec --onnx=../models/[모델명]/best.onnx --saveEngine=../models/[모델명]/best.engine --fp16 --workspace=1024 --avgRuns=1
   ```
4. **실시간 검증 실행**: 매핑 오류 방지 옵션(`--data`)과 감지할 클래스 필터(`--classes`)를 지정해 실시간 비디오를 띄웁니다.
   ```bash
   python3 detect.py --weights ../models/[모델명]/best.engine --img 320 --conf 0.25 --source 0 --data ../dataset.yaml --classes 1 2
   ```

---

## 4. ⚠️ 핵심 패치 소스코드(.py)의 PC 이관 시 활용 지침

압축 파일에 동봉된 4개의 파이썬 소스 파일(`detect.py`, `export.py`, `plots.py`, `__init__.py`)은 PC 이관 시 다음과 같은 목적에 한해서만 국한하여 활용해야 합니다.

### ① PC 학습 시 적용 배제 (순정 코드 훈련 원칙)
* PC 개발 환경에서 모델을 학습(`train.py` 기동)할 때는 젯슨 나노용 하향 호환 패치가 적용된 이 파일들을 **사용하지 마십시오.** 
* PC 학습은 PC의 최신 Python 및 PyTorch 환경에 최적화된 **순정 YOLOv5 코드 전체를 그대로 사용**해야 가속 훈련 기술과 시각화 도구가 정상 작동합니다.

### ② 주요 활용 용도
1. **코드 비교 분석 레퍼런스 (Diff)**: PC의 최신 코드와 젯슨용 하향 패치 코드 간의 차이점을 VSCode 등의 개발 툴로 직접 비교 검토하여, 젯슨의 환경적 제약 사항을 파악하는 기술 교과서로 사용합니다.
2. **배포용 복구 백업본**: PC에서 새로운 모델 학습이 성공적으로 끝나 가중치(`.pt`)를 들고 젯슨으로 다시 돌아왔을 때, 젯슨 나노의 `yolov5` 폴더에 이 4개의 패치 파일들을 그대로 덮어쓰기하여 오류 없는 구동 환경을 1초 만에 원상 복구하는 배포 백업본으로 사용합니다.
