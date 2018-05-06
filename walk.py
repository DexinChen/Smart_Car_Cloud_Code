from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
import time
from time import sleep
import cv2
import cv2.cv as cv
import numpy as np
import picar

picar.setup()
# Show image captured by camera, True to turn on, youwill need #DISPLAY and it also slows the speed of tracking
show_image_enable   = False
draw_circle_enable  = False
scan_enable         = False
rear_wheels_enable  = True
front_wheels_enable = True
pan_tilt_enable     = True

#kernel = np.ones((5,5),np.uint8)
#img = cv2.VideoCapture(-1)

#SCREEN_WIDTH = 160
#SCREEN_HIGHT = 120
#img.set(3,SCREEN_WIDTH)
#img.set(4,SCREEN_HIGHT)
#CENTER_X = SCREEN_WIDTH/2
#CENTER_Y = SCREEN_HIGHT/2
#BALL_SIZE_MIN = SCREEN_HIGHT/10
#BALL_SIZE_MAX = SCREEN_HIGHT/3

# Filter setting, DONOT CHANGE
#hmn = 12
#hmx = 37
#smn = 96
#smx = 255
#vmn = 186
#vmx = 255

# camera follow mode:
# 0 = step by step(slow, stable),
# 1 = calculate the step(fast, unstable)
follow_mode = 1

MIDDLE_TOLERANT = 5
PAN_ANGLE_MAX   = 170
PAN_ANGLE_MIN   = 10
TILT_ANGLE_MAX  = 150
TILT_ANGLE_MIN  = 70
FW_ANGLE_MAX    = 90+30
FW_ANGLE_MIN    = 90-30

bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
picar.setup()

fw.offset = 0
fw.calibration()
pan_servo.offset = 0
tilt_servo.offset = 0

bw.speed = 40
#fw.turn(90)
pan_servo.write(90)
tilt_servo.write(90)
motor_speed = 60

def main():
    pan_angle = 90              # initial angle for pan
    tilt_angle = 90             # initial angle for tilt
    fw_angle = 90
    fw.turn_straight()
    
    while True:
        t_end = time.time() + 6
        while time.time() < t_end:
            fw.turn(100)
            bw.speed = 40
            bw.forward()
	bw.stop()
        pan_servo.write(60)
        sleep(2)
        tilt_servo.write(60)
        sleep(2)
        tilt_servo.write(90)
        sleep(2)
        tilt_servo.write(120)
        sleep(2)
        pan_servo.write(90)
        sleep(2)
        tilt_servo.write(60)
        sleep(2)
        tilt_servo.write(90)
        sleep(2)
        tilt_servo.write(120)
        sleep(2)
        pan_servo.write(150)
        sleep(2)
        tilt_servo.write(60)
        sleep(2)
        tilt_servo.write(90)
        sleep(2)
        tilt_servo.write(120)
        sleep(2)
        pan_servo.write(90)
        tilt_servo.write(90)
        t_end1 = time.time() + 6
        while time.time() < t_end1:
            fw.turn(60)
	    bw.speed = 40
            bw.backward()
	bw.stop()
        pan_servo.write(60)
        sleep(2)
        tilt_servo.write(60)
        sleep(2)
        tilt_servo.write(90)
        sleep(2)
        tilt_servo.write(120)
        sleep(2)
        pan_servo.write(90)
        sleep(2)
        tilt_servo.write(60)
        sleep(2)
        tilt_servo.write(90)
        sleep(2)
        tilt_servo.write(120)
        sleep(2)
        pan_servo.write(150)
        sleep(2)
        tilt_servo.write(60)
        sleep(2)
        tilt_servo.write(90)
        sleep(2)
        tilt_servo.write(120)
        sleep(2)
        pan_servo.write(90)
        tilt_servo.write(90)
def destroy():
    bw.stop()
    fw.turn_straight()
    #img.release()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        destroy()
