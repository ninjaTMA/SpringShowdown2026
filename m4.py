from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis
from pybricks.tools import wait
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task

hub = PrimeHub()
leftdrive_motor = Motor(Port.E)
leftarm_motor = Motor(Port.B)
rightarm_motor = Motor(Port.F)
rightdrive_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
use_gyro = True

drive_base = DriveBase(leftdrive_motor, rightdrive_motor, wheel_diameter=62.5, axle_track=95)
drive_base.settings(straight_speed=600, straight_acceleration=800, turn_rate=100, turn_acceleration=900)

hub.imu.reset_heading(0)
global global_angle
global_angle = 0

async def turnwithgyro(target_angle, turn_speed):
    global global_angle
    starting_yaw = hub.imu.heading()
    global_angle += target_angle
    
    if(target_angle>0):
        leftdrive_motor.run(-turn_speed)
        rightdrive_motor.run(turn_speed)
        while True:
            current = hub.imu.heading()
            if current >= global_angle-3:
                break
    else:
        leftdrive_motor.run(turn_speed)
        rightdrive_motor.run(-turn_speed)
        while True:
            current = hub.imu.heading()
            if current <= global_angle+3:
                break
    leftdrive_motor.stop()
    rightdrive_motor.stop()

    
async def main():
    await drive_base.straight(815)
    await turnwithgyro(-90, 150)
    await drive_base.straight(450)
    await drive_base.straight(-75)
    await wait(300)
    await drive_base.straight(235)
    await turnwithgyro(-36005, 150)
    await drive_base.straight(280)
    await drive_base.straight(-60)


run_task(main())