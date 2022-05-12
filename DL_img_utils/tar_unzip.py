import os
import sys
import tarfile

# tarボールの解凍
def extract_tar_file(dirname, path):
    with tarfile.open(path, 'r:*') as tar:
        tar.extractall(dirname)

def main(wnid=-1):
    if wnid == -1:
        print("wnidが不正です。")
        return
    
    path="./DL_img_utils/Annotation_all/"+wnid+".tar.gz"
    if path.endswith('.tar.gz'):
        path = path.replace('\\','/')
        # tarボールを保存している一つ一つのディレクトリ抽出
        dirname, basename = os.path.split(path)
        extract_tar_file("./DL_img_utils", path)
    else:
        print("NONE Anotation File")

if __name__ == '__main__':
    main()
    