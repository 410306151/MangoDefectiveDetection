import pandas as pds
import numpy as np
from PIL import Image

def findNan(row):
    # 因為每筆資料擁有的缺陷數量不一
    # 因此要找出每列資料沒有值的位置
    column = 0
    for j in range(file.shape[1]):
        if temp[j]:
            column = j
            break
    return column


targetFile = "Dev"
file = pds.read_csv("modified_" + targetFile + ".csv", encoding = "iso-8859-1")
images = []
categories = []
annotations = []
for i in range(file.shape[0]):
    temp = file.iloc[i].isnull()
    maxColmun = findNan(temp)
    #print("file name:" + file.iloc[i, 0] + ", file[" + str(i) + ", " + str(maxColmun) + "] is nan")
    imageName = file.iloc[i, 0]
    im = Image.open(targetFile + "/" + imageName)
    width, length = im.size
    print("image = " + imageName + ", width = " + str(width) + ", length = " + str(length))
    if i >= 5:
        break
