#Mission Code for The Silo And Forge
from pybricks.hubs import PrimeHub
from pybricks.parameters import Axis
from pybricks.tools import wait
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.robotics import DriveBase
from pybricks.tools import multitask, run_task


hub = PrimeHub()
# Wait for IMU to stabilize
print("Calibrating IMU...")
wait(1000)
# Reset IMU heading to 0
hub.imu.reset_heading(0)
print("IMU calibrated and heading reset.")

leftdrive_motor = Motor(Port.E)
leftarm_motor = Motor(Port.B)
rightarm_motor = Motor(Port.F)
rightdrive_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
use_gyro = True

drive_base = DriveBase(leftdrive_motor, rightdrive_motor, wheel_diameter=62.5, axle_track=100)
drive_base.settings(straight_speed=800, straight_acceleration=800, turn_rate=100, turn_acceleration=900)

hub.imu.reset_heading(0)

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
    start_heading = hub.imu.heading()    
    
    # Determine turn direction
    if target_degrees > 0:
        # Clockwise turn: left forward, right backward
        motor_left.run(-speed)
        motor_right.run(speed)
    else:
        # Counter-clockwise turn: left backward, right forward
        motor_left.run(speed)
        motor_right.run(-speed)

    # Track how much we've turned
    degrees_turned = 0
    last_heading = start_heading

    # Keep turning until we reach target
    while True:
        current_heading = hub.imu.heading()
        # Calculate chssnge since last reading
        delta = current_heading - last_heading

        # Fix wraparound if we crossed 0/360 boundary
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360
        
        # Accumulate the turn
        degrees_turned += delta
        last_heading = current_heading

        # Check if we've turned enough
        if abs(degrees_turned) >= abs(target_degrees) - 2:
            break
        
        await wait(10)  # Small delay to prevent busy-waiting

    # Stop motors with brake for precision
    motor_left.brake()
    motor_right.brake()


async def main():
    drive_base.settings(straight_speed=200, straight_acceleration=200, turn_rate=70, turn_acceleration=70)
    # Pass jig wall
    await drive_base.straight(50)
    # Curve, hit the relic off the pedestal and face temple gates
    await drive_base.arc(320, 130)
    # Approach temple gates and drop off lantern
    await drive_base.straight(40)
    # Back up to brush mission
    await drive_base.straight(-180)
    # Retrieve the brush
    await leftarm_motor.run_angle(1100, 1300)
    await leftarm_motor.run_angle(1100, -1000)
    # Back up to the pedestal
    await drive_base.straight(-55)
    # Drop off the idol
    await rightarm_motor.run_angle(1100, -500)
    # Back up a bit to confirm that the idol is on the pedestal
    await drive_base.straight(-45)
    # Return home without knowing idol off of the pedestal
    await tank_turn(hub, leftdrive_motor, rightdrive_motor, -120, 800)
    drive_base.settings(straight_speed=800, straight_acceleration=800, turn_rate=70, turn_acceleration=70)
    await drive_base.straight(400)
    

run_task(main())