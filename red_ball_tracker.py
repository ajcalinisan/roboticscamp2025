from picamera2 import Picamera2
import cv2
import numpy as np

# Setup Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
'''
picam2.set_controls ({
	"ExposureTime": 1000
})
'''
picam2.start()
#picam2.set_controls({ "FrameRate": 30})
# Define HSV range for red wiffleball
lower_hsv = np.array([172, 130, 50])
upper_hsv = np.array([178, 247, 255])

# Global frame storage for mouse callback
clicked_hsv = (0, 0, 0)
hsv_frame = None

# Mouse callback to get HSV value at click
def show_hsv_on_click(event, x, y, flags, param):
    global hsv_frame
    if event == cv2.EVENT_LBUTTONDOWN and hsv_frame is not None:
        hsv_val = hsv_frame[y, x]
        print(f"HSV at ({x},{y}): {hsv_val}")

cv2.namedWindow("Pickleball Tracking")
cv2.setMouseCallback("Pickleball Tracking", show_hsv_on_click)

while True:
    # Capture frame
    frame = cv2.flip(picam2.capture_array(), -1)

    # Convert to HSV and store for mouse clicks
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create mask
    mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)

    # Find contours
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
            cv2.circle(frame, (int(x), int(y)), 3, (0, 0, 255), -1)
            cv2.putText(frame, f"Radius: {int(radius)}", (int(x)-40, int(y)-20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Show feed
    cv2.imshow("Pickleball Tracking", frame)

    # ESC to exit
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
