import streamlit as st
import cv2
import numpy as np
import av
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

st.title("Streamlit App Test (MediaPipe)")
st.write("Saitoh-lab @ Kyutech")

def process(image, is_show_image, draw_pattern):
    out_image = image.copy()

    with mp.solutions.face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        min_detection_confidence=0.5
    ) as face_mesh:

        # landmark indexes
        all_left_eye_idxs = list(mp.solutions.face_mesh.FACEMESH_LEFT_EYE)
        all_left_eye_idxs = set(np.ravel(all_left_eye_idxs))
        all_right_eye_idxs = list(mp.solutions.face_mesh.FACEMESH_RIGHT_EYE)
        all_right_eye_idxs = set(np.ravel(all_right_eye_idxs))
        all_left_brow_idxs = list(mp.solutions.face_mesh.FACEMESH_LEFT_EYEBROW)
        all_left_brow_idxs = set(np.ravel(all_left_brow_idxs))
        all_right_brow_idxs = list(mp.solutions.face_mesh.FACEMESH_RIGHT_EYEBROW)
        all_right_brow_idxs = set(np.ravel(all_right_brow_idxs))
        all_lip_idxs = list(mp.solutions.face_mesh.FACEMESH_LIPS)
        all_lip_idxs = set(np.ravel(all_lip_idxs))
        all_idxs = all_left_eye_idxs.union(all_right_eye_idxs)
        all_idxs = all_idxs.union(all_left_brow_idxs)
        all_idxs = all_idxs.union(all_right_brow_idxs)
        all_idxs = all_idxs.union(all_lip_idxs)


        results = face_mesh.process(image)

        (image_height, image_width) = image.shape[:2]

        black_image = np.zeros((image_height, image_width, 3), np.uint8)
        white_image = black_image + 255

        if is_show_image == False:
            out_image = white_image.copy()

        if pattern_landmarks == "A":
            if results.multi_face_landmarks:
                for face in results.multi_face_landmarks:
                   for landmark in face.landmark:               
                        x = int(landmark.x * image_width)
                        y = int(landmark.y * image_height)
                        cv2.circle(out_image, center=(x, y), radius=2, color=(0, 255, 0), thickness=-1)
                        cv2.circle(out_image, center=(x, y), radius=1, color=(255, 255, 255), thickness=-1)

        elif pattern_landmarks == "B":
            if results.multi_face_landmarks:
                for face in results.multi_face_landmarks:
                    for idx in range(len(face.landmark)):
                        x = face.landmark[idx].x
                        y = face.landmark[idx].y
                        x = int(x * image_width)
                        y = int(y * image_height)
    
                        if idx in all_idxs:
                            cv2.circle(out_image, center=(x, y), radius=2, color=(0, 0, 255), thickness=-1)
                        else:
                            cv2.circle(out_image, center=(x, y), radius=1, color=(128, 128, 128), thickness=-1)    
        
    return cv2.flip(out_image, 1)
    
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class VideoProcessor:
    def __init__(self) -> None:
        self.is_show_image = True
        self.draw_pattern = "A"

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = process(img, self.is_show_image, self.draw_pattern)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_ctx = webrtc_streamer(
    key="example",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    video_processor_factory=VideoProcessor,
    async_processing=True,
)

if webrtc_ctx.video_processor:
    webrtc_ctx.video_processor.is_show_image = st.checkbox("show camera image", value=True)
    webrtc_ctx.video_processor.draw_pattern = st.radio("draw pattern", ["A", "B", "None"], key="A", horizontal=True)
    
