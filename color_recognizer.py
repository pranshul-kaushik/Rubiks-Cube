import numpy as np
from PIL import Image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from scipy import stats
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

def collect_init_samples(arr, _, color = None):
    yellow = [161, 117, 3]
    green = [5, 68, 6]
    orange = [178, 48, 5]
    red = [164, 8, 21]
    white = [162, 162, 164]
    blue = [5, 35, 126]

    """orange = [255,69,0]
    yellow = [255,255,0]
    white = [255,255,255]
    red = [139,0,0]
    blue = [0,0,139]
    green = [0,128,0] """

    if color == None:
        orange_dist = []
        yellow_dist = []
        white_dist = []
        red_dist = []
        blue_dist = []
        green_dist = []
    else:
        problem_color =  {
            color[0] : [],
            color[1] : []
        }
    while _:
        x = np.random.randint(arr.shape[0])
        y = np.random.randint(arr.shape[1])
        pix = arr[x][y]
        if color == None:
            orange_dist += [ColorDistance(pix, orange)] 
            yellow_dist += [ColorDistance(pix, yellow)]
            white_dist += [ColorDistance(pix, white)]
            red_dist += [ColorDistance(pix, red)]
            blue_dist += [ColorDistance(pix, blue)]
            green_dist += [ColorDistance(pix, green)]
        else:
            if "orange" in problem_color.keys():
                problem_color["orange"] += [ColorDistance(pix, orange)]
            if "yellow" in problem_color.keys():
                problem_color["yellow"] += [ColorDistance(pix, yellow)]
            if "white" in problem_color.keys():
                problem_color["white"] += [ColorDistance(pix, white)]
            if "red" in problem_color.keys():
                problem_color["red"] += [ColorDistance(pix, red)]
            if "blue" in problem_color.keys():
                problem_color["blue"]+= [ColorDistance(pix, blue)]
            if "green" in problem_color.keys():
                problem_color["green"]+= [ColorDistance(pix, green)]
        _ -= 1 
    if color == None:
        return {
            "orange": orange_dist,
            "yellow": yellow_dist,
            "white" : white_dist, 
            "red"   : red_dist, 
            "blue"  : blue_dist,
            "green" : green_dist
              }
    else:
        return problem_color

def color_detector(arr, to_be_careful = False):
    dist = collect_init_samples(arr, 100)
    number_sample = 100
    flag = 0
    if not to_be_careful:
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
    else:
        while flag != 6:
            min_c = random.choice(list(dist.keys()))
            min_c_dist = dist[min_c]
            number_sample = 100
            p_value = 1
            for each_c in dist.keys():
                statistic, p_value = stats.ttest_ind(dist[each_c], min_c_dist)
                while p_value < 0.1 and statistic < 0:
                    statistic, p_value = stats.ttest_ind(dist[each_c], min_c_dist)
                    number_sample *= 4
                    new_dist_samples = collect_init_samples(arr, number_sample, color = [min_c, each_c])
                    for each_new_c in new_dist_samples.keys():
                        dist[each_new_c] += new_dist_samples[each_new_c]
                    if p_value < 0.1:
                        break
                    print(statistic, p_value)
                if statistic < 0:
                    min_c = each_c
                    min_c_dist = dist[min_c]
                flag += 1
    return min_c

""" color = "red"
img = Image.open(os.path.dirname(__file__) + f'/division/{color}.jpeg')
arr = np.array(img)
print(color_detector(arr)) """