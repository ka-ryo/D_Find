import cv2
import os
import shutil

def main(class_name):
	#実験の為削除ではなく移動
	os.makedirs('./remove',exist_ok=True)
	os.makedirs('./remove/'+class_name,exist_ok=True)

	TARGET_FILE = './target_img/'+class_name+'.jpg'
	IMG_DIR = './trimming_obj/'+class_name+'/'

	TARGET_SIZE = (252,252)

	#結果を記録する辞書式配列
	ret_dir ={}

	#bf = cv2.BFMatcher(cv2.NORM_HAMMING)
	bf = cv2.BFMatcher(cv2.NORM_HAMMING)
	# 特徴点算出のアルゴリズムを決定(コメントアウトで調整して切り替え)
	# detector = cv2.ORB_create()
	detector = cv2.AKAZE_create()

	tage_img = cv2.imread(TARGET_FILE,cv2.IMREAD_GRAYSCALE)
	tage_img = cv2.resize(tage_img, (TARGET_SIZE[0],TARGET_SIZE[1]))
	(target_kp, target_des) =detector.detectAndCompute(tage_img, None)

	print('TARGET_FILE: %s' % (TARGET_FILE))

	files = os.listdir(IMG_DIR)
	for file in files:
		if file == '.DS_Store' or file == TARGET_FILE:
			continue

		comparing_img_path = IMG_DIR + file
		try:
			comp_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
			comp_img = cv2.resize(comp_img, (TARGET_SIZE[0],TARGET_SIZE[1]))
			(comparing_kp, comparing_des) = detector.detectAndCompute(comp_img, None)

			#画像同士をマッチング
			matches = bf.match(target_des, comparing_des)
			matches = sorted(matches, key = lambda x:x.distance)

			dist = [m.distance for m in matches]
			if len(dist) != 0:
				#類似度を計算する
				ret = sum(dist) / len(dist)
			else:
				print("len(dist) Error")
				ret = 165
			#print(file, ret)

		except cv2.error:
			ret = 165

		ret_dir[os.path.splitext(file)[0]] = ret

		"""
		if ret >= 200:
			print("remove")
			#shutil.move(comparing_img_path,'./remove/'+class_name)
		"""
	return ret_dir


def calc_kp_and_des(img_path, detector,size):
	"""
		特徴点と識別子を計算する
		:param str img_path: イメージのディレクトリパス
		:param detector: 算出の際のアルゴリズム
		:return: keypoints
		:return: descriptor
	"""
	IMG_SIZE = (size[0], size[1])
	img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
	img = cv2.resize(img, IMG_SIZE)
	return detector.detectAndCompute(img, None)


if __name__ == '__main__':
	print("=======REMOTE==========")
	main('remote')
	print("=======mouse==========")
	main('mouse')
	print("=======phone==========")
	main('phone')