from opencvapp.defaults import *

import cv2
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2


model_path = './hand_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
landamrker = HandLandmarker.create_from_options(options)

def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
  print('hand landmarker result: {}'.format(result))

def draw_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)

  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    hand_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      hand_landmarks_proto,
      solutions.hands.HAND_CONNECTIONS,
      solutions.drawing_styles.get_default_hand_landmarks_style(),
      solutions.drawing_styles.get_default_hand_connections_style())

  return annotated_image

def preprocess_image(image: np.ndarray, landmarker = landamrker):
  h, w = image.shape[:2]
  if h > w:
    image = image[h//2 - w//2: h//2 + w//2, :]
  elif w > h:
    image = image[:, w//2 - h//2: w//2 + h//2]
  preprocessed_image = cv2.resize(image, (480, 480), interpolation=cv2.INTER_AREA)
  preprocessed_image = cv2.cvtColor(preprocessed_image, cv2.COLOR_BGR2RGB)
  mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=preprocessed_image)
  detection_result = landmarker.detect(mp_image)    
  preprocessed_image = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
  preprocessed_image_landmarks = cv2.cvtColor(preprocessed_image, cv2.COLOR_RGB2BGR)
  preprocessed_image = cv2.resize(preprocessed_image_landmarks, (224, 224), interpolation=cv2.INTER_AREA)
  preprocessed_image = np.asarray(preprocessed_image, dtype=np.uint8).reshape(1, 224, 224, 3)
  return preprocessed_image, preprocessed_image_landmarks

def draw_label(image, label):
  cv2.putText(image, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
  return image  
