#Mission Code for The Silo And Forge
from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis
from pybricks.tools import wait
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task

# Constants (adjust to match your physical robot)
DRIVING_WHEEL_DIAMETER = 62   # mm
DRIVING_WHEEL_SPACING = 112    # mm
DRIVING_WHEEL_MAX_SPEED = 100  # deg/s

hub = PrimeHub()
leftdrive_motor = Motor(Port.E)
leftarm_motor = Motor(Port.B)
rightarm_motor = Motor(Port.F)
rightdrive_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
use_gyro = True

drive_base = DriveBase(leftdrive_motor, rightdrive_motor, wheel_diameter=62.5, axle_track=100)
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

async def turn_arc(hub, leftdrive_motor, rightdrive_motor, turning_radius, turning_degrees, turning_speed):
    """
    Executes a precise gyro-controlled arc turn.
    
    Parameters:
    turning_radius (int): Distance from inner wheel to pivot center (mm).
    turning_degrees (int): Target degrees (Positive = Right/CW, Negative = Left/CCW).
    turning_speed (int): Base speed percentage (1 to 100).
    """
    if turning_degrees == 0:
        return

    # 1. Map 1-100 speed to actual motor deg/s (assuming ~1000 deg/s max for SPIKE motors)
    base_speed = (abs(turning_speed) / 100.0) * DRIVING_WHEEL_MAX_SPEED

    # 2. Calculate the speed differential based on wheel geometry
    # Outer wheel must travel a larger radius, so it spins faster
    inner_speed = base_speed
    outer_speed = base_speed * ((turning_radius + DRIVING_WHEEL_SPACING) / turning_radius)

    # 3. Assign speeds to correct motors based on direction
    # Positive degrees = Right Turn (Clockwise) -> Left wheel is outer, Right is inner
    if turning_degrees < 0:
        left_speed = outer_speed
        right_speed = inner_speed
    else:
        # Negative degrees = Left Turn (Counter-Clockwise) -> Right wheel is outer, Left is inner
        left_speed = inner_speed
        right_speed = outer_speed

    # 4. Initialize IMU
    hub.imu.reset_heading(0)
    await wait(50) # Allow IMU to stabilize

    # 5. Start the motors
    leftdrive_motor.run(left_speed)
    rightdrive_motor.run(right_speed)

    # 6. Monitor turn progress using robust signed checks
    if turning_degrees > 0:
        # Turning Right (Clockwise): heading increases toward a positive target
        while hub.imu.heading() < turning_degrees:
            await wait(10)
    else:
        # Turning Left (Counter-Clockwise): heading decreases toward a negative target
        while hub.imu.heading() > turning_degrees:
            await wait(10)

    # 7. Brake hard to maintain FLL precision
    leftdrive_motor.hold()
    rightdrive_motor.hold()

async def tank_turn(hub, motor_left, motor_right, target_degrees, speed):
    """
    Turn the robot using gyro feedback with proper angle wrapping.
    
    Args:
        hub: PrimeHub object
        motor_left: Left wheel Motor object
        motor_right: Right wheel Motor object
        target_degrees: Degrees to turn (positive = clockwise, negative = counter-clockwise)
        speed: Turn speed (1-100)
    """
    # Get starting heading
    speed = max(25, min(100, speed))  # Ensure speed is within reasonable bounds
    # Tolerance: 10% of target or 2 degrees, whichever is smaller
    tolerance = min(2, abs(target_degrees) * 0.1)

    # Determine turn direction
    if target_degrees > 0:
        # Clockwise turn: left forward, right backward
        motor_left.run(-speed)
        motor_right.run(speed)
    else:
        # Counter-clockwise turn: left backward, right forward
        motor_left.run(speed)
        motor_right.run(-speed)

    # Record starting heading
    start_heading = hub.imu.heading()

    # Wait until we've turned far enough
    while abs(hub.imu.heading() - start_heading) < abs(target_degrees) - tolerance:
        await wait(10)

    # Stop motors with brake for precision
    motor_left.brake()
    motor_right.brake()

async def main():
    # Lift arm as approaching the mission
    await multitask(rightarm_motor.run_angle(1100, 400), drive_base.straight(425))
    # Turning while using the arm to carry the miner to the other side
    await turnwithgyro(-40, 50)
    await drive_base.straight(40)
    await turnwithgyro(-10, 50)
    await drive_base.straight(10)
    wait(1000)
    # Back up and lift arm
    await drive_base.straight(-100)
    await rightarm_motor.run_angle(1100, -400)
    # Get in position to drop the site markers
    await turnwithgyro(-10, 50)
    await drive_base.straight(220)
    await turnwithgyro(45, 80)
    await drive_base.straight(-30)
    await turnwithgyro(45, 50)
    await drive_base.straight(30)
    await drive_base.straight(5)
    # Drop site markers
    await leftarm_motor.run_angle(-400, 300)
    

run_task(main())