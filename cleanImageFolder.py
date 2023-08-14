import glob
import os


def cleanImgFolder():
    store_all_img = glob.glob("images/*.png")
    for i in store_all_img:
        os.remove(i)
