from ultralytics import YOLO

model = YOLO("yolov8s.pt")

results = model.train(
    data="data.yaml",
    seed=42,
    imgsz=640,
    epochs=100,
    batch=8,
    optimizer="AdamW",
    name="yolov8s_24classes_2",
    mosaic=0,
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=10.0,
    scale=0.7,
)
