#Mission Code for The Silo And Forge
from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis
from pybricks.tools import wait
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task
from utils import turn_with_gyro

hub = PrimeHub()
leftdrive_motor = Motor(Port.E)
leftarm_motor = Motor(Port.B)
rightarm_motor = Motor(Port.F)
rightdrive_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
use_gyro = True

drive_base = DriveBase(leftdrive_motor, rightdrive_motor, wheel_diameter=62.5, axle_track=100)
drive_base.settings(straight_speed=800, straight_acceleration=800, turn_rate=100, turn_acceleration=900)

hub.imu.reset_heading(0)


### EXAMPLE CODE ###
###drive_base.straight(300)
###turn_with_gyro(hub, leftdrive_motor, rightdrive_motor, 90,100)
###leftarm_motor.run_angle(500, 300)
###drive_base.straight(150)
###drive_base.straight(-450)

async def main():
    drive_base.settings(straight_speed=200, straight_acceleration=200, turn_rate=70, turn_acceleration=70)
    await drive_base.straight(60)
    await drive_base.arc(345, 115)
    await drive_base.straight(50)
    await drive_base.straight(-160)
    await leftarm_motor.run_angle(1100, 1300)
    await leftarm_motor.run_angle(1100, -1000)
    await drive_base.straight(-55)
    await rightarm_motor.run_angle(1100, -500)
    await drive_base.straight(-20)
    await turn_with_gyro(hub, leftdrive_motor, rightdrive_motor, -25, 100)
    # await drive_base.straight(-100)
    

"""    #drive forward to the Replace the Relic mission
    drive_base.settings(straight_speed=300, straight_acceleration=300, turn_rate=70, turn_acceleration=70)
    await drive_base.straight(97.5)
    await turn_with_gyro(hub, leftdrive_motor, rightdrive_motor, 55, 100)
    await drive_base.straight(360)
    await turn_with_gyro(hub, leftdrive_motor, rightdrive_motor, -55, 50)
    await drive_base.straight(85)
    #lower idol onto pedestal
    await rightarm_motor.run_angle(1100, -500)
    await drive_base.straight(75)
    #retrieve LEGOlith
    await leftarm_motor.run_angle(1100, 1600)
    await leftarm_motor.run_angle(1100, -1000)
    #deliver lantern to pedestal
    await drive_base.straight(150)
    await turn_with_gyro(hub, leftdrive_motor, rightdrive_motor, -5, 50)
    await drive_base.straight(-70)
    #return to base
    drive_base.settings(straight_speed=800, straight_acceleration=800, turn_rate=100, turn_acceleration=100)
    await turn_with_gyro(hub, leftdrive_motor, rightdrive_motor, 40, 199)
    await drive_base.straight(-700)
"""
run_task(main())