# Shared robot hardware configuration for Spring Showdown 2026
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase

# Hub
hub = PrimeHub()

# Motors (adjust ports if your build changes)
leftdrive_motor = Motor(Port.E)
rightdrive_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
leftarm_motor = Motor(Port.B)
rightarm_motor = Motor(Port.F)

# Drive base configuration (tune to your robot)
drive_base = DriveBase(leftdrive_motor, rightdrive_motor, wheel_diameter=62.5, axle_track=100)  # mm  # mm
# Default motion settings (can be changed per launch)
drive_base.settings(
    straight_speed=800,
    straight_acceleration=800,
    turn_rate=100,
    turn_acceleration=900,
)

# Gyro/IMU setup
hub.imu.reset_heading(0)

# Global heading target accumulator used by gyro turns
global_angle = 0
