#アノテーション内の以上を確認
import glob
import os.path
import pathlib

def main(wnid=-1):
    if wnid == -1:
        return
    #アノテーション内のwnidと異なるデータを削除
    img_paths = os.listdir("./DL_img_utils/Annotation/"+wnid)
    for img_path in img_paths:
        if not(wnid in img_path):
            os.remove("./DL_img_utils/Annotation/"+wnid+"/"+img_path)




if __name__ == "__main__":
    main("n03793489")