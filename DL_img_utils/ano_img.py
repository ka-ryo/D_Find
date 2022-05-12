#-------------------------------------------
# import
#-------------------------------------------
import os
import argparse
from DL_img_utils import downloader

#-------------------------------------------
# global
#-------------------------------------------


#-------------------------------------------
# functions
#-------------------------------------------
def arg_parser():
    #parser = argparse.ArgumentParser(description="Download images from ImageNet.")
    #parser.add_argument("wnid", type=str, help="download wnid")
    #parser.add_argument("-root", type=str, help="root dir", default=None)
    parser.add_argument("-limit", type=int, help="max save num", default=0)
    #parser.add_argument("-r", "--recursive", action='store_true', help="save recursive")
    #parser.add_argument("-v", "--verbose", action='store_true', help="show process message")

    return parser

def main(wnid,limit=0,verbose=True):
    #保存先
    root_dir =  "./DL_img_utils"

    api = downloader.ImageNet(root_dir)

    api.download(wnid, limit, verbose)
#-------------------------------------------
# main
#-------------------------------------------
if __name__ == '__main__':
    parser = arg_parser()
    args = parser.parse_args()
    main("n03941417")
