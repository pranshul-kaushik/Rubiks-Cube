import numpy as np
from PIL import Image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from scipy import stats
import colors
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

def collect_samples(arr, _):
    yellow = colors.yellow
    green = colors.green
    orange = colors.orange
    red = colors.red
    white = colors.white
    blue = colors.blue

    """orange = [255,69,0]
    yellow = [255,255,0]
    white = [255,255,255]
    red = [139,0,0]
    blue = [0,0,139]
    green = [0,128,0] """

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
    number_sample = 300
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
