import re

import numpy as np
import tensorflow as tf

model_path = './model.tflite'

interpreter = tf.lite.Interpreter(model_path=model_path)

class_names = open("labels.txt", "r").readlines()

def tflite_predict(image):
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()
  # print('Input details:', input_details)
  # print('Output details:', output_details)
  interpreter.allocate_tensors()
  interpreter.set_tensor(input_details[0]['index'], image)
  interpreter.invoke()
  prediction = interpreter.get_tensor(output_details[0]['index'])
  index = np.argmax(prediction[0])
  class_name = re.match(r'\d+ (.*)', class_names[index]).group(1)
  print('Class name:', class_name)
  return class_name
