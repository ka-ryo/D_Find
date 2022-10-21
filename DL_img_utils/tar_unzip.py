import os
import sys
import tarfile

# tarボールの解凍
def extract_tar_file(dirname, path):
    with tarfile.open(path, 'r:*') as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, dirname)

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
    