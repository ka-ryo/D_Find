import glob
import os.path
import pathlib
import shutil
import random

def main(class_name): 
    #_train,_valを削除
    dir = './DL_img_utils/Data'
    input_file_paths = glob.glob(dir+'/Annotations')
    for input_file_path in input_file_paths:
        if not os.path.exists(dir+'/ImageSets'):
            os.mkdir(dir+'/ImageSets')

        if not os.path.exists(dir+'/ImageSets/Main'):
            os.mkdir(dir+'/ImageSets/Main')

        path_train = dir+'/ImageSets/Main/train.txt'
        path_val = dir+'/ImageSets/Main/val.txt'

        if  os.path.exists(path_train):
            os.remove(path_train)

        if  os.path.exists(path_val):
            os.remove(path_val)

        files = []
        for filename in os.listdir(input_file_path):
            if os.path.isfile(os.path.join(input_file_path, filename)):
                files.append(os.path.splitext(os.path.basename(filename))[0])

        random.shuffle(files)
        random.shuffle(files)

        train_list = files[:int(len(files)*0.7)]
        val_list = files[int(len(files)*0.7):]


        for a_train_list in train_list:
            with open(path_train, mode='a') as f:
                f.write(a_train_list+'\n')
                #f.write(a_train_list+' 1\n')

        for a_val_list in val_list:
            with open(path_val, mode='a') as f:
                f.write(a_val_list+'\n')
                #f.write(a_train_list+' 1\n')
   

if __name__ == "__main__":
    main("bed")