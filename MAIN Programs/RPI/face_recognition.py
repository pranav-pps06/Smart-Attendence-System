import dlib
import numpy as np
import os
import cv2
from datetime import datetime

face_detector = dlib.get_frontal_face_detector()
face_rec_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
shape_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

known_faces_dir = "known_faces"
known_encodings = []
known_names = []

def load_known_faces():
    for filename in os.listdir(known_faces_dir):
        image = cv2.imread(os.path.join(known_faces_dir, filename))
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        faces = face_detector(rgb)
        if faces:
            shape = shape_predictor(rgb, faces[0])
            encoding = np.array(face_rec_model.compute_face_descriptor(rgb, shape))
            known_encodings.append(encoding)
            known_names.append(os.path.splitext(filename)[0])

def recognize_face(image_path):
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = face_detector(rgb)

    for face in faces:
        shape = shape_predictor(rgb, face)
        encoding = np.array(face_rec_model.compute_face_descriptor(rgb, shape))
        matches = [np.linalg.norm(encoding - known) for known in known_encodings]
        if matches:
            best_match = np.argmin(matches)
            if matches[best_match] < 0.6:
                return known_names[best_match]
    return "Unknown"

load_known_faces()
