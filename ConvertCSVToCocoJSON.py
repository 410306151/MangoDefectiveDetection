import pandas as pds
import json

def buildImagesField(row):
    image = {}

    image["id"] = row.image_id
    image["file_name"] = row.file_name
    image["width"] = row.image_width
    image["height"] = row.image_height

    return image

def buildCategoriesField(row):
    category = {}

    category["supercategory"] = 'Mango'
    category["id"] = row.category_id
    category["name"] = row.category_label

    return category

def buildAnnotationField(row):
    annotation = {}

    area = row.bbox_width * row.bbox_height
    annotation["segmentation"] = []
    annotation["iscrowd"] = 0
    annotation["area"] = area
    annotation["image_id"] = row.image_id
    annotation["bbox"] = [row.bbox_X, row.bbox_Y, row.bbox_width, row.bbox_height]

    annotation["category_id"] = row.category_id
    annotation["id"] = row.annotation_id

    return annotation

def main():
    file = pds.read_csv("output_" + targetFile + ".csv")
    data_coco = {}
    images = []
    categories = []
    annotations = []

    # 寫入images欄位
    image = file.drop_duplicates(subset=['image_id']).sort_values(by='image_id')
    for row in image.itertuples():
        images.append(buildImagesField(row))

    # 寫入categories欄位
    category = file.drop_duplicates(subset=['category_id']).sort_values(by='category_id')
    for row in category.itertuples():
        categories.append(buildCategoriesField(row))

    # 寫入annotations欄位
    for row in file.itertuples():
        annotations.append(buildAnnotationField(row))

    data_coco["images"] = images
    data_coco["categories"] = categories
    data_coco["annotations"] = annotations

    json.dump(data_coco, open("test.json", "w"), indent=4)

if __name__ == '__main__':
    targetFile = "Train(500)"
    main()