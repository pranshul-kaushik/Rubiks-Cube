from PIL import Image
import numpy as np
import partitioner, color_recognizer, colors
import os

def rectifier(pos, label):
    img = Image.open(os.path.dirname(__file__) + f'/division/{pos}.jpeg')
    arr = np.array(img)
    exec(f"colors.{label} = list(map(int, arr.mean(axis = 1).mean(0)))")

img = Image.open(os.path.dirname(__file__) + f'/media/face.jpeg')
arr = np.array(img)
div = partitioner.divide_face(arr)
for div_name, div_arr in div.items():
    print(div_name, color_recognizer.color_detector(div_arr))

ok = int(input("\n\nCorrrect (0 No/1 Yes):- "))
if ok == 0:
    _ = int(input("How many are wrong :- "))
    while _:
        rectifier(*input("/nPos and Correct color :- ").split())
        _ -= 1
    
    for div_name, div_arr in div.items():
        print(div_name, color_recognizer.color_detector(div_arr))
