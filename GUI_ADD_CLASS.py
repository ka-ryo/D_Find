import eel
from PIL import Image
import base64
import cv2
import numpy as np
from io import BytesIO
import os
import shutil
from DL_img_utils import ImageNET
import glob
from OIDv4_ToolKit import Data_Seiri

#Dataの中身を削除する
@eel.expose
def Delete_Data():
    train_path = './Data/train'
    val_path = './Data/val'

    if os.path.exists(train_path):
        shutil.rmtree(train_path)
    os.makedirs(train_path,exist_ok=True)

    if os.path.exists(val_path):
        shutil.rmtree(val_path)
    os.makedirs(val_path,exist_ok=True)

#画像読み込み
@eel.expose
def fetch_image():
    #クラスIDのひとつ前までのパス
    dir_ImageNet = 'DL_img_utils/img' 
    
    #クラスIDのフォルダパス
    class_ID_dirs = os.listdir(dir_ImageNet)

    for class_ID_dir in class_ID_dirs:
        #画像パス取得
        img_dirs = os.listdir(dir_ImageNet +"/" +class_ID_dir)
        count = 0
        #====================================================
        #今はIDになっている。テキストのクラス名を取った方が2億％いい
        #====================================================
        eel.make_radio_imgspace(class_ID_dir)
        for img_dir in img_dirs:
            image= Image.open(dir_ImageNet +"/"+class_ID_dir +"/" +img_dir)
            image=image.resize(size=(200,200))
            image = image.convert("RGB")
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            img_src = f"data:image/jpeg;base64,{str(img_str)[2:-1]}"
            eel.set_image(img_src,count,class_ID_dir)  # javascript側の画像表示関数を呼ぶ
            count += 1
            if count >= 7:
                break
    eel.make_No_match()

#入力されたクラス名が事前に登録されていないかを確認
@eel.expose
def Check_duaplicate_class(Search_txt):
    fileobj = open("./DL_img_utils/Class.txt", "r", encoding="utf_8")
    #重複確認
    Duplicate = "False"
    while True:
        line = (fileobj.readline()).replace("\n","")
        if line:
            if str(line) == str(Search_txt):
                Duplicate = "True"
        else:
            break
    return Duplicate

@eel.expose
def get_Search_class(Search_txt):
    #事前にDLされていたimgとanotationのフォルダを削除
    #img,annotationの前を削除
    print(Search_txt)
    dir_ImageNet = './DL_img_utils/'
    if os.path.exists(dir_ImageNet+'img'):
        shutil.rmtree(dir_ImageNet+'img')
    if os.path.exists(dir_ImageNet+'Annotation'):
        shutil.rmtree(dir_ImageNet+'Annotation')
    if os.path.exists(dir_ImageNet+'Data'):
        shutil.rmtree(dir_ImageNet+'Data')

    #一致したクラスの個数が帰ってくる
    result = ImageNET.Img_DL(Search_txt,7,-1)
    return result

#OIDの検索結果
@eel.expose
def OID_Search_class(Search_txt):
    dir_OID = "./OIDv4_ToolKit/"
    class_list = []
    #事前にDLされていたDataを削除
    if os.path.exists(dir_OID+'OID/Dataset'):
        shutil.rmtree(dir_OID+'OID/Dataset')
    os.mkdir(dir_OID+'OID/Dataset')

    if os.path.exists(dir_OID + 'To_Yolo'):
        shutil.rmtree(dir_OID +'To_Yolo')
    #クラスの一致数を取得
    #一致するクラスの名前を取得
    with open(dir_OID + "class_name.txt",'r', encoding='UTF-8') as f:
        read_data = f.readlines()
        for line in read_data:
            if line:
                line=line.replace("\n","")
                line=line.replace(" ","_")
                if Search_txt.upper() in line.upper():
                    class_list.append(line)
                    
    
    if len(class_list) != 0:
        #少数の画像データをDL
        pre_command = "python OIDv4_ToolKit/main.py downloader  --classes {} --type_csv train --limit 6 -y".format(' '.join(class_list))
        os.system(pre_command)

    return class_list

#OIDの画像ダウンロード
@eel.expose
def OID_download_img(class_name):
    print(class_name)
    dir_OID = "./OIDv4_ToolKit/"
    #事前にDLされていたDataを削除
    if os.path.exists(dir_OID+'OID/Dataset'):
        shutil.rmtree(dir_OID+'OID/Dataset')
    os.mkdir(dir_OID+'OID/Dataset')
    pre_command = "python OIDv4_ToolKit/main.py downloader --classes {} --type_csv all -y --limit 500".format(class_name.replace(" ","_"))
    os.system(pre_command)

    #ラベル付けを行うクラス番号
    with open("./DL_img_utils/Class.txt",'r',encoding='UTF-8') as f:
        read_data = f.readlines()
    class_number = len(read_data)
    print(class_number)

    #ファイルの整理
    #pre_command = "python OIDv4_ToolKit/OID2Yolo.py convert --class_name {} --class_number {} --dataset all ".format(class_name.replace(" ","_"),class_number)
    pre_command = "python OIDv4_ToolKit/OID2Yolo.py convert --class_name {} --dataset all ".format(class_name.replace(" ","_"))
    os.system(pre_command)
    Data_Seiri.main(class_name)

#画像を横並びで表示
@eel.expose
def OID_print_img(class_list):
    for class_name in class_list:
        dir_OID = "./OIDv4_ToolKit/"
        #DLした画像のパスを取得
        class_name = class_name.replace("_"," ")
        img_dirs = glob.glob(dir_OID+"OID/Dataset/train/"+class_name+"/*.jpg")
        #画像を表示する枠を作成
        eel.make_radio_imgspace(class_name)
        count = 0

        for img_dir in img_dirs:
            image= Image.open(img_dir)
            image=image.resize(size=(200,200))
            image = image.convert("RGB")
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            img_src = f"data:image/jpeg;base64,{str(img_str)[2:-1]}"
            eel.set_image(img_src,count,class_name)  # javascript側の画像表示関数を呼ぶ
            count += 1
            if count >= 7:
                break

    eel.make_No_match()
    
    

@eel.expose
def download_img(class_ID,class_name):
    #データをDLする
    ImageNET.ALL_DL(class_ID,class_name)

#学習開始
@eel.expose
def start_learning(class_name):
    #runs内のデータを削除
    if os.path.exists('./runs'):
        shutil.rmtree('./runs')
    pre_command = "python object/train.py --data data.yaml --weights object/yolov5s.pt --epochs 300 --batch 8"
    os.system(pre_command)
    #学習結果を移動
    if os.path.exists("./object/weights/best.pt"):
        os.remove("./object/weights/best.pt")

    #学習データを破棄する
    shutil.move("./runs/exp0/weights/best.pt","object/weights/{}.pt".format(class_name))
    #ImageNet内のデータを削除
    shutil.rmtree('img')
    shutil.rmtree('list')
    shutil.rmtree('Data')
    shutil.rmtree('Annotation')

    return 

#ターゲット画像の保存
@eel.expose
def target_img_save(src,class_name):
    src = src.split(',')[1]
    img_binary=base64.b64decode(src)
    jpg=np.frombuffer(img_binary,dtype=np.uint8)
    img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)
    cv2.imwrite('./target_img/'+class_name+'.jpg',img)

#クラスリストに追加書き込み
@eel.expose
def add_Class_txt(class_name):
    with open("./DL_img_utils/Class.txt", mode='a') as f:
        f.write('{}\n'.format(class_name))


@eel.expose
def show(s="NULL"):
    print(s)

def main():
    eel.init("web")

    web_app_options = {"chromeFlags": ["--window-size=420,200"]}
    eel.start('html/add_class.html',
            mode='chrome',
            cmdline_args=['--start-fullscreen'],
            block=False,
            port = 0,
            size=(1080, 700))

if __name__ == '__main__':
    main()