
from gpiozero import Motor
from time import sleep

# === Speed Compensation ===
# *YOU CAN CHANGE THESE*
RIGHT_SPEED = 1.0
LEFT_SPEED = 0.7  # 30% slower left motor

# Define motors (adjust pins if different)
right_motor = Motor(forward=26, backward=20)
left_motor = Motor(forward=19, backward=16)

# Move forward
print("Moving forward...")
left_motor.forward(LEFT_SPEED)
right_motor.forward(RIGHT_SPEED)
sleep(4)

# Move backward
print("Moving backward...")
left_motor.backward(LEFT_SPEED)
right_motor.backward(RIGHT_SPEED)
sleep(4)

# Turn left
print("Turning left...")
left_motor.backward()
right_motor.forward()
sleep(4)

# Turn right
print("Turning right...")
left_motor.forward()
right_motor.backward()
sleep(4)

# Stop
print("Stopping.")
left_motor.stop()
right_motor.stop()
