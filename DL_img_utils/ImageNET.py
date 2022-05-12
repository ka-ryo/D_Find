from DL_img_utils import tar_unzip
from DL_img_utils import ano_img
from DL_img_utils import Annotation_folder_check
from DL_img_utils import delete_error_img
from DL_img_utils import class_update
from DL_img_utils import delete_error_ano
import os
import argparse
from DL_img_utils import File_matome
from DL_img_utils import trans_YOLO_Data
import shutil

def Img_DL(class_name,limit,mode):
  #クラスのリストを読み込む
  #fileobj = open("./DL_img_utils/TEST_LIST.txt", "r", encoding="utf_8")
  fileobj = open("./DL_img_utils/ANO_LIST.txt", "r", encoding="utf_8")
  exists_file = 0
  wnid_list=[]

  while True:
    line = fileobj.readline()
    tmp_class_list = line.split()
    class_list = []

    #,をけす処理
    for s in tmp_class_list:
      if ',' in s:
        text = s.replace(',', '')
        class_list.append(text)
      else:
        class_list.append(s)

    #class_name = class_name + " "
    
    #print(class_name,"//")
    if line:

      if  class_name in class_list:
          wnid=line.split()[0]
          if os.path.exists("./DL_img_utils/Annotation_all/"+wnid+".tar.gz"):
              exists_file = 1
              wnid_list.append(wnid)
              print(wnid)
              #Anotationがはいってる圧縮ファイルを解凍
              tar_unzip.main(wnid)
              #アノテーションファイル内に不正なファイルがあるかを確認
              Annotation_folder_check.main(wnid)
              #画像をDL
              ano_img.main(wnid,limit=limit,verbose=False)
              #エラー画像を削除
              delete_error_img.main(wnid)
              #アノテーションのエラーを削除
              delete_error_ano.main(wnid)
    else:
      break
  return exists_file

#引数のクラスIDを参照して画像をDLする
def ALL_DL(wnid,class_name):
  if os.path.exists("./DL_img_utils/Annotation_all/"+wnid+".tar.gz"):
    #アノテーションファイル内に不正なファイルがあるかを確認
    Annotation_folder_check.main(wnid)
    #画像をDL
    ano_img.main(wnid,limit=500,verbose=False)
    #エラー画像を削除
    delete_error_img.main(wnid)
    #アノテーションのエラーを削除
    delete_error_ano.main(wnid)
      
  #ファイルをまとめる
  print("===========================")
  print("===ファイルを整理しています==")
  print("===========================")
  File_matome.main(wnid,class_name,limit=500)

  """
  fileobj = open("./DL_img_utils/Class.txt", "r", encoding="utf_8")
  #重複確認
  Duplicate = False
  while True:
      line = fileobj.readline()
      if line:
        if line == class_name:
          Duplicate = True     
      else:
        break
  fileobj.close()

  #クラスリストに追加書き込み
  if Duplicate == False:     
    with open("./DL_img_utils/Class.txt", mode='a') as f:
      print("ImageNet_line90:class_name:",class_name)
      f.write('{}\n'.format(class_name))
  """
    
  trans_YOLO_Data.main(class_name)
      

def main():
  #画像のDL数を設定
  limit = opt.limit
  #クラスのリストを読み込む
  fileobj = open("./DL_img_utils/TEST_LIST.txt", "r", encoding="utf_8")
  #クラス名を取得
  class_name=input("クラス名:")
  #class_name="remote"
  #クラス名が一致するwnidを保存するリスト
  #指定されたクラスの画像が存在したかを確認するフラグ
  exists_file = 0
  wnid_list=[]
  while True:
    line = fileobj.readline()
    class_list = line.split()
    if line:
      if  class_name in class_list:
          wnid=line.split()[0]
          if os.path.exists("./DL_img_utils/Annotation_all/"+wnid+".tar.gz"):
              exists_file = 1
              wnid_list.append(wnid)
              print(wnid)
              #Anotationがはいってる圧縮ファイルを解凍
              tar_unzip.main(wnid)
              #アノテーションファイル内に不正なファイルがあるかを確認
              Annotation_folder_check.main(wnid)
              #画像をDL
              ano_img.main(wnid,verbose=False)
              #エラー画像を削除
              delete_error_img.main(wnid)
              #アノテーションのエラーを削除
              delete_error_ano.main(wnid)
    else:
      break
  #ファイルをまとめる
  if opt.mode == 0 and exists_file == 1:
    print("===========================")
    print("===ファイルを整理しています==")
    print("===========================")
    #File_matome.main(wnid_list[0],class_name,0)

    with open("./DL_img_utils/Class.txt", mode='a') as f:
      f.write('{}\n'.format(class_name))

    trans_YOLO_Data.main()

    #不要なファイルを削除
    #shutil.rmtree('./DL_img_utils/Annotations')
    #shutil.rmtree('./DL_img_utils/img')

  elif exists_file == 0:
    print("指定された画像のクラスはまだ実装されていません")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=0, help='Number DL imags')
    parser.add_argument('--mode', type=int, default=0, help='0 is DL.1 is 試し')
    opt = parser.parse_args()
    main()


