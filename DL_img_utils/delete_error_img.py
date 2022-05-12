import cv2
import numpy as np
import os
import xml.etree.ElementTree as ET

def img_file_delete(path,wnid):
    #画像データの削除
    os.remove("./DL_img_utils/img/"+wnid+"/"+path)

    #アノテーションの削除
    os.remove("./DL_img_utils/Annotation/"+wnid+"/"+(path.replace('jpg','xml')))

def xml_file_delete(path,wnid):
    #画像データの削除
    os.remove("./DL_img_utils/Annotation/"+wnid+"/"+path)

    #アノテーションの削除
    os.remove("./DL_img_utils/img/"+wnid+"/"+(path.replace('xml','jpg')))

def main(wnid=-1):
    
    if wnid == -1:
        return

    #画像エラーチェック
    #判定する画像のパス
    img_paths = os.listdir("./DL_img_utils/img/"+wnid)

    #Error画像のサンプルのパス
    error_paths =os.listdir("./DL_img_utils/delete_img")

    for img_path in img_paths:
        im = cv2.imread("./DL_img_utils/img/"+wnid+"/"+img_path)
        
        if im is not None:
            for error_path in error_paths:
                error_im=cv2.imread("./DL_img_utils/delete_img/"+error_path)
                if (im.shape)==(error_im.shape):
                    if np.array_equal(im,error_im):
                        img_file_delete(img_path,wnid)
        else:
            img_file_delete(img_path,wnid)

    #アノテーションの画像サイズを確認
    input_file_paths = os.listdir('./DL_img_utils/Annotation/'+wnid)

    for input_file_path in input_file_paths:
        #xmlファイル取得
        
        root = ET.parse('./DL_img_utils/Annotation/'+wnid+'/'+input_file_path)
        im = cv2.imread("./DL_img_utils/img/"+wnid+"/"+os.path.splitext(os.path.basename(input_file_path))[0]+".jpg")
        #アノテーション内の画像サイズを取得
        width=0
        height=0
        for value in root.iter('size'):
            width=int(value.find("width").text)
            height=int(value.find("height").text)
        if im is not None:
            if (im.shape[1] != width) or (im.shape[0] != height):
                for element in root.iter('size'):
                    element.find("width").text=str(im.shape[1])
                    element.find("height").text=str(im.shape[0])
                root.write('./DL_img_utils/Annotation/'+wnid+'/'+input_file_path)


if __name__ == "__main__":
    main("n03793489")
    