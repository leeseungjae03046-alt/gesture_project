import os
import sys
from pathlib import Path
import cv2
import numpy as np
import torch
from flask import Flask, Response

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.common import DetectMultiBackend
from utils.datasets import LoadStreams
from utils.general import (LOGGER, check_img_size, colorstr, cv2,
                           non_max_suppression, scale_coords)
from utils.plots import Annotator, colors
from utils.torch_utils import select_device

app = Flask(__name__)

global_detector = None

class WebDetector:
    def __init__(self, weights='../models/weights_170_256x320_ultrafast/best.onnx',
                 data='../dataset.yaml', imgsz=[256, 320], conf_thres=0.8, iou_thres=0.45, use_dnn=True):
        self.weights = weights
        self.data = data
        self.imgsz = imgsz
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres

        self.device = select_device('')
        print("⚡ 퀄컴 Adreno 702 GPU + best.onnx 가속 엔진 로드 중...")
        # dnn=True 옵션으로 퀄컴 Adreno 702 GPU (OpenCL) 가속 적용
        self.model = DetectMultiBackend(weights, device=self.device, dnn=use_dnn, data=data)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size(imgsz, s=self.stride)
        self.model.warmup(imgsz=(1, 3, *self.imgsz))

    def generate(self, source='http://192.168.45.84:5000/video'):
        dataset = LoadStreams(source, img_size=self.imgsz, stride=self.stride, auto=self.pt)
        for path, im, im0s, vid_cap, s in dataset:
            im = torch.from_numpy(im).to(self.device)
            im = im.float() / 255.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

            pred = self.model(im, augment=False, visualize=False)
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, max_det=1000)

            im0 = im0s[0].copy()
            annotator = Annotator(im0, line_width=3, example=str(self.names))
            det = pred[0]
            if len(det):
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    label = f'{self.names[c]} {conf:.2f}'
                    annotator.box_label(xyxy, label, color=colors(c, True))

            result_frame = annotator.result()
            ret, buffer = cv2.imencode('.jpg', result_frame)
            if not ret:
                continue
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
@app.route('/video')
def video_feed():
    source_url = os.environ.get('SOURCE_URL', 'http://192.168.45.84:5000/video')
    return Response(global_detector.generate(source=source_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    global global_detector
    print("\n=======================================================")
    print("🚀 퀄컴 Adreno GPU + ONNX 기반 탐지 웹 서버 초기화 중...")
    global_detector = WebDetector()
    print("✨ 퀄컴 GPU + ONNX 탐지 영상 준비 완료!")
    print("👉 노트북 크롬 주소창 접속: http://192.168.45.124:7000")
    print("=======================================================\n")
    app.run(host='0.0.0.0', port=7000, debug=False)

if __name__ == '__main__':
    main()
