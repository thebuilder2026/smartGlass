# DrishtiGlass AI — AI Smart Glasses Assistive Vision

DrishtiGlass AI is a hackathon-ready smart-glasses software prototype that uses computer vision to help a wearer understand nearby surroundings. A camera feed is processed using YOLOv8 object detection to identify everyday objects, estimate whether they are to the left, right, or ahead, flag visually large nearby objects as possible hazards, and generate short scene guidance.

The project can be demonstrated with a laptop webcam or image upload, so physical smart-glasses hardware is not required for the hackathon demo.

## Main Features

- YOLOv8 object detection
- Webcam-based smart-glasses simulation
- Camera snapshot analysis
- Image-upload analysis
- Left / ahead / right object-position estimation
- Close / very-close visual hazard heuristic
- Road Safety mode
- Indoor Navigation mode
- General Mobility mode
- Scene summary generation
- Voice alerts in live webcam mode
- Optional Groq AI scene guidance
- Detection event logging
- Event analytics dashboard
- `.env` configuration

## Problem Statement

People with visual limitations, elderly users, travellers, and individuals moving through unfamiliar environments may find it difficult to quickly identify obstacles, moving vehicles, people, animals, and other objects around them. Traditional smart glasses can provide a camera view, but without intelligent interpretation they cannot actively explain what is happening in the user's surroundings. This can reduce situational awareness, particularly in crowded roads, indoor spaces, public areas, and unfamiliar locations.

There is therefore a need for an intelligent wearable-assistance system that can continuously interpret a camera feed, identify important surrounding objects, determine their approximate direction, highlight potential hazards, and communicate concise guidance to the wearer without requiring them to constantly look at a screen.

## Solution

DrishtiGlass AI transforms a smart-glasses camera into an AI-assisted environmental awareness system. The camera feed is analyzed using YOLOv8 to detect common objects such as people, cars, buses, motorcycles, bicycles, chairs, animals, and other everyday objects.

The application determines whether each detected object is on the left, right, or directly ahead. A prototype visual-size heuristic estimates whether an object appears close to the camera and generates warning messages for potentially important nearby objects.

The solution provides multiple assist modes for general mobility, road environments, and indoor navigation. Short scene summaries and hazard messages can be delivered visually or through voice output, making the architecture suitable for integration with an earpiece or bone-conduction speaker in future smart-glasses hardware.

For hackathon demonstration, the same AI pipeline works with a normal webcam or uploaded image, allowing the concept to be tested without specialized wearable hardware.

## Technology Stack

- Python
- Streamlit
- YOLOv8 / Ultralytics
- OpenCV
- NumPy
- Pandas
- Plotly
- pyttsx3
- python-dotenv
- Optional Groq API

## Project Structure

```text
drishtiglass_ai_smart_glasses/
├── app.py
├── live_glasses.py
├── requirements.txt
├── .env
├── .env.example
├── README.md
├── HOW_IBM_BOB_WAS_USED.md
├── run_dashboard.bat
├── run_live_glasses.bat
├── utils/
│   ├── vision.py
│   ├── speech.py
│   ├── event_log.py
│   └── ai.py
├── data/
├── outputs/
└── .streamlit/
    └── config.toml
```

## Installation

```bash
pip install -r requirements.txt
```

YOLOv8 will download `yolov8n.pt` automatically the first time it is used if it is not already available.

## Run the Hackathon Dashboard

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

## Run Live Smart-Glasses Simulation

```bash
python live_glasses.py
```

This opens the laptop webcam and displays the AI-annotated view.

Press:

```text
Q
```

to quit.

## Suggested Hackathon Demo

1. Explain that the laptop webcam represents the smart-glasses camera.
2. Run the live smart-glasses mode.
3. Place a chair or another person in front of the camera.
4. Show object detection and left/ahead/right classification.
5. Bring an object closer and show the close-object warning.
6. Demonstrate spoken alerts.
7. Open the Streamlit dashboard.
8. Test Road Safety and Indoor Navigation modes.
9. Upload a street or room image.
10. Show detection-event analytics.
11. Explain how the same software can run on a wearable edge device.

## Hardware Integration Idea

A future physical prototype could use:

- Small camera module
- Raspberry Pi 5 / Jetson Orin Nano / compatible edge-AI computer
- Smart-glasses frame
- Bone-conduction speaker or Bluetooth earpiece
- Battery pack
- GPS module
- IMU
- Depth camera or ultrasonic sensor
- Emergency/SOS button

## Important Limitation

The current prototype estimates closeness using the size of an object's bounding box in the image. This is not a true physical-distance measurement.

For a real safety-critical wearable product, true depth sensing should be added using stereo vision, LiDAR, ToF, ultrasonic sensing, or another validated ranging technology.

The project should not be presented as a replacement for a mobility cane, guide dog, trained human assistance, or certified safety equipment.

## Future Enhancements

- True depth estimation
- Stair and pothole detection
- Traffic-light recognition
- Pedestrian-crossing detection
- OCR and text-to-speech
- Currency recognition
- Medicine-label reading
- GPS navigation
- Indoor navigation
- Multilingual voice alerts
- Emergency location sharing
- Fall detection
- Familiar-object recognition
- Edge-AI optimization
- Offline models
- Battery optimization
- Smart-glasses hardware prototype

## Hackathon Pitch

"DrishtiGlass AI turns ordinary smart glasses into an intelligent environmental assistant. Instead of simply recording what the wearer sees, the glasses understand nearby objects, identify their direction, highlight possible hazards, and communicate concise guidance through audio, helping users become more aware of their surroundings."
