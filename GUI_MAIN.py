import eel
import numpy as np
import threading
import GUI_Camera
import GUI_ADD_CLASS
import os
import shutil
from plot_img_utils import plot_img

thread = None
web_app_options = {'port': 0,}
#カメラのON_OFF
Camera_Flag = False
#お試し
count = 0

#必用なファイル作成
os.makedirs('./Data',exist_ok=True)

#手検知
def hand_detection():
    
    #trimming内のデータを削除
    if os.path.exists('./trimming'):
        shutil.rmtree("./trimming")
    os.makedirs("./trimming",exist_ok=True)

    #手の検出結果の座標を削除
    #バウンディングボックスの座標をメモ
    if os.path.exists('./hand_box_save'):
        shutil.rmtree("./hand_box_save")
    os.makedirs("./hand_box_save",exist_ok=True)

    if os.path.exists('./video'):
        shutil.rmtree("./video")
    os.mkdir("./video")
    #pre_command = "python hand/detect.py --source 0 --conf 0.6 --device cpu"
    pre_command = "python hand/detect.py --source 0 --conf 0.7"
    test_flag = os.system(pre_command)
    return test_flag

#画像が溜まったら物検知
def obj_detection():
    
    
    #物体のトリミングファイルの削除
    
    if os.path.exists('./trimming_obj'):
        shutil.rmtree('./trimming_obj')
    
    os.makedirs('./trimming_obj',exist_ok=True)
   
    #removeフォルダ削除
    if os.path.exists('./remove'):
        shutil.rmtree('./remove')
    os.makedirs('./remove',exist_ok=True)

    #登録しているクラスを取得
    with open('./DL_img_utils/Class.txt') as f:
        data = f.readlines()
        for class_name in data:

            class_name = class_name.replace("\n","")
            print("===========================")
            print("============{}==========".format(class_name))
            print("===========================")
            #いずれ削除するかも？
            if os.path.exists('./result_img/'+class_name+'/'):
                shutil.rmtree("./result_img/"+class_name+'/')
            os.makedirs("./result_img/"+class_name+'/',exist_ok=True)
            #物体の座標を削除
            if os.path.exists("./Object_box_save/"+class_name+".txt"):
                os.remove("./Object_box_save/"+class_name+'.txt')
            #pre_command = "python object/detect.py --conf 0.65 --source ./trimming --weights object/weights/{0}.pt --output ./result_img/{0} --device cpu".format(class_name)
            pre_command = "python object/detect.py --conf 0.7 --source ./trimming --weights object/weights/{0}.pt --output ./result_img/{0} --augment".format(class_name)
            os.system(pre_command)


            plot_img.main(class_name)
    

            

def Main_Recognition():
    thread = threading.currentThread()
    while getattr(thread,"do_run",True):
        hand_detection()
        obj_detection()


@eel.expose
def Object_Recognition_function(name):
    global thread
    global Camera_Flag
    print(name)
    if name == "True":
        if Camera_Flag == True:
            thread = threading.Thread(target=Main_Recognition)
            thread.start()
        else:
            eel.Camera_error()
    else:
        if thread is not None:
            thread.do_run = False
            thread.join()
            thread = None

@eel.expose
def camera_window_open(target :str):
    print(target)
    global Camera_Flag
    if Camera_Flag == True:
        GUI_Camera.main()
    else:
        eel.Camera_error()

@eel.expose
def add_class_window_open(target :str):
    os.makedirs("./data",exist_ok=True)
    os.makedirs("./data",exist_ok=True)
    os.makedirs("./data",exist_ok=True)
    print(target)
    GUI_ADD_CLASS.main()


@eel.expose
def Camera_Switch_ON():
    global Camera_Flag
    Camera_Flag = True

@eel.expose
def Camera_Switch_OFF():
    global Camera_Flag
    Camera_Flag = False
    
#登録されているクラス名を返す
@eel.expose
def read_class_name():
    fileobj = open("./DL_img_utils/Class.txt", "r", encoding="utf_8")
    class_list = []
    while True:
        line = (fileobj.readline()).replace("\n","")
        if line:
            class_list.append(line)
        else:
            break
    return class_list

#Javascriptでファイル存在確認
#HTMLフォルダから
@eel.expose
def file_exists_OK(file_path):

    return os.path.exists(os.path.join('./web/html',file_path))


@eel.expose
def NON_function():
    global count
    count += 1
    print(count)


       
eel.init("web")
eel.start("html/main.html",
port = 0,
size=(1080, 600))
