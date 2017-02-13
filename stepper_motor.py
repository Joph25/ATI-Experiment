import logging
from time import sleep, time

from RPi import GPIO

CLOCKWISE = 1
COUNTERCLOCKWISE = 0
MOTOR_WAIT_TIME = 0.01  # equals .01 seconds or 10 ms
PIN_TIMOUT = 30  # timout reading end_pin


class StepperMotor:
    # -----------------------------------------------------------------------------------------------------
    def __init__(self, motor_pins, end_pin, a_pin):
        self.motor_pins = motor_pins
        self.end_pin = end_pin
        self.a_pin = a_pin
        self.counter_A = 0
        self.counter_B = 0
        self.counter_I = 0
        self.max_A = 0
        self.cur_rel_pos = 0  # percent value >=0 <= 100
        self.last_signal_A = False

        # Use BCM GPIO references instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)
        # Set motor_pins as output
        logging.info("Setup Motor pins" + str(self.motor_pins))
        for pin in self.motor_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

        # set end_pin and a_pin as input
        logging.info("Setup end-pin and a-pin: " + str(self.end_pin) + " " + str(self.a_pin))
        GPIO.setup(self.end_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.a_pin, GPIO.IN)

        self.calibrate()

    # ---------------------------------------------------------------------------------------------------------
    def reset(self):  # move to real world 0 position
        start_time = time()
        while not self.check_end():
            self.step(COUNTERCLOCKWISE)
            # check for timeout
            if time() - start_time >= PIN_TIMOUT:
                raise Exception("no end_pin signal within: " + str(PIN_TIMOUT) + " seconds")
        self.counter_A = 0
        self.counter_B = 0
        self.counter_I = 0
        logging.info("Motor " + str(self.motor_pins) + " is reset")

    # -----------------------------------------------------------------------------------------------------
    def calibrate(self):
        self.reset()
        self.step(CLOCKWISE)
        while not self.check_end():
            self.read_counter_a(CLOCKWISE)
            self.step(CLOCKWISE)
        self.max_A = self.counter_A
        self.reset()
        logging.info("Motor is calibrated. Max value of counter A is: " + str(self.max_A))

    # -----------------------------------------------------------------------------------------------------
    def step(self, direction):
        # controlling a 4-wire bipolar stepper motor (A,notA,B,notB)
        # one phase mode
        if direction == CLOCKWISE:
            # step 1
            GPIO.output(self.motor_pins[0], True)
            GPIO.output(self.motor_pins[1], False)
            GPIO.output(self.motor_pins[2], False)
            GPIO.output(self.motor_pins[3], False)
            sleep(MOTOR_WAIT_TIME)
            # step 2
            GPIO.output(self.motor_pins[0], False)
            GPIO.output(self.motor_pins[1], False)
            GPIO.output(self.motor_pins[2], True)
            GPIO.output(self.motor_pins[3], False)
            sleep(MOTOR_WAIT_TIME)
            # step 3
            GPIO.output(self.motor_pins[0], False)
            GPIO.output(self.motor_pins[1], True)
            GPIO.output(self.motor_pins[2], False)
            GPIO.output(self.motor_pins[3], False)
            sleep(MOTOR_WAIT_TIME)
            # step 4
            GPIO.output(self.motor_pins[0], False)
            GPIO.output(self.motor_pins[1], False)
            GPIO.output(self.motor_pins[2], False)
            GPIO.output(self.motor_pins[3], True)
            sleep(MOTOR_WAIT_TIME)
        else:
            # step 4
            GPIO.output(self.motor_pins[0], False)
            GPIO.output(self.motor_pins[1], False)
            GPIO.output(self.motor_pins[2], False)
            GPIO.output(self.motor_pins[3], True)
            sleep(MOTOR_WAIT_TIME)
            # step 3
            GPIO.output(self.motor_pins[0], False)
            GPIO.output(self.motor_pins[1], True)
            GPIO.output(self.motor_pins[2], False)
            GPIO.output(self.motor_pins[3], False)
            sleep(MOTOR_WAIT_TIME)
            # step 2
            GPIO.output(self.motor_pins[0], False)
            GPIO.output(self.motor_pins[1], False)
            GPIO.output(self.motor_pins[2], True)
            GPIO.output(self.motor_pins[3], False)
            sleep(MOTOR_WAIT_TIME)
            # step 1
            GPIO.output(self.motor_pins[0], True)
            GPIO.output(self.motor_pins[1], False)
            GPIO.output(self.motor_pins[2], False)
            GPIO.output(self.motor_pins[3], False)
            sleep(MOTOR_WAIT_TIME)
        # reset all motor pins to low
        for pin in self.motor_pins:
            GPIO.output(pin, False)
        logging.debug("Motor stepped in " + str(direction) + " direction")

    # ---------------------------------------------------------------------------------------------------------
    def go_position(self, new_rel_pos):
        assert new_rel_pos >= 0 & new_rel_pos <= 100
        delta = new_rel_pos - self.cur_rel_pos
        if delta != 0:
            self.move(delta)
        logging.debug("Motor moved to position: " + str(new_rel_pos))

    # -----------------------------------------------------------------------------------------------------
    def move(self, delta):
        if delta > 0:
            direction = CLOCKWISE
        else:
            direction = COUNTERCLOCKWISE
        counter_start = self.counter_A
        self.read_counter_a(direction)
        while (self.counter_A - counter_start) < delta:
            self.step(direction)
            self.read_counter_a(direction)
        logging.debug("Motor moved: " + str(delta))

    # -----------------------------------------------------------------------------------------------------
    def read_counter_a(self, direction):
        signal_a = self.read_signal_a()
        if signal_a != self.last_signal_A:
            if direction == CLOCKWISE:
                self.counter_A += 1
            else:
                self.counter_A -= 1
        self.last_signal_A = signal_a
        logging.info("Counter A: " + str(self.counter_A))

    # -----------------------------------------------------------------------------------------------------
    def read_signal_a(self):
        return GPIO.input(self.a_pin)

    # -----------------------------------------------------------------------------------------------------
    def check_end(self):
        return GPIO.input(self.end_pin)

    # -----------------------------------------------------------------------------------------------------
    def __del__(self):
        GPIO.cleanup()
