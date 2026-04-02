# Launch 2 – Refactored from m2.py
from pybricks.tools import run_task, multitask
from robot import drive_base, leftarm_motor, rightarm_motor
from movements import turnwithgyro, pause, set_drive_settings


async def main():
    # Go forward and dump boulders
    await drive_base.straight(460)
    await rightarm_motor.run_angle(500, -300)
    await pause(250)

    # Move forward while lifting arm back up (concurrently)
    await multitask(drive_base.straight(300), rightarm_motor.run_angle(1000, 300))

    # Align and operate left arm repeatedly
    await turnwithgyro(45, 100)
    await drive_base.straight(10)

    for _ in range(3):
        await leftarm_motor.run_angle(1100, 900)
        await leftarm_motor.run_angle(1100, -900)

    await turnwithgyro(15, 150)

    # Adjust speed for return
    set_drive_settings(straight_speed=800, straight_acceleration=300, turn_rate=150, turn_acceleration=150)
    await drive_base.straight(-520)

    # Restore default settings
    set_drive_settings()


run_task(main())
