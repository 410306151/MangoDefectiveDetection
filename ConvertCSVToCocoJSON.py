import pandas as pds
import numpy as np

def buildImagesField(imageID, imageName, width, height):
    image = {}

    image["id"] = imageID
    image["file_name"] = imageName
    image["width"] = width
    image["height"] = height

    return image

def buildCategoriesField(categoryName, categoryID):
    category = {}

    category["supercategory"] = 'Mango'
    category["id"] = categoryID
    category["name"] = categoryName

    return category

def buildAnnotationField(row, maxColumn):
    annotations = []
    annotation = {}

    # 第一個欄位是圖片ID
    annotation["image_id"] = row[0]

    for i in range(2, maxColumn):
        print(str(i) + ": " + str(row[i]))
        annotations.append(row[i])
    # annotation["segmentation"] = []
    # annotation["iscrowd"] = 0
    # annotation["area"] = area
    #
    # annotation["bbox"] = [row.xmin, row.ymin, row.xmax -row.xmin,row.ymax-row.ymin ]
    #
    # annotation["category_id"] = row.categoryid
    # annotation["id"] = row.annid
    return annotation

def main():
    # label 1: 著色不佳、 2: 炭疽病、 3: 乳汁吸附、 4: 機械傷害、 5: 黑斑病
    categories_label = {"Bad color": 1, "Anthrax": 2, "Absorption": 3, "Machine damage": 4, "Black spot": 5}
    file = pds.read_csv("modified_" + targetFile + ".csv", encoding = "iso-8859-1")
    images = []
    categories = []
    annotations = []

    # 把categories_label定義的label寫進dataset的categories欄位
    for name in categories_label:
        categories.append(buildCategoriesField(name, categories_label[name]))

    for i in range(file.shape[0]):
        # print("file name:" + file.iloc[i, 0] + ", file[" + str(i) + ", " + str(maxColmun) + "] is nan")

        # # 取得檔案名稱、檔案ID、圖片大小
        # imageName = file.loc[i, 'Filename']
        # imageID = file.loc[i, 'FileID']
        # width, height = getImageSize(imageName)
        #
        # # 填寫dataset的images欄位
        # images.append(buildImagesField(imageID, imageName, width, height))

        temp = file.iloc[i]
        # buildAnnotationField(temp, maxColumn, len(annotations))
        testAll = []
        for k in range(3):
            testTemp = []
            for j in range(10):
                testTemp.append(j)
            testAll.append(testTemp)
        annotations.append(testAll)

        if i > 1:
            break
    print(annotations)

if __name__ == '__main__':
    targetFile = "Dev"
    main()