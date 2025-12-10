import cv2
import numpy as np


def decode_image(img_bytes):
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return img


def encode_image(img):
    _, buffer = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 85])

    return buffer


def process_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    return processed
