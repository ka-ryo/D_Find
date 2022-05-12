from PIL import Image
from matplotlib import pyplot as plt
#import imageio
import glob
import os.path
import pathlib
import xml.etree.ElementTree as ET
import random
import cv2
from DL_img_utils import txt_split
from DL_img_utils import xml_test
import sys
import imgaug as ia

def img_file_delete(path,class_name):
    #画像データの削除
    os.remove(path)
    #アノテーションの削除
    os.remove(class_name+"/Annotations/"+(os.path.basename(path).replace('jpg','xml')))

def main(class_name):

    dir = os.path.dirname("") # 実行ファイルの場所
    input_file_paths = glob.glob(dir+class_name+'/JPEGImages/*')

    for input_file_path in input_file_paths:
        img = cv2.imread(input_file_path)


        #xmlからバウンディングボックスの座標を取得
        xml_bb=xml_test.main(dir+class_name+"/Annotations/"+os.path.splitext(os.path.basename(input_file_path))[0])
        #バウンディングボックスを定義
        bb = ia.BoundingBoxesOnImage([ia.BoundingBox(x1=float(xml_bb[0]), y1=float(xml_bb[1]), x2=float(xml_bb[2]), y2=float(xml_bb[3])),], shape=img.shape)

        image_before = bb.draw_on_image(img, thickness=2, color=[255, 0,0])

        x1=bb.bounding_boxes[0].x1
        x2=bb.bounding_boxes[0].x2
        y1=bb.bounding_boxes[0].y1
        y2=bb.bounding_boxes[0].y2

        root = ET.parse(dir+class_name+"/Annotations/"+os.path.splitext(os.path.basename(input_file_path))[0]+'.xml')

        width=0
        height=0

        for value in root.iter('size'):
            width=int(value.find("width").text)
            height=int(value.find("height").text)

        

        if x1<0 or y1<0:
            print("=======")
            print("0以下ERROE")
            print(input_file_path)
            print("=======")
            img_file_delete(input_file_path,class_name)

        elif width < x2 or height <y2:
            print("=======")
            print("オーバーサイズERROE")
            print(input_file_path)
            print("=======")
            img_file_delete(input_file_path,class_name)

        elif x1 > x2 or y1 > y2:
            print("=======")
            print("大小関係ERROE")
            print(input_file_path)
            print("=======")
            img_file_delete(input_file_path,class_name)


        # 変換前後の画像を描画
        #fig = plt.figure()
        #fig.add_subplot(121).imshow(image_before)
        #plt.show()

        """
        image = np.array(Image.open('chick.jpg'))
        bboxes = [(20, 130, 280, 280), (0, 0, 100, 100)]
        fig, ax = plt.subplots()
        add_bboxes_to_image(ax, np.uint8(image), bboxes, ['chick', '?'])
        """

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("引数にクラス名がありません")
    class_name = sys.argv[1]
    main(class_name)    