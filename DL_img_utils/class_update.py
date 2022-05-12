import os
import xml.etree.ElementTree as ET
import shutil

def main(wnid,class_name,limit):
    dir = './DL_img_utils/'
    input_file_paths = os.listdir(dir+'img/'+wnid)
    counter = 0
    for input_file_path in input_file_paths:
            #xmlファイル取得 
            root = ET.parse(dir+'Annotation/'+wnid+'/'+input_file_path.replace('jpg','xml'))
            #folderをクラス名に更新
            for element in root.iter('annotation'):
                element.find("folder").text=class_name
                element.find("filename").text=element.find("filename").text+".jpg"
            #クラス名をwnidから変更
            for element in root.iter('object'):
                if element.find("name").text == wnid:
                    element.find("name").text=class_name
            os.makedirs(dir+"Data",exist_ok=True)
            os.makedirs(dir+"Data"+"/Annotations",exist_ok=True)
            root.write(dir+"Data"+"/Annotations/"+input_file_path.replace('jpg','xml'))
            #画像をクラス名フォルダに移動
            if not os.path.exists(dir+"Data"+"/JPEGImages"):
                os.mkdir(dir+"Data"+"/JPEGImages")
            if os.path.exists(dir+"Data"+"/JPEGImages/"+input_file_path):
                os.remove(dir+"Data"+"/JPEGImages/"+input_file_path)
            shutil.copy2(dir+"img/"+wnid+"/"+input_file_path,dir+"Data"+"/JPEGImages/"+input_file_path)
            if limit != 0 and limit <= counter:
                break
            counter+=1


if __name__ == "__main__":
    main("n04188179","bed")