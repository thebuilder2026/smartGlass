import cv2
from utils.vision import analyze_frame
from utils.speech import speak
from utils.event_log import log_events

MODE = "General Mobility"

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    frame_count = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            annotated, detections, alerts, summary = analyze_frame(frame, MODE)
            frame_count += 1

            if alerts:
                speak(alerts[0])
            elif frame_count % 120 == 0:
                speak(summary)

            if frame_count % 30 == 0:
                log_events(detections, source="live_webcam")

            cv2.putText(
                annotated,
                "DrishtiGlass AI | Q = Quit",
                (20,30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )

            cv2.imshow("DrishtiGlass AI Smart Glasses", annotated)

            if cv2.waitKey(1) & 0xFF in [ord("q"), ord("Q")]:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
