from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis
from pybricks.tools import wait
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase

hub = PrimeHub()
left_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.D)

hub.imu.reset_heading(0)
global global_angle
global_angle = 0
def turnwithgyro(target_angle, turn_speed):
    global global_angle
    starting_yaw = hub.imu.heading()
    global_angle += target_angle
    
    if(target_angle>0):
        left_motor.run(turn_speed)
        right_motor.run(-turn_speed)
        while True:
            current = hub.imu.heading()
            if current >= global_angle:
                break
    else:
        left_motor.run(-turn_speed)
        right_motor.run(turn_speed)
        while True:
            current = hub.imu.heading()
            if current <= global_angle:
                break
    left_motor.stop()
    right_motor.stop()

for i in range(2):
    turnwithgyro(90, 150)
    wait(1000)
    turnwithgyro(-90, 150)
    wait(1000)




