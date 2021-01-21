import pandas as pds
from PIL import Image

def findNan(row, len):
    # 因為每筆資料擁有的缺陷數量不一
    # 因此要找出每列資料沒有值的位置
    column = 0
    for i in range(len):
        if row[i]:
            column = i
            break
    if i == len - 1:
        column = i + 1

    return column

def getImageSize(imageName):
    # 因為csv檔沒有給每張圖的大小，需要自己抓出圖片的size
    im = Image.open(targetFile + "/" + imageName)
    width, height = im.size

    return width, height

targetFile = "Train"
file = pds.read_csv("modified_" + targetFile + ".csv", dtype = {"file_id": int, "file_name": str})

columnNames = ["image_id", "file_name", "image_width", "image_height", "category_id", "category_label", "bbox_X", "bbox_Y", "bbox_width", "bbox_height"]

# label 1: 著色不佳、 2: 炭疽病、 3: 乳汁吸附、 4: 機械傷害、 5: 黑斑病
categories_label = ["Bad color", "Anthrax", "Absorption", "Machine damage", "Black spot"]
imageDF = pds.DataFrame(columns = columnNames)
x = -1
y = -1
bboxwidth = -1
bboxheight = -1
categoryID = -1
for i in range(file.shape[0]):
    rowContent = {}
    # # 取得檔案名稱、檔案ID、圖片大小
    rowContent["image_id"] = file.loc[i, 'FileID']
    imageName = file.loc[i, 'Filename']
    rowContent["file_name"] = imageName
    width, height = getImageSize(imageName)
    rowContent["image_width"] = width
    rowContent["image_height"] = height

    # 取得該筆資料有多少個column，後面用來對應特徵欄位
    temp = file.iloc[i].isnull()
    maxColumn = findNan(temp, file.shape[1])
    # 開始做缺陷資料擷取
    row = file.iloc[i]
    for j in range(2, maxColumn):
        if ((j - 2) % 5) == 0:
            bboxX = row[j]
        elif ((j - 2) % 5) == 1:
            bboxY = row[j]
        elif ((j - 2) % 5) == 2:
            bboxWidth = row[j]
        elif ((j - 2) % 5) == 3:
            bboxHeight = row[j]
        elif ((j - 2) % 5) == 4:
            if row[j] == "defective1":
                rowContent["category_id"] = 1
                rowContent["category_label"] = categories_label[0]
            elif row[j] == "defective2":
                rowContent["category_id"] = 2
                rowContent["category_label"] = categories_label[1]
            elif row[j] == "defective3":
                rowContent["category_id"] = 3
                rowContent["category_label"] = categories_label[2]
            elif row[j] == "defective4":
                rowContent["category_id"] = 4
                rowContent["category_label"] = categories_label[3]
            elif row[j] == "defective5":
                rowContent["category_id"] = 5
                rowContent["category_label"] = categories_label[4]
            rowContent["bbox_X"] = bboxX
            rowContent["bbox_Y"] = bboxY
            rowContent["bbox_width"] = bboxWidth
            rowContent["bbox_height"] = bboxHeight
            imageDF = imageDF.append(rowContent, ignore_index = True)

imageDF.to_csv("output_" + targetFile + ".csv")