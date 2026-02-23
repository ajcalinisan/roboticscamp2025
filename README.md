# Author: AJ Calinisan
# Email: acalinis@uci.edu
# Date: 2-23-26

# SoccerBot: Raspberry Pi 4 Autonomous Ball-Tracking Rover

This project enables a Raspberry Pi 4-powered robot to:

1. Test motors using `motor_test.py`
2. Track a yellow-green pickleball with `green_ball_tracker.py`
3. Track a red wiffleball with `red_ball_tracker.py`
4. Chase and push the red ball autonomously using `soccer_bot.py`

---

## Overview (For Teachers)

This project teaches students how to build and program a robot that uses computer vision to:

- Detect a colored ball
- Turn toward it
- Drive forward
- Push it autonomously

You do not need to be a programmer to teach this.

Students will:

- Learn how cameras detect color using HSV
- Tune detection by clicking on the video preview
- Connect camera input to motor control
- Build a fully autonomous ball-chasing robot

---

## For Non-Technical Teachers

You do not need to understand:

- OpenCV internals
- Vision math details
- Linux deeply

You only need to:

- Run the scripts
- Click the ball to calibrate
- Encourage experimentation

---

## Suggested Teaching Flow (High School Camp)

### Day 1 - Build

- Assemble chassis
- Wire motors
- Verify `motor_test.py`

### Day 2 - Vision

- Run tracker scripts
- Explain HSV basics
- Use click-to-sample feature
- Adjust thresholds

### Day 3 - Integration

- Run `soccer_bot.py`
- Observe turning logic
- Tune motor speeds

### Day 4 - Refinement

- Adjust `TURN_TIME`
- Adjust `TURN_SPEED`
- Improve centering behavior

### Day 5 - Competition

- Push ball into goal
- Timed challenge
- Obstacle variation

---

## Clone and Run

```bash
git clone https://rasp@github.com/ajcalinisan/roboticscamp2025.git
cd roboticscamp2025
python3 soccer_bot.py
```

To delete the project directory:

```bash
cd ~
sudo rm -rf roboticscamp2025
```

---

## Pin Connections

| Raspberry Pi Pin | Function      | Connects To      |
| ---------------- | ------------- | ---------------- |
| Pin 11 (GPIO17)  | Motor Left A  | IN1              |
| Pin 12 (GPIO18)  | Motor Left B  | IN2              |
| Pin 15 (GPIO22)  | Motor Right A | IN3              |
| Pin 16 (GPIO23)  | Motor Right B | IN4              |
| Pin 2 or 4       | 5V Power      | Motor driver VCC |
| Pin 6 or 9       | Ground        | Motor driver GND |

---

## Hardware Requirements

- Raspberry Pi 4 and SD card
- 9V battery and Jumper Cable Adapter
- Power bank for Raspberry Pi
- Rover chassis
- Bold-colored ball to chase
- Camera module

Motor components:

- L293D motor driver
- 2x yellow gearbox motors with wheels
- 1x castor wheel

Cables:

- 2x male-to-female Dupont cables
- 4x female-to-female Dupont cables
- USB-A to USB-C cable
- 9V battery to Dupont adapter
- HDMI cable (for monitor setup)
- Raspberry Pi power adapter (for monitor setup)

Tools:

- Screwdrivers
- Pliers

---

## Project Files

### `motor_test.py`

Moves the robot forward, backward, left turn, and right turn (4 seconds each).
Includes safe motor stop behavior on normal exit and Ctrl+C.

### `green_ball_tracker.py`

Tracks a yellow-green pickleball using HSV filtering and draws a circle around the largest matching object.

### `red_ball_tracker.py`

Tracks a red wiffleball using HSV filtering and draws a circle around the largest matching object.

### `soccer_bot.py`

Full autonomous soccer mode for a red wiffleball:

- Spins to search for the ball
- Centers itself
- Moves forward and pushes the ball

### `hsv_persistence.py`

Shared helper used by all trackers and `soccer_bot.py` to save/load HSV ranges.

### `hsv_presets.json`

Auto-generated file that stores the latest saved HSV ranges per script profile.

---

## Setup Instructions

### Enable Interfaces

```bash
sudo raspi-config
```

- Enable **Camera** (Interface Options)
- Enable **SSH** if remote access is needed

### Install Required Packages

```bash
sudo apt update
sudo apt install python3-opencv python3-gpiozero python3-picamera2
```

If OpenCV is not found:

```bash
pip install opencv-python
```

### Test Camera

```bash
libcamera-hello
```

If nothing appears, re-check cable seating, re-enable the camera in `raspi-config`, and reboot.

---

## Run Scripts

### Motor Test

```bash
python3 motor_test.py
```

### Yellow-Green Ball Tracker

```bash
python3 green_ball_tracker.py
```

### Red Ball Tracker

```bash
python3 red_ball_tracker.py
```

### Soccer Bot (Red Ball)

```bash
python3 soccer_bot.py
```

---

## HSV Calibration (Updated)

All three camera scripts now support interactive HSV picking with averaging and persistence:

- Left click the ball **3 times** in the preview window
- The script averages the 3 HSV samples
- It builds a tracking range around that average
- It saves the range to `hsv_presets.json`
- On the next run, the script automatically reuses the saved range

This behavior is enabled in:

- `green_ball_tracker.py`
- `red_ball_tracker.py`
- `soccer_bot.py`

### Notes on red tracking

- Hue wrap-around (near 0/179) is handled automatically
- This improves red ball detection when hue crosses the HSV boundary

### Reset saved HSV values

If you want to reset saved HSV calibration:

```bash
rm hsv_presets.json
```

(Or delete the file manually in your file browser.)

---

## Default HSV Fallback Values

These are the defaults used when no saved preset exists:

Yellow-green pickleball:

```python
DEFAULT_LOWER_HSV = np.array([30, 140, 140], dtype=np.uint8)
DEFAULT_UPPER_HSV = np.array([43, 247, 255], dtype=np.uint8)
```

Red wiffleball:

```python
DEFAULT_LOWER_HSV = np.array([172, 130, 50], dtype=np.uint8)
DEFAULT_UPPER_HSV = np.array([178, 247, 255], dtype=np.uint8)
```

---

## Running Soccer Bot Without Camera View

If you want the robot to run without opening a camera window (for startup/background mode),
comment out these lines in `soccer_bot.py`:

```python
cv2.imshow(WINDOW_NAME, frame)
if cv2.waitKey(1) == 27:
    break
```

---

## Run Soccer Bot on Startup

Use crontab:

```bash
crontab -e
```

At the bottom, add:

```bash
@reboot python3 /home/raspberry/roboticscamp2025/soccer_bot.py &
```

Then save and reboot to test:

```bash
sudo reboot
```

---

## Stop Startup Task

Find the process:

```bash
ps aux | grep soccer_bot.py
```

Then stop by PID:

```bash
kill PID
```

Example:

```bash
kill 1234
```

---

## Remove Startup Task

```bash
crontab -e
```

Remove this line:

```bash
@reboot python3 /home/raspberry/roboticscamp2025/soccer_bot.py &
```

---

## Troubleshooting

### Camera not opening

- Enable camera in `raspi-config`
- Reboot
- Check camera cable seating

### Ball not detected

- Use bright lighting (sunlight works best)
- Click to recalibrate HSV
- Use a bright matte ball

### Robot spins endlessly

- Center tolerance may be too narrow
- Ball may be too small/far away

### Robot too aggressive

- Reduce `TURN_SPEED`
- Add a small delay

---

## What Students Learn

- RGB vs HSV color spaces
- Image filtering
- Contour detection
- Feedback control
- Hardware/software integration
- Debugging real systems

---

## Important Notes

- Lighting matters more than code
- Bright matte balls work best (tennis ball, pickleball)
- Avoid shadows
- Keep background simple
- Left/right motor speed differences can be adjusted in `soccer_bot.py`
- Tune `TURN_TIME` and `TURN_SPEED` for smoother steering
- Ensure motor driver power wiring is correct for logic and motor supply

---

## Clean Exit

- Press `ESC` to stop the tracker windows
- `soccer_bot.py` and `motor_test.py` include safe motor-stop handling on exit/interrupt

---

Happy hacking!
