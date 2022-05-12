import os 
import shutil
import glob

def main(class_name):


    os.makedirs("./Data",exist_ok=True)
    os.makedirs("./Data/train",exist_ok=True)
    os.makedirs("./Data/train/images",exist_ok=True)
    os.makedirs("./Data/train/labels",exist_ok=True)
    os.makedirs("./Data/val",exist_ok=True)
    os.makedirs("./Data/val/images",exist_ok=True)
    os.makedirs("./Data/val/labels",exist_ok=True)
    
    OID_file_dir = "./OIDv4_ToolKit"

    #改行削除
    line = class_name
    #画像データの移動
    #train
    img_move(OID_file_dir,"train",line)
    #val
    img_move(OID_file_dir,"validation",line)
    #test
    img_move(OID_file_dir,"test",line)
    
    #labelの移動
    #train
    label_move(OID_file_dir,"train",line)
    #val
    label_move(OID_file_dir,"validation",line)
    #test
    label_move(OID_file_dir,"test",line)

def label_move(OID_file_dir,train_or_val,class_name):
    print("labelPath=>:",OID_file_dir+"/To_Yolo/"+train_or_val+"/"+class_name+"/*.txt")
    label_file_paths = glob.glob(OID_file_dir+"/To_Yolo/"+train_or_val+"/"+class_name+"/*.txt")
    for label_file_path in label_file_paths:
        if train_or_val == "test" or train_or_val == "validation":
            if not os.path.exists('./Data/val/labels/{}'.format(os.path.basename(label_file_path))):
                shutil.move(label_file_path,'./Data/val/labels/')
            else:
                #追加書き込みの処理追加予定
                pass
        else:
            if not os.path.exists('./Data/train/labels/{}'.format(os.path.basename(label_file_path))):
                shutil.move(label_file_path,'./Data/'+train_or_val+'/labels/')
            else:
                #追加書き込みの処理追加予定
                pass

                

def img_move(OID_file_dir,train_or_val,class_name):
    img_file_paths =glob.glob(OID_file_dir+"/OID/Dataset/"+train_or_val+"/"+class_name+"/*.jpg")
    for img_file_path in img_file_paths:
        if train_or_val == "test" or train_or_val == "validation":
            if not os.path.exists('./Data/val/images/{}'.format(os.path.basename(img_file_path))):
                shutil.move(img_file_path,'./Data/val/images/')
        else:
            shutil.move(img_file_path,'./Data/'+train_or_val+'/images/')
               

if __name__ == "__main__":
    main()

