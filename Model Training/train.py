from ultralytics import YOLO

model = YOLO('yolov8n-cls.pt')

model.train(data="Dataset", epochs=10)

results = model.val()