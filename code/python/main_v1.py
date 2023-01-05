

# import fire_detect_v1 as fire_detect
import base64
import json
from typing import List
# from routes import router
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
import time
# from utils.torch_utils import select_device, smart_inference_mode
# from utils.plots import Annotator, colors, save_one_box
# from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
#                            increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
# from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
# from models.common import DetectMultiBackend
# import argparse
# import os
# import platform
# import sys
# from pathlib import Path

# from threading import Thread

# import torch

# import test as fire_detect

# FILE = Path(__file__).resolve()
# ROOT = FILE.parents[0]  # YOLOv5 root directory
# if str(ROOT) not in sys.path:
#     sys.path.append(str(ROOT))  # add ROOT to PATH
# ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


# from fastapi.openapi.utils import get_openapi

# from fire_detect_v1 import run, IMAGE


# img_rs = {
#     "rs": None,
#     # "acc": None,
#     # "xywh": None,
#     "telemetry": None,
#     "im0": None
# }

# telemetry = {}

# count = 0
app = FastAPI()

origins = ["*"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# app.include_router(router)

# app.mount("/public", StaticFiles(directory="public", html=True), name="public")
# # # app.mount("/", SPAStaticFiles(directory="view", html=True), name="view")


# @app.get("/")
# async def get():
#     return FileResponse('./public/index.html')


# @app.get("/rs")
# def get_rs():
#     return img_rs


# @app.get('/telemetry')
# def get_telemetry():
#     return telemetry


# def detect():
#     global img_rs

#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         im0, rs = fire_detect.run(frame)

#         # cv2.imshow('frame', im0)
#         # cv2.waitKey(1)

#         _, im_arr = cv2.imencode('test.jpg', im0)
#         im_bytes = im_arr.tobytes()
#         im_b64 = base64.b64encode(im_bytes).decode('utf-8')
#         im_b64 = f"data:image/jpeg;base64,{im_b64}"

#         img_rs = {
#             "rs": rs,
#             "im0": im_b64
#         }


# def connect_arduino():
#     global telemetry
#     import serial
#     ser = serial.Serial("COM9", 115200, timeout=1)
#     while (True):
#         data = ser.readline()
#         data = data.decode('utf-8')
#         if data:
#             data = json.loads(data)
#             telemetry = data


# @app.on_event("startup")
# # @repeat_every(seconds=1, wait_first=True)
# def task():
#     t1 = Thread(target=detect)
#     t2 = Thread(target=connect_arduino)
#     t1.start()
#     t2.start()
