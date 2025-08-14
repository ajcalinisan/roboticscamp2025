# Author: AJ Calinisan
# Email: acalinis@uci.edu

To clone this repo and run it:

```bash
git clone https://rasp@github.com/ajcalinisan/roboticscamp2025.git
cd roboticscamp2025
python3 soccer_bot.py
```
To delete the roboticscamp2025 directory
```bash
cd ~
sudo rm -rf roboticscamp2025
```
| Raspberry Pi Pin | Function      | Connects To               |
| ---------------- | ------------- | ------------------------- |
| Pin 11 (GPIO17)  | Motor Left A  | IN1                       |
| Pin 12 (GPIO18)  | Motor Left B  | IN2                       |
| Pin 15 (GPIO22)  | Motor Right A | IN3                       |
| Pin 16 (GPIO23)  | Motor Right B | IN4                       |
| Pin 2 or 4       | 5V Power      | Motor driver VCC          |
| Pin 6 or 9       | Ground        | Motor driver GND          |

# SoccerBot: Raspberry Pi 4 Autonomous Ball-Tracking Rover

This project enables a Raspberry Pi 4-powered robot to:

1. **Test motors** using `motor_test.py`  
2. **Track a yellow-green pickleball** with `green_ball_tracker.py`  
3. **Track a red wiffleball** with `red_ball_tracker.py`  
4. **Chase and push the red ball** autonomously using `soccer_bot.py`  

---

## 🛠 Hardware Requirements

•	Raspberry Pi 4 and SD Card
•	9V Battery
•	Power Bank for Powering Pi
•	Rover Chassis
•	Bold-colored Ball to chase
•	Camera Module

Motor Components:
•	L293D Motor Drivers
•	2x Yellow Gearbox Motors with Yellow Wheels
•	1x Castor Wheel

Cables: 
•	2x Male to Female Dupont Cables
•	4x Female to Female Dupont Cables
• USB A to USB C	
•	9V Battery to dupont cable adapter 
•	HDMI Cable (For monitor setup)
•	Raspberry Pi power adapter (For monitor setup)

Tools:
• Screwdrivers
• Pliers 

---

## 📁 Project Files

### `motor_test.py`

Moves the robot:

- Forward
- Backward
- Left turn
- Right turn  
Each for 4 seconds.

### `green_ball_tracker.py`

Tracks a yellow-green pickleball using HSV filtering, drawing a circle around the largest matching object.

### `red_ball_tracker.py`

Tracks a red wiffleball using HSV filtering, drawing a circle around the largest matching object.

### `soccer_bot.py`

Full autonomous soccer mode for **red wiffleball**:

- Spins to search for the ball
- Centers itself
- Moves forward and pushes the ball

---

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

If nothing appears, re-check cable seating, enable the camera in raspi-config, and reboot the Pi.

---

## 🧪 Run Scripts

### Motor Test:

```bash
python3 motor_test.py
```

### Yellow-Green Ball Tracker:

```bash
python3 green_ball_tracker.py
```

### Red Ball Tracker:

```bash
python3 red_ball_tracker.py
```

Click anywhere in the camera window to see HSV values.

### Soccer Bot (Red Ball):

```bash
python3 soccer_bot.py
```

Robot will:

- Search for the red ball
- Center on it
- Move forward and push it

---

## 🖥️ Running Soccer Bot Without Camera View

If you want the robot to run without opening a camera window (for example, when running on startup),  
open `soccer_bot.py` and **comment out** these three lines at the bottom of the loop:

```python
cv2.imshow("Soccer Bot View", frame)
if cv2.waitKey(1) == 27:
    break
```

To **comment out** a line in Python, put a `#` at the start of it, like this:

```python
# cv2.imshow("Soccer Bot View", frame)
# if cv2.waitKey(1) == 27:
#     break
```

This will prevent the Pi from trying to open a video window.

---

## 🚀 Run Soccer Bot on Startup

✅ Method: Crontab (@reboot)  
Open crontab:

```bash
crontab -e
```
When it says Choose 1-3 [1]:
Type:
```
1
```
and press enter

At the bottom, add this line (adjust the path):

```bash
@reboot python3 /home/raspberry/roboticscamp2025/soccer_bot.py &
```

`&` lets it run in the background so the boot process doesn't hang.

Save and exit (`Ctrl+O`, `Enter`, then `Ctrl+X` if using nano).

(Optional but recommended) Test it by rebooting:

```bash
sudo reboot
```

⚠️ **Important:**  
If running on startup, it is highly recommended that you comment out the camera display lines as shown in the [Running Soccer Bot Without Camera View](#️running-soccer-bot-without-camera-view) section above.

---

## 🛑 Stopping the Startup Task

If `soccer_bot.py` is running in the background after boot, you can stop it with:

```bash
ps aux | grep soccer_bot.py
```

You’ll see a list of processes. Look for the line showing:

```
python3 /home/raspberry/roboticscamp2025/soccer_bot.py
```

Note the **PID** (the number in the second column), then run:

```bash
kill PID
```

Example:

```bash
kill 1234
```

This will stop the soccer bot program until the next reboot (unless you remove it from crontab).

---

## ❌ Removing Soccer Bot from Startup

If you want to completely disable it from auto-starting at boot:

```bash
crontab -e
```

Find the line:

```bash
@reboot python3 /home/raspberry/roboticscamp2025/soccer_bot.py &
```

Delete that line, save (`Ctrl+O`, `Enter`) and exit (`Ctrl+X`).

The program will no longer launch automatically when the Raspberry Pi starts.

---

## ⚙️ Recommended HSV Values

Our code uses these HSV values to track a ball based on its color.  
You may adjust the HSV thresholds in `green_ball_tracker.py`, `red_ball_tracker.py`, and `soccer_bot.py`:

For Yellow-Green Pickleball

```python
lower_hsv = np.array([28, 140, 140])
upper_hsv = np.array([43, 247, 255])
```

For Red Wiffleball

```python
lower_hsv = np.array([172, 130, 50])
upper_hsv = np.array([178, 247, 255])
```

Use either tracker script and click in the camera window to identify HSV values for your ball.

---

## 🤖 Notes

- The left motor on some builds is faster/slower; `soccer_bot.py` includes compensation
- Modify `TURN_TIME` and `TURN_SPEED` for smoother movement
- Make sure your motor driver has:
  - `5V` input for logic (usually from Pi)
  - `9–12V` input for motors (9V Battery used in this build)

---

## 🧼 Clean Exit

Press `ESC` to stop tracking in any script. Motors will stop automatically with `stop()`.

---

Happy hacking!
