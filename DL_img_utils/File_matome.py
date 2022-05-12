from DL_img_utils import class_update
from DL_img_utils import txt_split
import sys
import os

def main(wnid,class_name,limit):
    class_update.main(wnid,class_name,limit)
    txt_split.main(class_name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("引数にクラス名がありません")
    class_name = sys.argv[1]
    paths = os.listdir("Annotation/")
    for path in paths:       
        main(path,class_name)