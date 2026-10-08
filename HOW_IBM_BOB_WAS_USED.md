# How IBM Bob Was Used in DrishtiGlass AI

IBM Bob was used as an AI-assisted development tool throughout the DrishtiGlass AI smart-glasses project. It helped analyze the assistive-vision use case, plan the computer-vision architecture, generate and refine Python code, and organize the application into reusable modules. IBM Bob supported the integration of YOLOv8 and OpenCV for object detection, helped implement object-position classification for left, right, and forward directions, and assisted in creating the logic used to identify visually close objects and convert them into hazard alerts.

IBM Bob was also used to develop the Streamlit demonstration interface, webcam-based smart-glasses simulation, detection-event logging, voice-alert workflow, and multiple assist modes such as General Mobility, Road Safety, and Indoor Navigation. It helped debug camera-processing issues, improve exception handling, refactor repeated logic, configure optional services through `.env`, and add an optional AI layer for generating concise scene guidance.

IBM Bob further assisted in documenting the system architecture, identifying limitations of camera-only distance estimation, and planning future hardware integration with depth sensors, GPS, IMU, bone-conduction audio, and edge-AI devices. The actual object detection is performed by the YOLOv8 model; IBM Bob was used as a development assistant for planning, coding, debugging, refactoring, and documentation. Final feature selection, testing, safety decisions, and project validation were handled by the development team.

## Example IBM Bob Prompts

### Ask Mode

```text
Design an AI smart-glasses solution that can help a user understand nearby
surroundings using a camera. The system should detect objects, identify
whether they are left, right or ahead, identify possible close hazards,
and provide short voice guidance.
```

### Plan Mode

```text
Create a modular Python architecture using YOLOv8, OpenCV and Streamlit
for an AI smart-glasses assistive-vision prototype. Include webcam input,
image input, hazard logic, scene summaries, voice alerts, event logging,
multiple assist modes, .env configuration and optional AI guidance.
```

### Agent Mode

```text
Implement the complete smart-glasses prototype across multiple Python files.
Create object detection, position estimation, close-object alerts, webcam
processing, voice output, Streamlit dashboard, analytics, fallback handling,
configuration and documentation.
```
