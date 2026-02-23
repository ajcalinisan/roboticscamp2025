from picamera2 import Picamera2
import cv2
import numpy as np

from hsv_persistence import load_hsv_range, save_hsv_range

# Setup Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 60  # Set your desired FPS here
picam2.configure("preview")
'''
picam2.set_controls ({
	"ExposureTime": 1000
})
'''
picam2.start()

# Define HSV range for your yellow-green pickleball
PROFILE_NAME = "green_ball_tracker"
DEFAULT_LOWER_HSV = np.array([30, 140, 140], dtype=np.uint8)
DEFAULT_UPPER_HSV = np.array([43, 247, 255], dtype=np.uint8)
lower_hsv, upper_hsv, clicked_hsv = load_hsv_range(PROFILE_NAME, DEFAULT_LOWER_HSV, DEFAULT_UPPER_HSV)

H_TOLERANCE = 10
S_TOLERANCE = 60
V_TOLERANCE = 60
AVG_SAMPLE_COUNT = 3

# Global frame storage for mouse callback
hsv_frame = None
sampled_hsv = []


def average_hsv_samples(samples):
    hue_angles = np.array([sample[0] * (2.0 * np.pi / 180.0) for sample in samples], dtype=np.float32)
    sin_mean = np.mean(np.sin(hue_angles))
    cos_mean = np.mean(np.cos(hue_angles))
    avg_angle = np.arctan2(sin_mean, cos_mean)
    if avg_angle < 0:
        avg_angle += 2.0 * np.pi

    avg_h = int(round(avg_angle * (180.0 / (2.0 * np.pi)))) % 180
    avg_s = int(round(np.mean([sample[1] for sample in samples])))
    avg_v = int(round(np.mean([sample[2] for sample in samples])))
    return avg_h, avg_s, avg_v


def update_hsv_range_from_center(h, s, v):
    lower_h = (h - H_TOLERANCE) % 180
    upper_h = (h + H_TOLERANCE) % 180

    lower = np.array(
        [lower_h, max(0, s - S_TOLERANCE), max(0, v - V_TOLERANCE)],
        dtype=np.uint8,
    )
    upper = np.array(
        [upper_h, min(255, s + S_TOLERANCE), min(255, v + V_TOLERANCE)],
        dtype=np.uint8,
    )
    return lower, upper


def build_hsv_mask(hsv):
    if int(lower_hsv[0]) <= int(upper_hsv[0]):
        return cv2.inRange(hsv, lower_hsv, upper_hsv)

    lower_1 = np.array([0, int(lower_hsv[1]), int(lower_hsv[2])], dtype=np.uint8)
    upper_1 = np.array([int(upper_hsv[0]), int(upper_hsv[1]), int(upper_hsv[2])], dtype=np.uint8)
    lower_2 = np.array([int(lower_hsv[0]), int(lower_hsv[1]), int(lower_hsv[2])], dtype=np.uint8)
    upper_2 = np.array([179, int(upper_hsv[1]), int(upper_hsv[2])], dtype=np.uint8)

    return cv2.bitwise_or(cv2.inRange(hsv, lower_1, upper_1), cv2.inRange(hsv, lower_2, upper_2))


# Mouse callback to collect HSV samples and update mask after averaging
def show_hsv_on_click(event, x, y, flags, param):
    global hsv_frame, clicked_hsv, lower_hsv, upper_hsv, sampled_hsv

    if event == cv2.EVENT_LBUTTONDOWN and hsv_frame is not None:
        sample = tuple(int(val) for val in hsv_frame[y, x])
        sampled_hsv.append(sample)
        print(f"Sample {len(sampled_hsv)}/{AVG_SAMPLE_COUNT} at ({x},{y}): {sample}")

        if len(sampled_hsv) < AVG_SAMPLE_COUNT:
            return

        clicked_hsv = average_hsv_samples(sampled_hsv)
        sampled_hsv = []
        lower_hsv, upper_hsv = update_hsv_range_from_center(*clicked_hsv)

        save_hsv_range(PROFILE_NAME, lower_hsv, upper_hsv, clicked_hsv)
        print(f"Averaged HSV: {clicked_hsv}")
        print(f"Saved HSV range: lower={lower_hsv.tolist()}, upper={upper_hsv.tolist()}")


cv2.namedWindow("Pickleball Tracking")
cv2.setMouseCallback("Pickleball Tracking", show_hsv_on_click)

try:
    while True:
        # Capture frame
        frame = cv2.flip(picam2.capture_array(), -1)

        # Convert to HSV and store for mouse clicks
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # Create mask
        mask = build_hsv_mask(hsv_frame)

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

        if clicked_hsv is None:
            cv2.putText(frame, "Left click 3x to sample ball color", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        else:
            cv2.putText(frame, f"Picked AVG HSV: {clicked_hsv}", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        if sampled_hsv:
            cv2.putText(frame, f"Sampling: {len(sampled_hsv)}/{AVG_SAMPLE_COUNT}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        # Show feed
        cv2.imshow("Pickleball Tracking", frame)

        # ESC to exit
        if cv2.waitKey(1) == 27:
            break
finally:
    try:
        picam2.stop()
    except Exception:
        pass
    cv2.destroyAllWindows()
