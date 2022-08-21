from machine import Pin
from time import sleep
from sys import exit

__version__ = "0.1.0"
__author__ = "Finn Drünert"


class StepperMotor:

    DIRECTION_FORWARD = 0
    DIRECTION_BACKWARD = 1

    STEP_MODE_FULL_ONE_PHASE = 2
    STEP_MODE_FULL_TWO_PHASE = 3
    STEP_MODE_HALF = 4

    def __init__(self, gear_ratio: int, stride_angle: float, **motor_coil_pins):

        """
        If you dont self.clear_pins() one or more motor coils will consume power and will produce heat
        motor_coil_pins: must be given like {<engine controler pin name (e.g. IN1)>: <coresponding pin number on microcontroler>}
        """

        for IN in motor_coil_pins:
            if (not IN.startswith("IN")) and (type(IN.split("IN")[1]) is not int):
                raise Exception(
                    "motor_coil_pins must be given like {<engine controler pin name (e.g. IN1)>: <coresponding pin number on microcontroler>}"
                )

        self.pins = [
            Pin(motor_coil_pins[IN], Pin.OUT) for IN in sorted(motor_coil_pins)
        ]
        self.full_step_state = 0
        self.half_step_state = 0
        self.stride_angle = stride_angle
        self.gear_ratio = gear_ratio
        self.motor_coils = len(motor_coil_pins)
        self.steps_per_revolution = 360 / stride_angle
        self.output_shaft_steps_per_revolution = self.steps_per_revolution * gear_ratio
        self.rotation_per_step = 360 / self.output_shaft_steps_per_revolution
        self.half_step_sequence = self.__generate_half_step_sequence()
        self.max_steps_per_second = 1 / (0.001 * self.motor_coils)
        self.max_angular_velocity = self.max_steps_per_second * self.rotation_per_step
        self.printed_speed_warning = False

    def __del__(self):
        self.clear_pins()

    def clear_pins(self):
        for pin in self.pins:
            pin.off()

    def __generate_half_step_sequence(self):

        sequence = []
        for i in range(self.motor_coils * 2):
            seq = [0] * self.motor_coils

            if i == self.motor_coils * 2 - 1:
                seq[0] = 1
                seq[-1] = 1
                sequence.append(seq)
                continue

            if i % 2 == 0:
                seq[i // 2] = 1
            else:
                seq[(i - 1) // 2] = 1
                seq[i // 2 + 1] = 1
            sequence.append(seq)

        return sequence

    def full_step_one_phase(self, direction: int = DIRECTION_FORWARD):

        pins = self.pins if direction == self.DIRECTION_FORWARD else self.pins[::-1]
        for i, pin in enumerate(pins):
            pin.value(1 if i == self.full_step_state else 0)
            sleep(0.001)

        self.full_step_state += 1
        if self.full_step_state == self.motor_coils:
            self.full_step_state = 0

    def full_step_two_phase(self, direction: int = DIRECTION_FORWARD):

        pins = self.pins if direction == self.DIRECTION_FORWARD else self.pins[::-1]
        for i, pin in enumerate(pins):
            pin.value(
                1
                if i == self.full_step_state
                or i == self.full_step_state + 1
                or (self.full_step_state == self.motor_coils - 1 and i == 0)
                else 0
            )
            sleep(0.001)

        self.full_step_state += 1
        if self.full_step_state == self.motor_coils:
            self.full_step_state = 0

    def half_step(self, direction: int = DIRECTION_FORWARD):

        pins = self.pins if direction == self.DIRECTION_FORWARD else self.pins[::-1]
        for i, pin in enumerate(pins):
            pin.value(self.half_step_sequence[self.half_step_state][i])
            sleep(0.001)

        self.half_step_state += 1
        if self.half_step_state == self.motor_coils * 2:
            self.half_step_state = 0

    def step(
        self,
        step_mode: int = STEP_MODE_FULL_ONE_PHASE,
        direction: int = DIRECTION_FORWARD,
    ):
        if step_mode == self.STEP_MODE_FULL_ONE_PHASE:
            self.full_step_one_phase(direction=direction)
        elif step_mode == self.STEP_MODE_FULL_TWO_PHASE:
            self.full_step_two_phase(direction=direction)
        elif step_mode == self.STEP_MODE_HALF:
            self.half_step(direction=direction)
        else:
            raise Exception("Invalid mode")

    def turn_output_shaft(
        self,
        steps: int,
        steps_per_second: int,
        step_mode: int = STEP_MODE_FULL_ONE_PHASE,
        direction: int = DIRECTION_FORWARD,
    ):

        if (
            steps_per_second > self.max_steps_per_second
            and not self.printed_speed_warning
        ):
            print(
                f"Warning: {self.max_steps_per_second}steps/second is the maximum speed (requested {steps_per_second})"
            )
            self.printed_speed_warning = True

        delay = 1 / steps_per_second - 0.001 * self.motor_coils

        if delay < 0:
            delay = 0

        for step in range(steps):
            self.step(step_mode=step_mode, direction=direction)
            sleep(delay)

    def turn_output_shaft_angle(
        self,
        degree: float,
        steps_per_second: int,
        step_mode: int = STEP_MODE_FULL_ONE_PHASE,
    ):

        """
        Turn the output shaft by a certain angle
        Use negativ degrees to rotate backwards
        """

        direction = self.DIRECTION_FORWARD

        if degree < 0:
            degree *= -1
            direction = self.DIRECTION_BACKWARD

        steps = degree * self.stride_angle

        if step_mode == self.STEP_MODE_HALF:
            steps *= 2

        angle_loss = abs(int(steps) - steps) * self.rotation_per_step

        self.turn_output_shaft(
            steps=int(steps),
            steps_per_second=steps_per_second,
            step_mode=step_mode,
            direction=direction,
        )

        return angle_loss

    def turn_output_shaft_angular_velocity(
        self,
        degree: float,
        angular_velocity: float,
        step_mode: int = STEP_MODE_FULL_ONE_PHASE,
    ):

        """
        Turn the output shaft by a certain angle with a certain angular velocity
        Use negativ degrees to rotate backwards
        angular_velocity: <angle>/second
        """

        if angular_velocity < self.rotation_per_step:
            raise Exception(
                "The angular velocity must be grater than the rotation per step"
            )

        if angular_velocity > self.max_angular_velocity:
            print(
                f"Warning: {self.max_angular_velocity}°/s is the maximum angular velocity (requested {angular_velocity}°/s)"
            )
            steps_per_second = self.max_steps_per_second
        else:
            steps_per_second = angular_velocity // self.rotation_per_step

        if step_mode == self.STEP_MODE_HALF:
            steps_per_second *= 2

        return self.turn_output_shaft_angle(
            degree=degree, steps_per_second=steps_per_second, step_mode=step_mode
        )

    def rotate_forever(
        self,
        steps_per_second: int,
        step_mode: int = STEP_MODE_FULL_ONE_PHASE,
        direction: int = DIRECTION_FORWARD,
    ):
        turns = 0
        try:
            while True:
                self.turn_output_shaft(
                    self.output_shaft_steps_per_revolution,
                    steps_per_second=steps_per_second,
                    direction=direction,
                    step_mode=step_mode,
                )
                turns += 1
        except KeyboardInterrupt:
            self.clear_pins()
            exit()
