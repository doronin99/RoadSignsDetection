import json
import os
from ultralytics import YOLO
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
import cv2
from tqdm import tqdm
import shutil


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    global model
    model = YOLO('../models/best8class60epochs_renamed.pt')

    global input_dir
    input_dir = "../input"
    os.makedirs(os.path.join(input_dir), exist_ok=True)
    
    global output_dir
    output_dir = "../output"
    os.makedirs(os.path.join(output_dir), exist_ok=True)

    global frames_to_skip
    frames_to_skip = 1

    yield
    
    shutil.rmtree(input_dir)
    shutil.rmtree(output_dir)


app = FastAPI(lifespan=lifespan)

@app.post("/predict")
async def predict(request: Request):
    """Predict"""
    request = json.loads((await request.body()).decode())

    video_name = request["video_name"]
    input_video_path = os.path.join(input_dir, video_name)
    output_video_path = os.path.join(output_dir, video_name)

    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
            headers = {"success": str(False)}
            raise Exception(
                "Can't open video file"
            )
    else:
         headers = {"success": str(True)}

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc('a','v','c','1'), fps, (int(cap.get(3)), int(cap.get(4))))

    for _ in tqdm(range(total_frames), desc="Processing video"):
        success, frame = cap.read()
        if not success:
            break
        
        if cap.get(cv2.CAP_PROP_POS_FRAMES) % frames_to_skip == 0:
            results = model(frame, verbose=False, conf=0.5)
            annotated_frame = results[0].plot()
            out.write(annotated_frame)
        
    out.release()
    cap.release()

    # Remove the temporary file after usage
    os.remove(input_video_path)

    return Response(headers=headers)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)