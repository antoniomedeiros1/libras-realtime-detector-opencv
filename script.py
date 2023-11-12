from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import os

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

model_path = './hand_landmarker.task'

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a hand landmarker instance with the live stream mode:
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    print('hand landmarker result: {}'.format(result))

# options = HandLandmarkerOptions(
#     base_options=BaseOptions(model_asset_path=model_path),
#     running_mode=VisionRunningMode.LIVE_STREAM,
#     result_callback=print_result)

base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                       num_hands=2)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

def draw_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks_list = detection_result.hand_landmarks
  handedness_list = detection_result.handedness
  annotated_image = np.copy(rgb_image)

  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]
    handedness = handedness_list[idx]

    # Draw the hand landmarks.
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

    # Get the top left corner of the detected hand's bounding box.
    # height, width, _ = annotated_image.shape
    # x_coordinates = [landmark.x for landmark in hand_landmarks]
    # y_coordinates = [landmark.y for landmark in hand_landmarks]
    # text_x = int(min(x_coordinates) * width)
    # text_y = int(min(y_coordinates) * height) - MARGIN

    # Draw handedness (left or right hand) on the image.
    # cv2.putText(annotated_image, f"{handedness[0].category_name}",
    #             (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
    #             FONT_SIZE, HANDEDNESS_TEXT_COLOR, FONT_THICKNESS, cv2.LINE_AA)

  return annotated_image

# CAMERA can be 0 or 1 based on default camera of your computer

camera = cv2.VideoCapture(0)

with HandLandmarker.create_from_options(options) as landmarker:

  while True:

    # Grab the webcamera's image.
    ret, image = camera.read()
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    try:

      mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
      detection_result = landmarker.detect(mp_image)
      # print(f'detection_result: {detection_result}')
      annotated_image = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
      cv2.imshow('Test', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))

      preprocessed_image = cv2.resize(annotated_image, (224, 224), interpolation=cv2.INTER_AREA)

      # Make the image a numpy array and reshape it to the models input shape.
      preprocessed_image = np.asarray(preprocessed_image, dtype=np.float32).reshape(1, 224, 224, 3)

      # Normalize the image array
      preprocessed_image = (preprocessed_image / 127.5) - 1

      # Predicts the model
      prediction = model.predict(preprocessed_image)
      index = np.argmax(prediction)
      class_name = class_names[index]
      confidence_score = prediction[0][index]

      # Print prediction and confidence score
      print("Class:", class_name[2:], end="")
      print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    except Exception as e:
      print(e)
      continue

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break


camera.release()
cv2.destroyAllWindows()