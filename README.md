# SpringShowdown2026
A compliation of our team's pybricks code for Spring Showdown 2026

## Structure

- robot.py — shared robot hardware (hub, motors, drive base)
- movements.py — shared reusable moves (e.g., gyro turns)
- launches/ — one file per competition launch (trip)
	- launch1.py, launch2.py, ...
- finalmissions.py — on-hub menu to pick a launch

## Add a New Launch

1. Create a new file in `launches/` (e.g., `launches/launch3.py`).
2. Import shared items:
	 `from robot import drive_base, leftarm_motor, rightarm_motor`
	 `from movements import turnwithgyro, pause`
3. Implement `async def main(): ...` and end with `run_task(main())`.
4. Add the new option in `finalmissions.py` to import your launch.
