import re
import json
import cv2 as cv
import os
import numpy as np

g = os.walk(r'E:\0')
for dir_path, dir_list, filename_list in g:
    for filename in filename_list:
        path = dir_path+os.sep+filename
        img = cv.imread(path)
        heigh = img.shape[0]
        width = img.shape[1]
        if width > heigh:
            width_half = int(width/2)
            img0 = img[0:heigh, width_half:width]
            img1 = img[0:heigh, 0:width_half]
            cv.imwrite(dir_path+os.sep+filename.split('.')[0]+'_00.jpg', img0)
            cv.imwrite(dir_path+os.sep+filename.split('.')[0]+'_01.jpg', img1)
            os.remove(dir_path+os.sep+filename)
