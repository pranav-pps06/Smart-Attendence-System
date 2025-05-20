import cv2
import config

def capture_image(path="capture.jpg"):
    
    cap = cv2.VideoCapture(0)

    if hasattr(config, 'CAMERA_RESOLUTION'):
        width, height = config.CAMERA_RESOLUTION
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    if not cap.isOpened():
        raise RuntimeError("Could not open USB camera")

    ret, frame = cap.read()
    cap.release()

    if not ret:
        raise RuntimeError("Failed to capture image from USB camera")

    cv2.imwrite(path, frame)
    return path
