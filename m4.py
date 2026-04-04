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
    await drive_base.straight(818)
    await turnwithgyro(-90, 150)
    await drive_base.straight(480)
    await drive_base.straight(-115)
    await wait(300)
    await drive_base.straight(245)
    await turnwithgyro(-5, 150)
    await drive_base.straight(280)
    await drive_base.straight(-70)
    await turnwithgyro(-10, 150)
    await drive_base.straight(325)
    await turnwithgyro(15, 150)
    await drive_base.arc(-240, 70)
    await turnwithgyro(-10, 150)
    await drive_base.straight(-80)
    await rightarm_motor.run_angle(800, 635)
    await turnwithgyro(30, 500)
    wait(300)
    await turnwithgyro(-30, 500)
    await drive_base.straight(250)
    wait(300)
    await drive_base.straight(-85)
    await leftarm_motor.run_angle(-300, 200)
    await turnwithgyro(-70, 150)
    await drive_base.straight(800)


run_task(main())