
import io
from PIL import Image
import base64
import os
import cv2
import numpy as np


fontface = cv2.FONT_HERSHEY_SIMPLEX
face_cascade = cv2.CascadeClassifier(
    "./model/haarcascade_frontalface_default.xml")


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('./model/trainningData.yml')

path = 'dataset'


def frame_to_base64(frame):
    _, im_arr = cv2.imencode('test.png', frame)
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes).decode('utf-8')
    im_b64 = f"data:image/png;base64,{im_b64}"
    return im_b64


def base64_to_frame(img_b64):
    decoded_data = base64.b64decode((img_b64))
    image = Image.open(io.BytesIO(decoded_data))
    image = image.resize((640, 480), Image.ANTIALIAS)
    frame = np.array(image)
    return frame


def get_image_with_id(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    faces = []
    IDs = []

    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')

        print(imagePath)

        Id = int(imagePath.split('\\')[1].split('.')[1])

        faces.append(faceNp)
        IDs.append(Id)

        # cv2.imshow('tranning', faceNp)
        # cv2.waitKey(10)

    return faces, IDs


def traing():
    global recognizer
    faces, Ids = get_image_with_id(path)
    recognizer.train(faces, np.array(Ids))
    recognizer.save('./model/trainningData.yml')
    # cv2.destroyAllWindows()


def get_face_ids(frame, faces):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ids = []
    for (x, y, g, h) in faces:
        roi_gray = gray[y: y+h, x: x+g]
        id, confidence = recognizer.predict(roi_gray)
        if confidence < 40:
            ids.append(id)
    return ids


def face_predict(frame, faces):
    rs = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for (x, y, g, h) in faces:
        roi_gray = gray[y: y+h, x: x+g]
        id, confidence = recognizer.predict(roi_gray)

        if confidence < 40:
            label = f'{id} {confidence}'
            cv2.putText(frame, label, (x + 10, y + h + 30),
                        fontface, 1, (0, 255, 0), 2)
        else:
            label = f'Unknow {confidence}'
            cv2.putText(frame, label, (x + 10, y + h + 30),
                        fontface, 1, (0, 255, 0), 2)

    return frame


def get_count_user():
    count = 0
    for root, dirs, files in os.walk('./dataset'):
        for file in files:
            arr = file.split('.')
            user_id = int(arr[1])
            if user_id > count:
                count = user_id

    return count


def get_count_img(name):
    count = 0
    for root, dirs, files in os.walk('./dataset'):
        for file in files:
            arr = file.split('.')
            user_id = int(arr[1])
            if user_id == name:
                file_id = int(arr[2])
                if file_id > count:
                    count = file_id
    return count


def save_dataset(frame, faces, name):
    count = 0
    if not os.path.exists('dataset'):
        os.makedirs('dataset')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for (x, y, g, h) in faces:
        cv2.rectangle(frame, (x, y), (x+g, y+h), (0, 225, 0), 2)
        count = get_count_img(name)+1
        file = f'./dataset/User.{name}.{count}.jpg'
        cv2.imwrite(file, gray[y: y+h, x: x + g])
    return count


def draw_box(frame, faces):
    for (x, y, g, h) in faces:
        cv2.rectangle(frame, (x, y), (x+g, y+h), (0, 225, 0), 2)

    # cv2.imshow('frame', frame)
    # cv2.waitKey(1)
    return frame


def face_detect(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return faces
