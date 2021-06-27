from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from . import partitioner, color_recognizer
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from PIL import Image
import urllib.request
import numpy as np
import kociemba
import pickle
import shutil
import json
import io
import os

def rectifier(pos, label):
    img = Image.open(f'division/{pos}.jpeg')
    arr = np.array(img)
    print("Updating the COLORS pkl")
    f = open('COLORS.pkl', 'rb')
    COLORS = pickle.load(f)   
    f.close()
    exec(f"print('Old value of ', '{label} ' ,COLORS.{label})")
    with open('COLORS.pkl', 'wb') as f:
        exec(f"COLORS.{label} = list(map(int, arr.mean(axis = 1).mean(0)))")
        pickle.dump(COLORS, f, pickle.HIGHEST_PROTOCOL)
    
    f = open('COLORS.pkl', 'rb')
    COLORS = pickle.load(f)   
    f.close()
    exec(f"print('New value of ', '{label} ' ,COLORS.{label})")

def face_recognize(path):
    img = Image.open(path)
    face = ''
    arr = np.array(img)
    div = partitioner.divide_face(arr)
    for div_name, div_arr in div.items():
        color_obs = color_recognizer.color_detector(div_arr)
        face += color_obs[0]
    return face

@csrf_exempt
def InputStream(request):
    data = request.POST.get('data')[0]
    path = "media/face.jpeg"
    urllib.request.urlretrieve(data, path)
    #path = default_storage.save(f'media/face.jpeg', ContentFile(Image.open(data).read()))
    #tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    print(path)
    face_color = face_recognize(path)
    delete_files('media')

    with open('color.face', 'w') as f:
        f.write(face_color)

    return JsonResponse({'data':face_color})

@csrf_exempt
def acknowledge(request):
    pos = {
        0 : "top_left",
        1 : "top",
        2 : "top_right",
        3 : "left",
        4 : "middle",
        5 : "right",
        6 : "bottom_left",
        7 : "bottom",
        8 : "bottom_right",
    }
    data = json.loads(request.body)['data']

    f = open('color.face', 'r')
    old = f.read()
    f.close()

    for _, color in enumerate(old):
        if data[_] != color:
            rectifier(pos[_], data[_])

    with open('color.face', 'w') as f:
        f.write(data)
    
    os.remove("color.face") 
    return JsonResponse({'data':data})

def delete_files(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

@csrf_exempt
def reset(request):
    os.remove("COLORS.pkl") 
    delete_files('media')
    delete_files('division')
    return JsonResponse({'reset':True})

@csrf_exempt
def solve(request):
    _ = 9
    cube = json.loads(request.body).get("cube")
    try:
        MAPPER_FACE_CENTER = {
            side: side_id for side, side_id in zip(['U', 'R', 'F', 'D', 'L', 'B'], [i * _ + 4 for i in range(6)])
        }
    
        for side, side_id in MAPPER_FACE_CENTER.items():
            cube = cube.replace(cube[side_id], side)
        
        print(cube)
        rotation = kociemba.solve(cube)
        
        try:
            os.remove("COLORS.pkl") 
        except:
            pass
        
        delete_files('media')
        delete_files('division')
        return JsonResponse({'rotation':rotation})
    except Exception as e:
        return JsonResponse({'error':str(e)})