import cv2
import dlib
import mediapipe as mp
import time
import numpy as np
import os

# ============= Iestatījumi =============
IMG_PATH = "photo.jpg"
MODEL_DIR = "models"


# ============= 1. OpenCV Haar Cascade =============
def detect_haar(img):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    start = time.time()
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    end = time.time()
    return faces, end - start


# ============= 2. Dlib HoG =============
def detect_dlib_hog(img):
    detector = dlib.get_frontal_face_detector()
    start = time.time()
    faces = detector(img)
    end = time.time()
    results = [(f.left(), f.top(), f.width(), f.height()) for f in faces]
    return results, end - start


# ============= 3. OpenCV DNN =============
def detect_opencv_dnn(img):
    modelFile = os.path.join(MODEL_DIR, "res10_300x300_ssd_iter_140000_fp16.caffemodel")
    configFile = os.path.join(MODEL_DIR, "deploy.prototxt")
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
    (h, w) = img.shape[:2]
    blob = cv2.dnn.blobFromImage(
        cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
    )
    start = time.time()
    net.setInput(blob)
    detections = net.forward()
    end = time.time()
    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")
            faces.append((x1, y1, x2 - x1, y2 - y1))
    return faces, end - start


# ============= 4. Dlib CNN =============
def detect_dlib_cnn(img):
    model_path = os.path.join(MODEL_DIR, "mmod_human_face_detector.dat")
    cnn_detector = dlib.cnn_face_detection_model_v1(model_path)
    start = time.time()
    detections = cnn_detector(img, 1)
    end = time.time()
    faces = [
        (d.rect.left(), d.rect.top(), d.rect.width(), d.rect.height())
        for d in detections
    ]
    return faces, end - start


# ============= 5. Mediapipe =============
def detect_mediapipe(img):
    mp_face = mp.solutions.face_detection
    mp_draw = mp.solutions.drawing_utils
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    start = time.time()
    with mp_face.FaceDetection(
        model_selection=0, min_detection_confidence=0.5
    ) as detector:
        results = detector.process(rgb)
    end = time.time()
    faces = []
    if results.detections:
        for detection in results.detections:
            box = detection.location_data.relative_bounding_box
            h, w, _ = img.shape
            x, y, ww, hh = (
                int(box.xmin * w),
                int(box.ymin * h),
                int(box.width * w),
                int(box.height * h),
            )
            faces.append((x, y, ww, hh))
    return faces, end - start


# ============= Izpilde =============
img = cv2.imread(IMG_PATH)
if img is None:
    raise FileNotFoundError(f"Nevar atvērt attēlu: {IMG_PATH}")

detectors = {
    "Haar Cascade": detect_haar,
    "Dlib HoG": detect_dlib_hog,
    # "OpenCV DNN": detect_opencv_dnn,
    # "Dlib CNN": detect_dlib_cnn,
    "Mediapipe": detect_mediapipe,
}

results = {}

for name, func in detectors.items():
    print(f"--- Testē: {name} ---")
    try:
        faces, duration = func(img.copy())
        results[name] = {"faces": len(faces), "time": duration}
        print(f"Atrastas {len(faces)} sejas, laiks: {duration:.3f}s")
    except Exception as e:
        results[name] = {"faces": 0, "time": None}
        print(f"⚠️ {name} neizdevās: {e}")

# ============= Rezultātu tabula =============
print("\n=== REZULTĀTI ===")
print(f"{'Algoritms':<15} {'Sejas':<5} {'Laiks (s)':<10}")
print("-" * 35)
for name, res in results.items():
    print(f"{name:<15} {res['faces']:<5} {res['time'] if res['time'] else '-':<10}")
