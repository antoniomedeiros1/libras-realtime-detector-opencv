import cv2
import re
import numpy as np
import tensorflow as tf

from model import tflite_predict, tflite_all_results

image = cv2.imread('./Dois2004.png')
# image = cv2.imread('./Febre1007.png')

preprocessed_image = cv2.resize(image, (224, 224))
preprocessed_image = np.expand_dims(preprocessed_image, axis=0)
preprocessed_image = np.asarray(preprocessed_image, dtype=np.uint8).reshape(1, 224, 224, 3)

# image = tf.io.read_file('./Febre1007.png')
# preprocessed_image = tf.image.decode_png(image, channels=3)
# preprocessed_image = tf.image.resize(preprocessed_image, [224, 224])
# # preprocessed_image = tf.cast(preprocessed_image, tf.uint8)
# preprocessed_image = tf.expand_dims(preprocessed_image, axis=0)

output = tflite_all_results(preprocessed_image)
# print(output)

class_names = open("dict.txt", "r").readlines()
for i in range(len(output[0])):
  print(f'{class_names[i][:-1]}: {output[0][i]}')

print('Prediction: ', tflite_predict(preprocessed_image))

while True:
    cv2.imshow('Libras SLT', image)
    keyboard_input = cv2.waitKey(1)
    if keyboard_input == 27:
      break
