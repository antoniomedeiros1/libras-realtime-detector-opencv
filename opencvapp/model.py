import re

import numpy as np
import tensorflow as tf

model_path = './model.tflite'

interpreter = tf.lite.Interpreter(model_path=model_path)

class_names = open("dict.txt", "r").readlines()

def tflite_predict(image):
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()
  # print('Input details:', input_details)
  # print('Output details:', output_details)

  input_type = input_details[0]['dtype']
  if input_type == np.uint8:
    input_scale, input_zero_point = input_details[0]['quantization']
    print("Input scale:", input_scale)
    print("Input zero point:", input_zero_point)
    print()
    image = (image / input_scale) + input_zero_point
    image = np.around(image).astype('uint8')

  interpreter.allocate_tensors()
  interpreter.set_tensor(input_details[0]['index'], image)
  interpreter.invoke()
  output = interpreter.get_tensor(output_details[0]['index'])

  output_type = output_details[0]['dtype']
  if output_type == np.uint8:
    output_scale, output_zero_point = output_details[0]['quantization']
    print("Raw output scores:", output)
    print("Output scale:", output_scale)
    print("Output zero point:", output_zero_point)
    print()
    output = output_scale * (output.astype(np.float32) - output_zero_point)
    
  prediction = interpreter.get_tensor(output_details[0]['index'])
  index = np.argmax(prediction[0])
  return class_names[index]

def tflite_all_results(image):
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()
  # print('Input details:', input_details)
  # print('Output details:', output_details)

  input_type = input_details[0]['dtype']
  if input_type == np.uint8:
    input_scale, input_zero_point = input_details[0]['quantization']
    # print("Input scale:", input_scale)
    # print("Input zero point:", input_zero_point)
    # print()
    image = (image / input_scale) + input_zero_point
    image = np.around(image).astype('uint8')

  interpreter.allocate_tensors()
  interpreter.set_tensor(input_details[0]['index'], image)
  interpreter.invoke()
  output = interpreter.get_tensor(output_details[0]['index'])
  
  output_type = output_details[0]['dtype']
  if output_type == np.uint8:
    output_scale, output_zero_point = output_details[0]['quantization']
    # print("Raw output scores:", output)
    # print("Output scale:", output_scale)
    # print("Output zero point:", output_zero_point)
    # print()
    output = output_scale * (output.astype(np.float32) - output_zero_point)

  return output