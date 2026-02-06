from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis
from pybricks.tools import wait
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase

hub = PrimeHub()
left_motor = Motor(Port.C)
arm_motor = Motor(Port.A)
right_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
use_gyro = True

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=100)
hub.imu.reset_heading(0)
global global_angle
global_angle = 0
def drive(speed):
    left_motor.run(speed)
    right_motor.run(speed)
    print("I WAS HERE")
def turnwithgyro(target_angle, turn_speed):
    global global_angle
    starting_yaw = hub.imu.heading()
    global_angle += target_angle
    
    if(target_angle>0):
        left_motor.run(-turn_speed)
        right_motor.run(turn_speed)
        while True:
            current = hub.imu.heading()
            if current >= global_angle:
                break
    else:
        left_motor.run(turn_speed)
        right_motor.run(-turn_speed)
        while True:
            current = hub.imu.heading()
            if current <= global_angle:
                break
    left_motor.stop()
    right_motor.stop()


drive_base.straight(300)
turnwithgyro(90,200)
arm_motor.run_angle(500, 300)
drive_base.straight(150)
drive_base.straight(-450)



