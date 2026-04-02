# Reusable movement utilities shared across launches
from pybricks.tools import wait
from robot import hub, drive_base, leftdrive_motor, rightdrive_motor

# Use the global_angle from robot to accumulate heading
from robot import global_angle as _global_angle_ref


def set_drive_settings(straight_speed=800, straight_acceleration=800, turn_rate=100, turn_acceleration=900):
    drive_base.settings(
        straight_speed=straight_speed,
        straight_acceleration=straight_acceleration,
        turn_rate=turn_rate,
        turn_acceleration=turn_acceleration,
    )


async def turnwithgyro(target_angle: int, turn_speed: int, tolerance: int = 3):
    """
    Gyro-based point turn by target_angle degrees at turn_speed.
    Keeps track of cumulative heading to avoid wrap issues.
    Positive angle turns right; negative turns left.
    """
    # Access and update the shared global angle via robot module state
    from robot import global_angle as ga

    ga += target_angle
    # Write back the updated value
    import robot

    robot.global_angle = ga

    if target_angle > 0:
        # Turn right
        leftdrive_motor.run(-turn_speed)
        rightdrive_motor.run(turn_speed)
        while True:
            current = hub.imu.heading()
            if current >= ga - tolerance:
                break
    else:
        # Turn left
        leftdrive_motor.run(turn_speed)
        rightdrive_motor.run(-turn_speed)
        while True:
            current = hub.imu.heading()
            if current <= ga + tolerance:
                break

    leftdrive_motor.stop()
    rightdrive_motor.stop()


async def pause(ms: int):
    await wait(ms)
