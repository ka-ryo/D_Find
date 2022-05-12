import cv2
import os
import random
from plot_img_utils import color
from plot_img_utils import AKAZE
import shutil

#============================================#
#現状決め打ちで数値を取っているので変更する必要あり
#最後に検出されたものに変更12/20
#============================================#
def comb_movie(count,out_path,class_name="remote"):
    
    #合成するビデオのパス
    movie_files = []

    #output_path
    out_path = out_path+"{}.mp4".format(class_name)

    if count == 0 or count==1:
        for i in range(0,3):
            if os.path.exists("./video/video_{}.mp4".format(i)):
                movie_files.append("./video/video_{}.mp4".format(i))
    else:
        if os.path.exists("./video/video_{}.mp4".format(count-1)):
            movie_files.append("./video/video_{}.mp4".format(count-1)) 

        if os.path.exists("./video/video_{}.mp4".format(count)):
            movie_files.append("./video/video_{}.mp4".format(count)) 

        if os.path.exists("./video/video_{}.mp4".format(count+1)):
            movie_files.append("./video/video_{}.mp4".format(count+1)) 
    
    # 形式はmp4
    #fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    fourcc = cv2.VideoWriter_fourcc('H','2','6','4')    

    # 動画情報の取得
    movie = cv2.VideoCapture(movie_files[0])
    fps = movie.get(cv2.CAP_PROP_FPS)
    height = movie.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = movie.get(cv2.CAP_PROP_FRAME_WIDTH)


    # 出力先のファイルを開く
    out = cv2.VideoWriter(out_path, int(fourcc), fps, (int(width), int(height)))


    for movies in (movie_files):
        #print(movies)
        # 動画ファイルの読み込み，引数はビデオファイルのパス
        movie = cv2.VideoCapture(movies)

        if movie.isOpened() == True: # 正常に動画ファイルを読み込めたか確認
            ret, frame = movie.read() # read():1コマ分のキャプチャ画像データを読み込む
        else:
            ret = False

        while ret:
            # 読み込んだフレームを書き込み
            out.write(frame)
            # 次のフレーム読み込み
            ret, frame = movie.read()


def main(class_name):

    if os.path.exists('./Object_box_save/'+class_name+'.txt'):

        result_color=color.main(class_name)
        result_AKAZE=AKAZE.main(class_name)

        img_path = './trimming_obj/'+class_name

        #選別した残りを記録
        img_list=[]

        #選別
        for  key in result_AKAZE:
            ret_AKAZE = int (result_AKAZE[key])
            ret_color = result_color[key]
            print(key,":",ret_AKAZE, ret_color)
            if ret_AKAZE >=180:
                shutil.move(os.path.join(img_path,'{}.jpg'.format(key)),'./remove/'+class_name)
            elif ret_AKAZE >=170 :
                if ret_color < 0.5:
                    shutil.move(os.path.join(img_path,'{}.jpg'.format(key)),'./remove/'+class_name)            
            elif ret_AKAZE >= 160:
                if ret_color < 0.45:
                    shutil.move(os.path.join(img_path,'{}.jpg'.format(key)),'./remove/'+class_name) 
            else:
                if ret_color <0.4:
                    shutil.move(os.path.join(img_path,'{}.jpg'.format(key)),'./remove/'+class_name) 
                


        #ヒストグラムとAKAZEでふるいにかけた残り
        img_list = os.listdir('./trimming_obj/'+class_name)
        img_list = [int(os.path.splitext(os.path.basename(n))[0]) for n in img_list]
        print(img_list)

        if len(img_list) != 0:

            #部屋の画像を読み込む
            img = cv2.imread("./room.jpg")
            #objのリスト
            obj_num_list = []
            #objの辞書配列に
            obj_dict = {}
            #辞書配列に変換
            with open("Object_box_save/{}.txt".format(class_name)) as f:
                for Line in f:
                    Line = Line.replace("\n","")
                    split_line = Line.split(" ")
                    obj_dict[int(split_line[0])] = "{} {} {} {}".format(split_line[1],split_line[2],split_line[3],split_line[4])
                    obj_num_list.append(int(split_line[0]))

            obj_num_list.sort()

            #handの辞書型
            hand_dict = {}
            #カウンター
            counter = 0
            #handの辞書変換
            with open("hand_box_save/hand.txt") as f:
                for Line in f:
                    Line = Line.replace("\n","")
                    split_line = Line.split(" ")
                    #minx,miny,maxx,maxy,time
                    hand_dict[counter] = "{} {} {} {} {}".format(split_line[0],split_line[1],split_line[2],split_line[3],split_line[4])
                    counter+=1

            
            #ランダムで一つピックアップ
            #plot_data=random.choice(obj_num_list)
            img_list.sort()
            print("plot_img 127:choice=>",img_list[-1])
            plot_data=img_list[-1]

            #str
            obj_box = obj_dict[plot_data].split(" ")
            hund_box = hand_dict[plot_data].split(" ")
            #str -> int
            obj_box = [int(n) for n in obj_box]
            hund_box = [int(hund_box[n]) for n in range(4)]
            #print(hund_box)
            #print(obj_box)
            #縦・横の比を計算

            height_ratio = (int(hund_box[3]) - int(hund_box[1]))/480
            #横
            width_ratio = (int(hund_box[2]) - int(hund_box[0]))/640

            #objのbox
            #c1,c2 = (int(obj_box[0]*height_ratio),int(obj_box[1]*width_ratio)),(int(obj_box[2]*height_ratio),int(obj_box[3]*width_ratio))
            c1,c2 = (((obj_box[0]+hund_box[0]),(obj_box[1]+hund_box[1])),((hund_box[2]- ((hund_box[2]-hund_box[0])-obj_box[2])),(hund_box[3]- ((hund_box[3]-hund_box[1])-obj_box[3]))))
            #print(c1)
            #print(c2)

            

            #書き込み
            img=cv2.rectangle(img, c1, c2, color=(0,255,0), thickness=10, lineType=cv2.LINE_AA)
            #cv2.circle(img, (c1[0],c1[1]), 10, (255,0,0), thickness=-1, lineType=cv2.LINE_8, shift=0)
            #cv2.circle(img, (c2[0],c2[1]), 10, (255,0,0), thickness=-1, lineType=cv2.LINE_8, shift=0)
            cv2.imwrite('web/img/{}.jpg'.format(class_name),img)

            #動画の保存
            detect_time = hand_dict[plot_data].split(" ")[4]
            print(detect_time)

            #動画を確認
            save_vido = int(float(detect_time)/60)-1
            print(save_vido)

            #動画を連結
            comb_movie(save_vido,"./web/video/",class_name)


if __name__ == "__main__":
    main("mouse")
    main("remote")
    main("phone")

#全ての結果のプロットを行う場合
"""
for num in obj_num_list:
    img = cv2.imread("./room.jpg")
    #str
    obj_box = obj_dict[num].split(" ")
    hund_box = hand_dict[num].split(" ")
    #str -> int
    obj_box = [int(n) for n in obj_box]
    hund_box = [int(n) for n in hund_box]
    #print(hund_box)
    #print(obj_box)
    #縦・横の比を計算

    height_ratio = (int(hund_box[3]) - int(hund_box[1]))/480
    #横
    width_ratio = (int(hund_box[2]) - int(hund_box[0]))/640

    #objのbox
    #c1,c2 = (int(obj_box[0]*height_ratio),int(obj_box[1]*width_ratio)),(int(obj_box[2]*height_ratio),int(obj_box[3]*width_ratio))
    c1,c2 = (((obj_box[0]+hund_box[0]),(obj_box[1]+hund_box[1])),((hund_box[2]- ((hund_box[2]-hund_box[0])-obj_box[2])),(hund_box[3]- ((hund_box[3]-hund_box[1])-obj_box[3]))))
    #print(c1)
    #print(c2)

    

    #書き込み
    img=cv2.rectangle(img, c1, c2, color=(0,255,0), thickness=1, lineType=cv2.LINE_AA)
    #cv2.circle(img, (c1[0],c1[1]), 10, (255,0,0), thickness=-1, lineType=cv2.LINE_8, shift=0)
    #cv2.circle(img, (c2[0],c2[1]), 10, (255,0,0), thickness=-1, lineType=cv2.LINE_8, shift=0)
    cv2.imwrite('out/output{}.jpg'.format(num),img)
"""