import asyncio
import importlib
import sys
import types
import unittest


def _install_fake_pybricks_modules():
    pybricks = types.ModuleType("pybricks")
    pybricks.__path__ = []

    hubs = types.ModuleType("pybricks.hubs")
    hubs.PrimeHub = object

    parameters = types.ModuleType("pybricks.parameters")
    parameters.Axis = object
    parameters.Port = object
    parameters.Direction = object

    async def wait(ms):
        return

    tools = types.ModuleType("pybricks.tools")
    tools.wait = wait
    tools.multitask = lambda *args, **kwargs: None
    tools.run_task = lambda *args, **kwargs: None

    pupdevices = types.ModuleType("pybricks.pupdevices")
    pupdevices.Motor = object

    robotics = types.ModuleType("pybricks.robotics")
    robotics.DriveBase = object

    sys.modules["pybricks"] = pybricks
    sys.modules["pybricks.hubs"] = hubs
    sys.modules["pybricks.parameters"] = parameters
    sys.modules["pybricks.tools"] = tools
    sys.modules["pybricks.pupdevices"] = pupdevices
    sys.modules["pybricks.robotics"] = robotics


class FakeMotor:
    def __init__(self):
        self.calls = []

    def run(self, speed):
        self.calls.append(("run", speed))

    def stop(self):
        self.calls.append(("stop",))


class FakeIMU:
    def __init__(self, headings):
        self._headings = iter(headings)

    def heading(self):
        return next(self._headings)


class FakeHub:
    def __init__(self, headings):
        self.imu = FakeIMU(headings)


class TurnWithGyroTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _install_fake_pybricks_modules()
        if "utils" in sys.modules:
            del sys.modules["utils"]
        cls.utils = importlib.import_module("utils")

    async def _dummy_wait(self, _ms):
        return

    def setUp(self):
        self.utils.wait = self._dummy_wait

    def test_turn_positive_wraps_at_zero(self):
        hub = FakeHub([355, 358, 359, 1, 5])
        left_motor = FakeMotor()
        right_motor = FakeMotor()

        asyncio.run(self.utils.turn_with_gyro(hub, left_motor, right_motor, 10, 100))

        self.assertEqual(left_motor.calls[0], ("run", -100))
        self.assertEqual(right_motor.calls[0], ("run", 100))
        self.assertEqual(left_motor.calls[-1], ("stop",))
        self.assertEqual(right_motor.calls[-1], ("stop",))

    def test_turn_negative_wraps_at_zero(self):
        hub = FakeHub([5, 2, 0, 359, 355])
        left_motor = FakeMotor()
        right_motor = FakeMotor()

        asyncio.run(self.utils.turn_with_gyro(hub, left_motor, right_motor, -10, 100))

        self.assertEqual(left_motor.calls[0], ("run", 100))
        self.assertEqual(right_motor.calls[0], ("run", -100))
        self.assertEqual(left_motor.calls[-1], ("stop",))
        self.assertEqual(right_motor.calls[-1], ("stop",))

    def test_turn_zero_angle_does_nothing(self):
        hub = FakeHub([0])
        left_motor = FakeMotor()
        right_motor = FakeMotor()

        asyncio.run(self.utils.turn_with_gyro(hub, left_motor, right_motor, 0, 100))

        self.assertEqual(left_motor.calls, [])
        self.assertEqual(right_motor.calls, [])


if __name__ == "__main__":
    unittest.main()
