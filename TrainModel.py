from detectron2.data.datasets import register_coco_instances
from detectron2.data import MetadataCatalog, DatasetCatalog
import random
import cv2
from detectron2.utils.visualizer import Visualizer
from detectron2.engine import DefaultTrainer, DefaultPredictor
from detectron2.config import get_cfg
import os
from detectron2 import model_zoo
from detectron2.utils.visualizer import ColorMode

# 註冊資料集到detectron2
register_coco_instances("my_mango_dataset", {}, "./images_train/Train.json", "./images_train")
register_coco_instances("my_mango_test_dataset", {}, "./images_validate/Dev(500).json", "./images_validate")


# 訓練集
mango_metadata = MetadataCatalog.get("my_mango_dataset")
dataset_dicts = DatasetCatalog.get("my_mango_dataset")
# 測試集
mango_test_metadata = MetadataCatalog.get("my_mango_test_dataset")
dataset_test_dicts = DatasetCatalog.get("my_mango_test_dataset")

# 看訓練圖的邊框
def showImage():
    # for d in random.sample(dataset_dicts, 20):
    for i in range(124, 125):
        d = dataset_dicts[i]
        img = cv2.imread(d["file_name"])
        visualizer = Visualizer(img[:, :, ::-1], metadata=mango_metadata, scale=0.5)
        vis = visualizer.draw_dataset_dict(d)
        cv2.imshow(d["file_name"], vis.get_image()[:, :, ::-1])
        cv2.waitKey(0)

# 訓練Model
def trainModel():
    cfg = get_cfg()
    cfg.merge_from_file(
        "/home/ad/detectron2/detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    ) # 從Detectron2拿Mask RCNN的模型
    cfg.DATASETS.TRAIN = ("my_mango_dataset",) # 拿來Train的資料集
    cfg.DATASETS.TEST = ()
    cfg.DATALOADER.NUM_WORKERS = 2 # 2個workers取圖片
#    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")  # 從網路上拿Pretrained的權重
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth") # 讀取已訓練過的權重
    cfg.SOLVER.IMS_PER_BATCH = 2 # 每個 iteration 看兩張圖片
    cfg.SOLVER.BASE_LR = 0.02 # learning rate
    cfg.SOLVER.MAX_ITER = 12884 * 5  # number of iteration: 1 Epoch = MAX_ITER * BATCH_SIZE / TOTAL_NUM_IMAGES
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 5  # 5 classes (著色不佳, 炭疽病, 乳汁吸附, 機械傷害, 黑斑病)

    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    trainer = DefaultTrainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.train()

# 驗證模型
def validateModel():
    cfg = get_cfg()
    cfg.merge_from_file(
        "/home/ad/detectron2/detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"
    )
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.75   # set the testing threshold for this model
    cfg.MODEL.ROI_HEADS.NMS_THRESH_TEST  = 0.1 # 設定Non-Maximum Suppression的IoU門檻
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 5  # 5 classes (著色不佳, 炭疽病, 乳汁吸附, 機械傷害, 黑斑病)
    cfg.DATASETS.TEST = ("my_mango_test_dataset", )
    predictor = DefaultPredictor(cfg)
    for i in range(len(dataset_test_dicts)):
    # for i in range(487, 488):
        d = dataset_test_dicts[i]
        filename = d["file_name"].split('/')[-1]
        im = cv2.imread(d["file_name"])
        
        outputs = predictor(im)
        v = Visualizer(im[:, :, ::-1],
                       metadata=mango_test_metadata,
                       scale=0.5, 
                       instance_mode=ColorMode.IMAGE_BW   # remove the colors of unsegmented pixels
        )
        v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        
        cv2.imwrite("./predict_validate/train_x10/" + filename, v.get_image()[:, :, ::-1])
        # cv2.imwrite(filename, v.get_image()[:, :, ::-1])
        # cv2.imshow(d["file_name"], v.get_image()[:, :, ::-1])
        # cv2.waitKey(0)
      
# showImage()
# trainModel()
validateModel()
