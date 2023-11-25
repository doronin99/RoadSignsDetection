import streamlit as st
import cv2
from ultralytics import YOLO
from tqdm import tqdm
import tempfile
import os

st.title("Road Signs Detector")


def perform_video_inference(video_file, model_weights='best_multi.pt', output_file='output_multi.mp4'):
    model = YOLO(model_weights)
    frames_to_skip = 2

    # Create a temporary file to save the contents of the uploaded file
    temp_video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    with open(temp_video_path, "wb") as f:
        f.write(video_file.read())

    cap = cv2.VideoCapture(temp_video_path)
    if not cap.isOpened():
        st.error("Error: Unable to open the video")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (int(cap.get(3)), int(cap.get(4))))

    for _ in tqdm(range(total_frames), desc="Processing video"):
        success, frame = cap.read()
        if not success:
            break

        if cap.get(cv2.CAP_PROP_POS_FRAMES) % frames_to_skip == 0:
            results = model(frame, verbose=False)
            annotated_frame = results[0].plot()
            out.write(annotated_frame)

    out.release()
    cap.release()

    # Remove the temporary file after usage
    os.remove(temp_video_path)


# Upload a video file
video_file = st.file_uploader("Upload a video file", type=["mp4"])

st.markdown(
        """
        ## Instructions:
        1. Upload a video file in MP4 format using the file uploader.
        2. The model will process the video and annotate road signs.
        3. View the processed video and download the results if needed.

        **Expected Result:**
        - The processed video will be displayed below.
        - Annotated road signs will be highlighted in the video.
        """
    )

if video_file:
    # Perform predictions and display the results
    perform_video_inference(video_file)
    st.video("output_multi.mp4")  # Play the processed video
