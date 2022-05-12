import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)
def convert_annotation(image_id,classes):
    #in_file = open('VOCdevkit/VOC%s/Annotations/%s.xml'%(year, image_id))
    #out_file = open('VOCdevkit/VOC%s/labels/%s.txt'%(year, image_id), 'w')
    
    #挿入
    in_file = open('../DL_img_utils/Data/Annotations/%s.xml'%(image_id))
    out_file = open('../DL_img_utils/Data/labels/%s.txt'%(image_id),'w')

    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        if bb[0] <1 and bb[1] < 1 and bb[2] < 1 and bb[3]< 1:
            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def main(class_name="None"):
    sets=[('train'),('val')]
    Data_dir = "./DL_img_utils/"
    Out_dir = "./DL_img_utils/"
    classes = []
    """
    #クラス名を読み込む
    fileobj = open(Data_dir+"Class.txt", "r", encoding="utf_8")
    while True:
        line = fileobj.readline()
        if line:
            classes.append(line)
        else:
            break

    #重複チェック
    classes=list(set(classes))
    classes = [c.replace('\n', '') for c in classes]
    #classes = ["Remote"]
    """
    classes.append(class_name.replace("\n",''))



    if not os.path.exists('./Delete'):
        os.makedirs('./Delete')
    os.chdir('./Delete')

    Data_dir = "../DL_img_utils/"

    wd = getcwd()
    for image_set in sets:
        if not os.path.exists(Data_dir+'Data/labels/'):
            os.makedirs(Data_dir+'Data/labels/')
        image_ids = open(Data_dir+'Data/ImageSets/Main/%s.txt'%(image_set)).read().strip().split()
        list_file = open('%s.txt'%(image_set), 'w')
        for image_id in image_ids:
            list_file.write(Data_dir+'Data/JPEGImages/%s.jpg\n'%(image_id))
            convert_annotation(image_id,classes)
        list_file.close()


    #ファイル移動
    os.makedirs('../Data',exist_ok=True)
    os.makedirs('../Data/train',exist_ok=True)
    os.makedirs('../Data/train/images',exist_ok=True)
    os.makedirs('../Data/train/labels',exist_ok=True)
    os.makedirs('../Data/val',exist_ok=True)
    os.makedirs('../Data/val/images',exist_ok=True)
    os.makedirs('../Data/val/labels',exist_ok=True)

    f = open('./train.txt', 'r')
    lines= f.readlines()
    for line in lines:
        line = "/".join(line.split('/')[-5:]).strip()
        if (os.path.exists(line)):
            shutil.copy("./"+ line,"../Data/train/images")
            #os.system("cp ./"+ line + " ../VOC/images/train")
            
        line = line.replace('JPEGImages', 'labels')
        line = line.replace('jpg', 'txt')
        if (os.path.exists("./" + line)):
            shutil.copy("./"+ line,"../Data/train/labels")
            #os.system("cp ./"+ line + " ../VOC/labels/train")

    print(os.path.exists('val.txt'))
    f = open('./val.txt', 'r')
    lines = f.readlines()
    for line in lines:
        line = "/".join(line.split('/')[-5:]).strip()
        if (os.path.exists(line)):
            shutil.copy("./"+ line,"../Data/val/images")
            #os.system("cp ./"+ line + " ../VOC/images/val")
            
        line = line.replace('JPEGImages', 'labels')
        line = line.replace('jpg', 'txt')
        if (os.path.exists("./" + line)):
            shutil.copy("./"+ line,"../Data/val/labels")
            #os.system("cp ./"+ line + " ../VOC/labels/val")



    with open("../data.yaml",mode='w') as f:
        f.write("train: ./Data/train/images\n")
        f.write("val: ./Data/val/images\n")
        f.write("\n")
        #f.write("nc: {}\n".format(len(classes)))
        f.write("nc: 1\n")
        #クラス書き込み
        f.write("names: ")
        f.write("['"+"{}".format(class_name)+"']")
        #f.write("{}".format(classes))

    #仮置きのディレクトリを削除
    os.chdir('../')
    shutil.rmtree('./Delete')

if __name__ == "__main__":
    main()