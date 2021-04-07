import numpy as np
from PIL import Image as im 
import os

def divide_face(arr):
    X = int(arr.shape[0]/3)
    Y = int((arr.shape[0]/3))*2
    A = int(arr.shape[1]/3)
    B = int((arr.shape[1]/3))*2

    div = {
    "top_left" : arr[0:X, 0:A],
    "top" : arr[0:X, A:B],
    "top_right" : arr[0:X, B:arr.shape[1]],
    "left" : arr[X:Y, 0:A],
    "middle" : arr[X:Y, A:B],
    "right" : arr[X:Y, B:arr.shape[1]],
    "bottom_left" : arr[Y:arr.shape[0], 0:A],
    "bottom" : arr[Y:arr.shape[0], A:B],
    "bottom_right" : arr[Y:arr.shape[0], B:arr.shape[1]]
    }

    wall = 0.25
    for div_name, div_arr in div.items():
        div[div_name] = div_arr[int(div_arr.shape[0]*wall): int(div_arr.shape[0] - div_arr.shape[0]*wall),  int(div_arr.shape[1]*wall): int(div_arr.shape[1] - div_arr.shape[1]*wall)]
    
    for div_name, div_arr in div.items():
        data = im.fromarray(div_arr) 
        data.save(f'division/{div_name}.jpeg') 
    return div