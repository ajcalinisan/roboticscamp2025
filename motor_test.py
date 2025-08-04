
from gpiozero import Motor
from time import sleep

# Define motors (adjust pins if different)
right_motor = Motor(forward=17, backward=18)
left_motor = Motor(forward=22, backward=23)

# Move forward
print("Moving forward...")
left_motor.forward(.7)
right_motor.forward()
sleep(4)

# Move backward
print("Moving backward...")
left_motor.backward(.7)
right_motor.backward()
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
