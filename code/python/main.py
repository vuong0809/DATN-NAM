
import base64
from typing import List, Optional
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import time

import utils
import cv2


class CreateUser(BaseModel):
    id: Optional[int]
    image_base64: str


class GetFaceId(BaseModel):
    image_base64: str


app = FastAPI()

origins = ["*"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )


car_img = ''


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.post('/api/face-id')
def get_id(form_data: GetFaceId):
    img_b64 = form_data.image_base64.split(',')[1]
    frame = utils.base64_to_frame(img_b64)
    faces = utils.face_detect(frame)
    frame = utils.face_predict(frame, faces)
    ids = utils.get_face_ids(frame, faces)

    frame = utils.draw_box(frame, faces)
    return {
        "id": ids[0]if len(ids) > 0 else 0,
        "img": utils.frame_to_base64(frame)
    }


@app.post('/api/dataset')
def post_data_set(form_data: CreateUser):
    if form_data.id == 0:
        form_data.id = utils.get_count_user()+1

    count = utils.get_count_img(form_data.id)
    img_b64 = form_data.image_base64.split(',')[1]
    id = 0
    frame = utils.base64_to_frame(img_b64)
    faces = utils.face_detect(frame)
    if count < 200:
        count = utils.save_dataset(frame, faces, form_data.id)
    else:
        utils.traing()
        ids = utils.get_face_ids(frame, faces)
        id = ids[0]if len(ids) > 0 else 0
        frame = utils.face_predict(frame, faces)

    frame = utils.draw_box(frame, faces)
    img_b64 = utils.frame_to_base64(frame)

    return {
        "user_id": form_data.id,
        "id": id,
        "img": img_b64
    }


@app.post('/api/car')
def car(form_data: GetFaceId):
    global car_img
    img_b64 = form_data.image_base64.split(',')[1]
    frame = utils.base64_to_frame(img_b64)
    faces = utils.face_detect(frame)

    frame = utils.face_predict(frame, faces)
    frame = utils.draw_box(frame, faces)
    # cv2.imshow('frame', frame)
    # cv2.waitKey(1)

    car_img = utils.frame_to_base64(frame)
    return utils.distance_finder(faces)


@app.get('/api/car')
def get():
    return car_img


app.mount("/", StaticFiles(directory="html", html=True), name="view")
