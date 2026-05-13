from pybricks.tools import wait

async def turn_with_gyro(hub, left_motor, right_motor, target_angle, turn_speed):
    if target_angle == 0:
        return

    angular_speed = abs(turn_speed)
    initial_heading = hub.imu.heading()
    target_degrees = abs(target_angle)
    tolerance = min(3.0, target_degrees * 0.25)
    stop_threshold = target_degrees - tolerance

    if target_angle > 0:
        left_motor.run(-angular_speed)
        right_motor.run(angular_speed)
        while True:
            current_heading = hub.imu.heading()
            delta_heading = (current_heading - initial_heading) % 360
            if delta_heading >= stop_threshold:
                break
            await wait(10)
    else:
        left_motor.run(angular_speed)
        right_motor.run(-angular_speed)
        while True:
            current_heading = hub.imu.heading()
            delta_heading = (initial_heading - current_heading) % 360
            if delta_heading >= stop_threshold:
                break
            await wait(10)

    left_motor.stop()
    right_motor.stop()