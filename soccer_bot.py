from gpiozero import Motor
from picamera2 import Picamera2
import cv2
import numpy as np
from time import sleep

# === Motor Setup ===
right_motor = Motor(forward=17, backward=18)
left_motor = Motor(forward=22, backward=23)

# === Speed Compensation ===
# *YOU CAN CHANGE THESE*
RIGHT_SPEED = 1.0
LEFT_SPEED = 0.7  # 30% slower left motor
TURN_SPEED = 0.4
TURN_TIME = 0.1   # How long each turn burst lasts (seconds)
SPIN_TIME = 0.09
TURN_SLEEP = 0.05
SPIN_SLEEP = 0.3
PUSH_SLEEP = 2
# === Constants ===
# *YOU CAN CHANGE THESE*
CENTER_MIN = 240
CENTER_MAX = 400
FAR_RADIUS = 10
NEAR_RADIUS = 40

# === Camera Setup ===
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 60  # Set your desired FPS here
picam2.configure("preview")
picam2.start()
"""
picam2.set_controls({
    "ExposureTime": 3000,      # Reduce motion blur
    "AnalogueGain": 4.0
})
"""
# === HSV Range for Red Wiffleball ===
lower_hsv = np.array([172, 130, 50])
upper_hsv = np.array([178, 247, 255])


# === Movement Functions ===
def stop():
    left_motor.stop()
    right_motor.stop()

def spin_right():
    print("Spinning right to search...")
    left_motor.forward(LEFT_SPEED)
    right_motor.backward(RIGHT_SPEED)
    sleep(SPIN_TIME)
    stop()

def turn_toward(direction):
    print(f"Turning {direction}...")
    if direction == "left":
        left_motor.backward(TURN_SPEED * LEFT_SPEED)
        right_motor.forward(TURN_SPEED * RIGHT_SPEED)
    elif direction == "right":
        left_motor.forward(TURN_SPEED * LEFT_SPEED)
        right_motor.backward(TURN_SPEED * RIGHT_SPEED)
    sleep(TURN_TIME)
    stop()

def move_forward():
    print("Moving forward...")
    left_motor.forward(LEFT_SPEED * 0.8)
    right_motor.forward(RIGHT_SPEED * 0.8)

def push_forward():
    print("Pushing the ball...")
    left_motor.forward(LEFT_SPEED)
    right_motor.forward(RIGHT_SPEED)

# === Main Loop ===
while True:
    frame = cv2.flip(picam2.capture_array(), -1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        x = int(x)
        radius = int(radius)

        # Visuals
        cv2.circle(frame, (x, int(y)), radius, (0, 255, 0), 2)
        cv2.putText(frame, f"x={x}, r={radius}", (x, int(y) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if radius < FAR_RADIUS:
            spin_right()
            sleep(SPIN_SLEEP)
        elif radius < NEAR_RADIUS:
            if CENTER_MIN <= x <= CENTER_MAX:
                move_forward()
            elif x < CENTER_MIN:
                turn_toward("left")
                sleep(TURN_SLEEP)
            else:
                turn_toward("right")
                sleep(TURN_SLEEP)
        else:
            push_forward()
            sleep(PUSH_SLEEP)
    else:
        spin_right()
        sleep(SPIN_SLEEP)


 # This is the code for the camera view. 
 # If you want to run this script on startup,
 # use '#'s to comment out these next three lines.       
    cv2.imshow("Soccer Bot View", frame)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
stop()
