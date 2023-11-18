from ultralytics import YOLO
 
# Load the model.
model = YOLO('yolov8m.pt')
 
# Training.
results = model.train(
   data='trafic_sign_40.yaml',
   seed=42,
   imgsz=640,
   epochs=5,
   batch=8,
   optimizer='AdamW',
   name='yolov8m_40cls_5epochs')