import os
import shutil

#input_classname
class_name = input("クラス名:")

#DL_class_list
class_list = []

#事前にDLした画像を削除
if os.path.exists('./OID/Dataset'):
    shutil.rmtree('./OID/Dataset')
os.makedirs('./OID/Dataset',exist_ok=True)

if os.path.exists('./To_Yolo'):
    shutil.rmtree('./To_Yolo')

#一致するクラスの名前を取得
with open("./class_name.txt",'r', encoding='UTF-8') as f:
    read_data = f.readlines()
    for line in read_data:
        if line:
            line=line.replace("\n","")
            line=line.replace(" ","_")
            if class_name.upper() in line.upper():
                class_list.append(line)

print(class_list)
#見せるようのDL(5枚)
#for DL_class_name in class_list:
pre_command = "python OIDv4_ToolKit/main.py downloader --Dataset OIDv4_ToolKit/OID/csv_folder/  --classes Mouse --type_csv train --limit 5 -y".format(' '.join(class_list))
os.system(pre_command)
