# Launch 1 – Refactored from m1.py
from pybricks.tools import multitask, run_task
from robot import drive_base, leftarm_motor, rightarm_motor
from movements import turnwithgyro, pause


async def main():
    # Move forward and raise arm at the same time
    await multitask(drive_base.straight(395), rightarm_motor.run_angle(500, 300))
    # Wait for boulders to fall out
    await pause(1667)
    # Collect all boulders
    await drive_base.straight(65)
    # Drive back and wait
    await drive_base.straight(-345)


run_task(main())
