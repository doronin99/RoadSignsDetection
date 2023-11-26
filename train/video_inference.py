import cv2
from ultralytics import YOLO
from tqdm import tqdm


model = YOLO('best_multi.pt')
frames_to_skip=2

cap = cv2.VideoCapture('Russian.mp4')

if not cap.isOpened():
    print("Ошибка: не удалось открыть видео")
    exit()
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_multi.mp4', fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

for _ in tqdm(range(total_frames), desc="Обработка видео"):
    success, frame = cap.read()
    if not success:
        break

    if cap.get(cv2.CAP_PROP_POS_FRAMES) % frames_to_skip == 0: 
        results = model(frame, verbose=False)
        annotated_frame = results[0].plot()
        out.write(annotated_frame)

out.release()
cap.release()
