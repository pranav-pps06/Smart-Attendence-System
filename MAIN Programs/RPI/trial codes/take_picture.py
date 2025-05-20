import cv2
import time
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("? Failed to open camera")
    exit()
time.sleep(2)

for _ in range(5):
    cap.read()
  
ret, frame = cap.read()

if ret:
    cv2.imwrite("usb_test.jpg", frame)
    print("? Image saved as usb_test.jpg")
else:
    print("? Failed to capture frame")

cap.release()
