#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""hist matching."""

import cv2
import os
import numpy as np
import shutil


def main(class_name):
    #実験の為削除ではなく移動
    os.makedirs('./remove',exist_ok=True)
    os.makedirs('./remove/'+class_name,exist_ok=True)

    TARGET_FILE = './target_img/'+class_name+'.jpg'
    IMG_DIR = './trimming_obj/'+class_name+'/'

    IMG_SIZE = (252,252)

    #結果を記録する辞書式配列
    ret_dir ={}

    target_img_path =TARGET_FILE
    target_img = cv2.imread(target_img_path)
    target_img = cv2.resize(target_img, IMG_SIZE)
    target_hist_0 = cv2.calcHist([target_img], [0], None, [256], [0, 256])
    target_hist_1 = cv2.calcHist([target_img], [1], None, [256], [0, 256])
    target_hist_2 = cv2.calcHist([target_img], [2], None, [256], [0, 256])

    IMG_SIZE = (target_img.shape[0], target_img.shape[1])
    #print('TARGET_FILE: %s' % (TARGET_FILE))

    files = os.listdir(IMG_DIR)
    for file in files:
        sum = 0
        if file == '.DS_Store' or file == TARGET_FILE:
            continue

        comparing_img_path = IMG_DIR + file
        comparing_img = cv2.imread(comparing_img_path)
        comparing_img = cv2.resize(comparing_img, IMG_SIZE)
        comparing_hist_0 = cv2.calcHist([comparing_img], [0], None, [256], [0, 256])
        comparing_hist_1 = cv2.calcHist([comparing_img], [1], None, [256], [0, 256])
        comparing_hist_2 = cv2.calcHist([comparing_img], [2], None, [256], [0, 256])
        cv2.imwrite('./result/'+os.path.basename(comparing_img_path),comparing_img)


        result = []
        result.append(cv2.compareHist(target_hist_0, comparing_hist_0, cv2.HISTCMP_INTERSECT)/np.sum(target_hist_0))
        result.append(cv2.compareHist(target_hist_1, comparing_hist_1, cv2.HISTCMP_INTERSECT)/np.sum(target_hist_1))
        result.append(cv2.compareHist(target_hist_2, comparing_hist_2, cv2.HISTCMP_INTERSECT)/np.sum(target_hist_2))
        result.sort(reverse=True)

        # print(file, ret)
        ret_dir[os.path.splitext(file)[0]] = result[0]
        
        #if ret <= -0.1:
            #print("remove")
            #shutil.move(comparing_img_path,'./remove/'+class_name)
    return ret_dir

if __name__ == "__main__":
	print("=======REMOTE==========")
	main('remote')
	print("=======mouse==========")
	main('mouse')
	print("=======phone==========")
	main('phone')