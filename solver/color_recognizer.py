import numpy as np
from PIL import Image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from scipy import stats
import pickle
import random
import os

def ColorDistance(rgb1,rgb2):
    rgb1 , rgb2 = np.array(rgb1), np.array(rgb2)
    color1_rgb = sRGBColor(*rgb1)
    color2_rgb = sRGBColor(*rgb2)
    color1_lab = convert_color(color1_rgb, LabColor)
    color2_lab = convert_color(color2_rgb, LabColor)
    delta_e = delta_e_cie2000(color1_lab, color2_lab)
    return delta_e

class color:
    y = [161, 117, 3]
    g = [5, 68, 6]
    o = [178, 48, 5]
    r = [164, 8, 21]
    w = [255, 255, 255]
    b = [5, 35, 126]


def collect_samples(arr, _):
    try:
        with open('COLORS.pkl', 'rb') as f:
            COLORS = pickle.load(f)
        print("\nCalling \n")
    except:
        print("\nCreating \n")
        with open('COLORS.pkl', 'wb') as f:
            COLORS = color()
            pickle.dump(COLORS, f, pickle.HIGHEST_PROTOCOL)
    
    yellow = COLORS.y
    green = COLORS.g
    orange = COLORS.o
    red = COLORS.r
    white = COLORS.w
    blue = COLORS.b

    orange_dist = []
    yellow_dist = []
    white_dist = []
    red_dist = []
    blue_dist = []
    green_dist = []

    while _:
        x = np.random.randint(arr.shape[0])
        y = np.random.randint(arr.shape[1])
        pix = arr[x][y]
        orange_dist += [ColorDistance(pix, orange)] 
        yellow_dist += [ColorDistance(pix, yellow)]
        white_dist += [ColorDistance(pix, white)]
        red_dist += [ColorDistance(pix, red)]
        blue_dist += [ColorDistance(pix, blue)]
        green_dist += [ColorDistance(pix, green)]
        _ -= 1 
    return {
        "orange": orange_dist,
        "yellow": yellow_dist,
        "white" : white_dist, 
        "red"   : red_dist, 
        "blue"  : blue_dist,
        "green" : green_dist
            }

def color_detector(arr):
    number_sample = 200
    dist = collect_samples(arr, number_sample)
    flag = 0
    while flag != 6:
        min_c = random.choice(list(dist.keys()))
        min_c_dist = dist[min_c]
        flag = 0
        for each_c in dist.keys():
            statistic, p_value = stats.ttest_ind(dist[each_c], min_c_dist)
            if statistic < 0:
                min_c = each_c
                min_c_dist = dist[min_c]
            flag += 1
    return min_c
