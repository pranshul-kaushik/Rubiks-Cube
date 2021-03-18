from PIL import Image
import numpy as np
import partitioner, color_recognizer
import os

img = Image.open(os.path.dirname(__file__) + f'/media/face.jpeg')
arr = np.array(img)
div = partitioner.divide_face(arr)
for div_name, div_arr in div.items():
    print(div_name, color_recognizer.color_detector(div_arr, to_be_careful= False))
