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
from PIL.ImageFilter import Filter
from cmath import pi, sqrt
from math import trunc, atan2
from PIL.ImageOps import grayscale
from numpy.random import randint

images = []

def main(args, path):
    filepath = ''
    try:
        ops, longops = getopt.getopt(args, "p:")
    except getopt.GetoptError:
        print("usage: comparator.py -p imagepath")
        return
    for o,a in ops:
        if o=="-p":
            filepath=a
        else:
            print("usage: comparator.py -p imagepath")
            return         
    files = [f for f in listdir(filepath) if isfile(join(filepath,f))]
    for file in files:
        try:
            image = Image.open(join(filepath,file))
            images.append(image)
        except IOError:
            print("cannot convert", file)
    for i in range(len(images)):
        for j in range(i+1,len(images)):
            if (compare(i, j)) is True:
                print(files[i]+" "+files[j]+" are similar")        
    
def canny(image):
    imcopy = grayscale(image)
    imcopy1 = imcopy.filter(ImageFilter.GaussianBlur)
    imcopy2, gradients  = sobel(imcopy1)
    imcopy3 = nms(imcopy2, gradients)
    m = median(imcopy3)
    low = m*0.66
    high = m*1.33
    weakness = [[0 for i in range(image.size[1])] for j in range(image.size[0])]
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if imcopy3.getpixel((i,j)) < low:
                weakness[i][j]=0
                imcopy3.putpixel((i,j),0)
            elif imcopy3.getpixel((i,j)) < high:
                weakness[i][j]=1
            else:
                weakness[i][j]=2
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if weakness[i][j]==1:
                strong = False
                for i1 in range(-1,1):
                    for j1 in range(-1,1):
                        x = i+i1
                        x = x if x>0 else 0
                        x = x if x<image.size[0] else image.size[0]-1
                        y = j+j1
                        y = y if y>0 else 0
                        y = y if y<image.size[1] else image.size[1]-1
                        if weakness[x][y]==2:
                            strong = True
                            break
                        else:
                            imcopy3.putpixel((i,j),0)
                    if strong:
                        break
    return imcopy3

def sobel(image):
    imcopy = Image.new("L", image.size, 0)
    firstHalf = ImageFilter.Kernel((3,3),(1,0,-1,2,0,-2,1,0,-1),1)
    image1 = image.filter(firstHalf)
    secondHalf = ImageFilter.Kernel((3,3),(1,2,1,0,0,0,-1,-2,-1),1)
    image2 = image.filter(secondHalf)
    gradients = [[0 for i in range(image.size[1])] for j in range(image.size[0])]
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            x = image1.getpixel((i,j))
            y = image2.getpixel((i,j))
            val=trunc((x*x+y*y)/4)
            imcopy.putpixel((i,j),val)
            gradients[i][j]=atan2(y, x)
    return imcopy, gradients
    
def nms(image, gradients):
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            degree = trunc(gradients[i][j]/(pi/4))
            x = i-1 if i>0 else 0
            y = j-1 if j>0 else 0
            x = x if x<image.size[0]-2 else image.size[0]-3
            y = y if y<image.size[1]-2 else image.size[1]-3
            if degree==1:
                if image.getpixel((x,y+1))>image.getpixel((x+1,y+1)) or image.getpixel((x+2,y+1))>image.getpixel((x+1,y+1)):
                    image.putpixel((i,j),0)
            elif degree==2:
                if image.getpixel((x,y+2))>image.getpixel((x+1,y+1)) or image.getpixel((x+2,y+1))>image.getpixel((x+1,y+1)):
                    image.putpixel((i,j),0)
            elif degree==3:
                if image.getpixel((x+1,y))>image.getpixel((x+1,y+1)) or image.getpixel((x+1,y+2))>image.getpixel((x+1,y+1)):
                    image.putpixel((i,j),0)
            else:
                if image.getpixel((x,y))>image.getpixel((x+1,y+1)) or image.getpixel((x+2,y+2))>image.getpixel((x+1,y+1)):
                    image.putpixel((i,j),0)
    return image

def compare(im1, im2):
    mins = min(images[im1].size, images[im2].size)
    image1 = images[im1].resize(mins)
    image2 = images[im2].resize(mins)
    qr1 = list(image1.getdata())
    qr2 = list(image2.getdata())
    qrc = 0
    for i in range(60):
        for j in range(3):
            r = randint(0, min((len(qr1)-1,len(qr2)-1)))
            if qr1[r][j]>qr2[r][j]*1.4 or qr1[r][j]<qr2[r][j]*0.7:
                qrc+=1
        if qrc>90:
            return False
    temp1 = canny(image1.resize((300,300), Image.LANCZOS))
    temp2 = canny(image2.resize((300,300), Image.LANCZOS))
    total = 90000
    #tc -- toCompare
    tc1 = list(temp1.getdata())
    tc2 = list(temp2.getdata())
    comparable = 0
    col = image1.size[1]
    for i in range(image1.size[0]):
        for j in range(col):
            if tc1[col+j]*0.95<=tc2[col+j] and tc1[col+j]*1.05>=tc2[col+j]:
                comparable +=1
            if comparable>=0.9*total:
                return True
    return False

if __name__ == '__main__':
    main(sys.argv[1:], sys.argv[0][:sys.argv[0].index("\comparator.py")])