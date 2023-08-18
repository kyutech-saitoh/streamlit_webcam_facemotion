import streamlit as st
import cv2
import numpy as np
import av
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

st.title("Streamlit App Test (MediaPipe)")
st.write("Saitoh-lab @ Kyutech")

def draw(out_image, face):
    #eye_width1 = np.sqrt((face.landmark[133].x - face.landmark[33].x)**2 + (face.landmark[133].y - face.landmark[33].y)**2)
    #eye_height1 = np.sqrt((face.landmark[159].x - face.landmark[145].x)**2 + (face.landmark[159].y - face.landmark[145].y)**2)
    #eye_width2 = np.sqrt((face.landmark[362].x - face.landmark[263].x)**2 + (face.landmark[362].y - face.landmark[263].y)**2)
    #eye_height2 = np.sqrt((face.landmark[386].x - face.landmark[374].x)**2 + (face.landmark[386].y - face.landmark[374].y)**2)
    #eye_width1 = int(eye_width1 * image_width)
    #eye_height1 = int(eye_height1 * image_width)
    #eye_width2 = int(eye_width2 * image_height)
    #eye_height2 = int(eye_height2 * image_height)
    
    #eye_center1x = (face.landmark[133].x + face.landmark[33].x + face.landmark[159].x + face.landmark[145].x) / 4
    #eye_center1y = (face.landmark[133].y + face.landmark[33].y + face.landmark[159].y + face.landmark[145].y) / 4
    #eye_center2x = (face.landmark[362].x + face.landmark[263].x + face.landmark[386].x + face.landmark[374].x) / 4
    #eye_center2y = (face.landmark[362].y + face.landmark[263].y + face.landmark[386].y + face.landmark[374].y) / 4
    #eye_center1x = int(eye_center1x * image_width)
    #eye_center1y = int(eye_center1y * image_width)
    #eye_center2x = int(eye_center2x * image_height)
    #eye_center2y = int(eye_center2y * image_height)

    dis1 = 100
    dis2 = 100
    dis1_ = int(dis1 / 5)
    dis2_ = int(dis2 / 5)
    
    x1 = face.landmark[468].x
    y1 = face.landmark[468].y
    x1 = int(x1 * image_width)
    y1 = int(y1 * image_height)
    
    x2 = face.landmark[473].x
    y2 = face.landmark[473].y
    x2 = int(x2 * image_width)
    y2 = int(y2 * image_height)
    
    #cv2.ellipse(out_image, ((eye_center1x, eye_center1y), (eye_width1, eye_height1), 0), (200, 200, 255), -1)
    cv2.circle(out_image, center=(x1, y1), radius=dis1, color=(250, 250, 255), thickness=-1)
    cv2.circle(out_image, center=(x1, y1), radius=dis1_, color=(0, 0, 0), thickness=-1)
    cv2.circle(out_image, center=(x2, y2), radius=dis2, color=(255, 250, 250), thickness=-1)
    cv2.circle(out_image, center=(x2, y2), radius=dis2_, color=(0, 0, 0), thickness=-1)

    return out_image
    
def process(image, is_show_image, draw_pattern):
    out_image = image.copy()

    with mp.solutions.face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=True,
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

        left_iris_idxs = list(mp.solutions.face_mesh.FACEMESH_LEFT_IRIS)
        left_iris_idxs = set(np.ravel(left_iris_idxs))
        right_iris_idxs = list(mp.solutions.face_mesh.FACEMESH_RIGHT_IRIS)
        right_iris_idxs = set(np.ravel(right_iris_idxs))

        results = face_mesh.process(image)

        (image_height, image_width) = image.shape[:2]

        black_image = np.zeros((image_height, image_width, 3), np.uint8)
        white_image = black_image + 255

        if is_show_image == False:
            out_image = white_image.copy()

        if draw_pattern == "A":
            if results.multi_face_landmarks:
                for face in results.multi_face_landmarks:
                   for landmark in face.landmark:               
                        x = int(landmark.x * image_width)
                        y = int(landmark.y * image_height)
                        cv2.circle(out_image, center=(x, y), radius=2, color=(0, 255, 0), thickness=-1)
                        cv2.circle(out_image, center=(x, y), radius=1, color=(255, 255, 255), thickness=-1)

        elif draw_pattern == "B":
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

        elif draw_pattern == "C":
            if results.multi_face_landmarks:
                for face in results.multi_face_landmarks:
                    out_image = draw(out_image, face) 
                    
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
    webrtc_ctx.video_processor.draw_pattern = st.radio("draw pattern", ["A", "B", "C", "None"], key="A", horizontal=True)
