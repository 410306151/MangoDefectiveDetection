import pandas as pds
import numpy as np
from PIL import Image

def findNan(row, len):
    # 因為每筆資料擁有的缺陷數量不一
    # 因此要找出每列資料沒有值的位置
    column = 0
    for i in range(len):
        if row[i]:
            column = i
            break

    return column

def getImageSize(imageName):
    # 因為csv檔沒有給每張圖的大小，需要自己抓出圖片的size
    im = Image.open(targetFile + "/" + imageName)
    width, height = im.size

    return width, height

def buildImagesField(imageID, imageName, width, height):
    image = {}
    image["id"] = imageID
    image["file_name"] = imageName
    image["width"] = width
    image["height"] = height

    return image

def main():
    file = pds.read_csv("modified_" + targetFile + ".csv", encoding = "iso-8859-1")
    images = []
    categories = []
    annotations = []
    for i in range(file.shape[0]):
        # 取得該筆資料有多少個column，後面用來對應特徵欄位
        temp = file.iloc[i].isnull()
        maxColumn = findNan(temp, file.shape[1])
        # print("file name:" + file.iloc[i, 0] + ", file[" + str(i) + ", " + str(maxColmun) + "] is nan")

        # 取得檔案名稱、檔案ID、圖片大小
        imageName = file.loc[i, 'Filename']
        imageID = file.loc[i, 'FileID']
        width, height = getImageSize(imageName)

        # Next step: 填寫dataset的images欄位
        print(buildImagesField(imageID, imageName, width, height))

if __name__ == '__main__':
    targetFile = "Dev"
    main()