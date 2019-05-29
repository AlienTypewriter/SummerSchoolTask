'''
Created on 29 мая 2019 г.

@author: Judge
'''
from __future__ import print_function
import sys
from os import listdir
from os.path import isfile, join
from PIL import Image, ImageFilter
from numpy import median
import getopt
from ctypes.wintypes import RGB

def main(args):
    filepath = ''
    try:
        ops = getopt.getopt(args, "p:")
    except getopt.GetoptError:
        print("usage: comparator.py -p imagepath")
        return
    try:
        for o, a in ops:
            if o=="-p":
                filepath=a
            else:
                print("usage: comparator.py -p imagepath")
                return
    except ValueError:
        print("usage: comparator.py -p imagepath")
        return                    
    images = []
    files = [f for f in listdir(filepath) if isfile(join(filepath,f))]
    for file in files:
        try:
            images+=Image.open(file)
        except IOError:
            print("cannot convert", file)
    print("Nah");
    
def canny(image):
    imcopy = image
    imcopy1 = imcopy.filter(ImageFilter.GaussianBlur)
    imcopy2, gradients  = sobel(imcopy1)
    imcopy3 = nms(imcopy2, gradients)
    m = median(imcopy3)
    low = m*0.66
    high = m*1.33
    imcopy4 = Image.new(RGB, image.size, 0)
    weakness = [[]]
    for i in range(image.size[0]):
        for j in range(image.size[1]):
             

def sobel(image):
    pass

def nms(image, gradients):
    pass

if __name__ == '__main__':
    main(sys.argv[:1])