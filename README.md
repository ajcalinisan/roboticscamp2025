To clone this repo and run it:

```bash
git clone https://rasp@github.com/ajcalinisan/roboticscamp2025.git
cd soccerbot-pi3
python3 soccer_bot.py
```

# SoccerBot: Raspberry Pi 3 Autonomous Ball-Tracking Rover

This project enables a Raspberry Pi 3-powered robot to:

1. **Test motors** using `motor_test.py`
2. **Track a yellow-green pickleball** with `ball_tracker.py`
3. **Chase and push the ball** autonomously using `soccer_bot.py`

---

## 🛠 Hardware Requirements

- Raspberry Pi 3 (Model B/B+)
- Raspberry Pi OS (Bullseye recommended)
- Pi Camera Module (CSI connector)
- L298N Motor Driver
- 2x DC Motors + wheels
- Power Bank (5V 2.4A recommended) for Pi power
- 9V Battery and Dupont Connector
- Jumper wires, breadboard (optional)

---

## 📁 Project Files

### `motor_test.py`

Moves the robot:

- Forward
- Backward
- Left turn
- Right turn 
For 4 seconds each.

### `ball_tracker.py`

Tracks a yellow-green pickleball using HSV filtering, drawing a circle around the largest matching object.

### `soccer_bot.py`

Full autonomous soccer mode for Yellow-Green Pickleball:

- Spins to search for the ball
- Centers itself
- Moves forward and pushes the ball

---
### `startup_soccer.py`

Autonomous soccer with Red Ball

## 🧪 Setup Instructions

### 🔌 Enable Interfaces

```bash
sudo raspi-config
```

- Enable **Camera** (under Interface Options)
- Enable **SSH** if remote access is needed
https://sourceforge.net/projects/vcxsrv/
http://www.straightrunning.com/XmingNotes/
https://www.realvnc.com/en/connect/download/viewer/
### 📦 Install Required Packages

```bash
sudo apt update
sudo apt install python3-opencv python3-gpiozero python3-picamera2
```

> If OpenCV is not found:

```bash
pip install opencv-python
```

### 🖼️ Test Camera

```bash
libcamera-hello
```

If nothing appears, re-check cable seating, enable the camera in raspi-config, and reboot the pi.

---

## 🧪 Run Scripts

### Motor Test:

```bash
python3 motor_test.py
```

### Ball Tracker:

```bash
python3 ball_tracker.py
```

Click anywhere in the camera window to see HSV values.

### Soccer Bot:

```bash
python3 soccer_bot.py
```

Robot will:

- Search for the ball
- Center on it
- Move forward and push it

---
### Run Startup_Soccer on Startup
✅ Method: Crontab (@reboot)
Open crontab:

```bash
crontab -e
```
At the bottom, add this line (adjust the path):
```
@reboot python3 /home/pi/roboticscamp2025/soccer_bot.py &
```
& lets it run in the background so the boot process doesn't hang.

Save and exit (Ctrl+O, Enter, then Ctrl+X if using nano).

(Optional but recommended) Test it by rebooting:

```bash
sudo reboot
```

## ⚙️ Recommended HSV Values

You may adjust the HSV thresholds in `ball_tracker.py` and `soccer_bot.py`:

For Yellow-Green Pickleball
```python
lower_hsv = np.array([28, 140,140])
upper_hsv = np.array([43, 247, 255])
```
For Red Wiffleball
```
lower_hsv = np.array([172, 130, 50])
upper_hsv = np.array([178, 247, 255])
```
Use `ball_tracker.py` and click to identify HSV values of your ball.

---

## 🤖 Notes

- The left motor on some builds is faster/slower; `soccer_bot.py` includes compensation
- Modify `TURN_TIME` and `TURN_SPEED` for smoother movement
- Make sure your motor driver has:
  - `5V` input for logic (usually 5V from Pi)
  - `12V` input for motor (9V Battery)

---


## 🧼 Clean Exit

Press `ESC` to stop tracking in any script. Motors will stop automatically with `stop()`.

---

Happy hacking!

