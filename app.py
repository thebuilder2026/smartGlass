import os
from pathlib import Path
import cv2
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

from utils.vision import analyze_frame
from utils.event_log import log_events, read_events
from utils.ai import scene_guidance

load_dotenv()
APP_NAME = os.getenv("APP_NAME","DrishtiGlass AI")

st.set_page_config(page_title=APP_NAME,page_icon="👓",layout="wide")

with st.sidebar:
    st.title(APP_NAME)
    st.caption("AI Smart Glasses Assistive Vision Prototype")
    page = st.radio("Navigation",[
        "Smart Glass Demo",
        "Camera Snapshot",
        "Event Analytics",
        "How It Works"
    ])
    mode = st.selectbox("Assist Mode",[
        "General Mobility",
        "Road Safety",
        "Indoor Navigation"
    ])

def show_analysis(image_rgb, source):
    frame = cv2.cvtColor(np.array(image_rgb), cv2.COLOR_RGB2BGR)
    annotated, detections, alerts, summary = analyze_frame(frame, mode)
    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

    guidance, guidance_mode = scene_guidance(summary, alerts)

    c1,c2 = st.columns([1.4,1])
    with c1:
        st.image(annotated_rgb,caption="AI Smart Glass View",use_container_width=True)
    with c2:
        st.subheader("Scene Guidance")
        if alerts:
            for alert in alerts[:5]:
                st.error(alert)
        else:
            st.success("No close hazard detected by the current prototype.")
        st.info(guidance)
        st.caption(guidance_mode)

        st.metric("Objects Detected",len(detections))
        st.metric("Close Hazard Alerts",len(alerts))

    if detections:
        table = pd.DataFrame(detections)
        st.subheader("Detected Objects")
        st.dataframe(table,use_container_width=True,hide_index=True)
        log_events(detections,source=source)

    st.caption(
        "Distance is estimated from bounding-box size and is only a prototype heuristic. "
        "This system must not be treated as a replacement for a mobility aid, trained guide, or safety equipment."
    )

if page == "Smart Glass Demo":
    st.title("AI Smart Glasses — Scene & Hazard Detection")
    st.write(
        "Upload an image representing what the smart-glasses camera sees. "
        "The system detects objects, estimates their direction, flags nearby hazards, "
        "and generates short assistive guidance."
    )

    uploaded = st.file_uploader("Upload smart-glass camera image",type=["jpg","jpeg","png"])
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        show_analysis(image,"uploaded_image")
    else:
        st.info("Upload an image to start the AI analysis.")

elif page == "Camera Snapshot":
    st.title("Camera Snapshot Mode")
    st.write("Use your device camera to capture a frame and analyze the surroundings.")
    shot = st.camera_input("Capture smart-glass view")
    if shot:
        image = Image.open(shot).convert("RGB")
        show_analysis(image,"camera_snapshot")

elif page == "Event Analytics":
    st.title("Detection Event Analytics")
    events = read_events()

    if events.empty:
        st.info("No detection events have been logged yet.")
    else:
        c1,c2,c3 = st.columns(3)
        c1.metric("Logged Detections",len(events))
        c2.metric("Hazard Detections",int(events["hazard"].astype(str).str.lower().eq("true").sum()))
        c3.metric("Unique Objects",events["object"].nunique())

        counts = events.groupby("object",as_index=False).size().sort_values("size",ascending=False)
        st.plotly_chart(
            px.bar(counts.head(15),x="object",y="size",text_auto=True),
            use_container_width=True
        )
        st.dataframe(events.tail(200),use_container_width=True,hide_index=True)

elif page == "How It Works":
    st.title("How DrishtiGlass AI Works")
    st.markdown("""
1. A camera mounted on smart glasses captures the user's surroundings.
2. YOLOv8 detects common objects such as people, cars, buses, bicycles, chairs, animals, and other everyday items.
3. The system estimates whether an object is on the left, right, or directly ahead.
4. A simple visual-size heuristic estimates whether an object is close or very close.
5. Relevant nearby objects are converted into short hazard alerts.
6. The scene is summarized into concise guidance that can later be delivered through an earpiece or bone-conduction speaker.
7. Detection events are logged for analytics and prototype testing.
""")
    st.warning(
        "This is a hackathon prototype. Camera-only object detection cannot measure true physical distance "
        "reliably. A production smart-glasses system should add depth sensors, GPS/IMU, obstacle sensors, "
        "battery management, accessibility testing, and rigorous field validation."
    )
