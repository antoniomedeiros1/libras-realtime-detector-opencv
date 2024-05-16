import cv2
import numpy as np

from opencvapp.preprocess import preprocess_image, draw_label
from opencvapp.model import tflite_predict

def main():
  camera = cv2.VideoCapture(0)
  print("Camera is opened, press 'ESC' to close the camera.")
  
  while True:
    ret, image = camera.read()
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    try:
      preprocessed_image, preprocessed_image_landmarks = preprocess_image(image)
      prediction = tflite_predict(preprocessed_image)
      cv2.imshow('Libras SLT', draw_label(preprocessed_image_landmarks, prediction))

    except Exception as e:
      print(e)
      continue

    keyboard_input = cv2.waitKey(1)
    if keyboard_input == 27:
      break

  camera.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()