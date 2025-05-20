import requests
import time
import config
from datetime import datetime
from camera import capture_image
from face_recognition import recognize_face
from oled_display import display_message, display_idle, display_success, display_no_control
from ir_sensor import is_triggered

def get_system_status():
    """Check if the system should be active based on PC control."""
    try:
        resp = requests.get(config.SERVER_CONTROL_URL, timeout=5)
        return resp.text.strip().lower() == "on"
    except:
        return False

def send_attendance(name):
    """Send attendance data to Flask app on PC."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        response = requests.post("http://192.168.66.182:5000/submit_attendance", json={
            "name": name,
            "timestamp": timestamp
        }, timeout=5)
        if response.ok:
            print(f"Attendance sent: {name}, {timestamp}")
        else:
            print(f"Failed to send attendance: {response.status_code}")
    except Exception as e:
        print(f"Error sending attendance: {e}")

if __name__ == "__main__":
    print("Smart Attendance System Started")
    display_message("Smart Attendance", "Starting...")

    while True:
        system_on = get_system_status()

        if not system_on:
            display_no_control()
            time.sleep(2)
            continue

        display_idle()
        if is_triggered():
            path = capture_image()
            name = recognize_face(path)
            send_attendance(name)
            display_success(name)
            time.sleep(3)  # Debounce delay
