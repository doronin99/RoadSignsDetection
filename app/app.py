import streamlit as st
import os
import requests


def save_video(video_file_name, video_file, input_dir="../input"):
    with open(os.path.join(input_dir, video_file_name), "wb") as f:
        f.write(video_file.read())
    return os.path.join(input_dir, video_file_name), video_file_name


def process_video(video_name: str, server_url: str = "http://localhost:8080/predict"):
    data = {"video_name": video_name}
    return requests.post(server_url, json=data, timeout=8000)


def main():
    st.title("Road Signs Detector")

    with st.form("Uploaded video"):
        video_file = st.file_uploader(
            "Upload a video file...",
            type=["mp4"],
            accept_multiple_files=False,
        )
        submit_button = st.form_submit_button("Process video")

        object_name = None
        if video_file is not None:
            try:
                object_path, object_name = save_video(video_file.name, video_file)

            except RuntimeError as e:
                st.write(str(e))

        if submit_button:
            if object_name is not None:
                with st.spinner(f"Processing video..."):
                    response = process_video(object_name)
                    print(response)
                    if response.headers["success"] == "True":
                        st.write("Processed video is shown below")

                        st_video = open(os.path.join("../output", object_name), "rb")
                        st_video_bytes = st_video.read()
                        st.video(st_video_bytes)
                    else:
                        st.write("Error while processing video")

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


if __name__ == "__main__":
    main()
