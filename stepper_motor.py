import random

from RPi import GPIO

CLOCKWISE = 1
COUNTERCLOCKWISE = 0


class StepperMotor:
    # -----------------------------------------------------------------------------------------------------
    def __init__(self, motor_pins, end_pin,a_pin):
        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)
        self.motor_pins = motor_pins
        self.end_pin = end_pin
        self.a_pin=a_pin
        self.counter_A = 0
        self.counter_B = 0
        self.counter_I = 0
        self.max_A = 0
        self.cur_rel_pos = 0  # percent value >=0 <= 100
        self.last_signal_A = False

        # Set motor_pins as output
        print("Setup Motor pins"+str(self.motor_pins))
        for pin in self.motor_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
        # set end_pin as input
        GPIO.setup(self.end_pin, GPIO.IN)
        print("Setup endpin: "+str(self.end_pin))
        # set a_pin as input
        GPIO.setup(self.a_pin, GPIO.IN)
        print("Setup a_pin: " + str(self.a_pin))
        self.calibrate()

    # ---------------------------------------------------------------------------------------------------------
    def reset(self):  # move to real world 0 position
        while not self.check_end():
            self.step(COUNTERCLOCKWISE)
        self.counter_A = 0
        self.counter_B = 0
        self.counter_I = 0
        print("Motor " + str(self.motor_pins)+ " is reset")

    # -----------------------------------------------------------------------------------------------------
    def calibrate(self):
        self.reset()
        self.step(CLOCKWISE)
        while not self.check_end():
            self.read_counter_a(CLOCKWISE)
            self.step(CLOCKWISE)
        self.max_A = self.counter_A
        self.reset()
        print("Motor is calibrated. Max value of counter A is: " + str(self.max_A))

    # -----------------------------------------------------------------------------------------------------
    def step(self, direction):
        print("motor stepped in " + str(direction) + " direction")

    # ---------------------------------------------------------------------------------------------------------
    def go_position(self, new_rel_pos):
        assert new_rel_pos >= 0 & new_rel_pos <= 100
        delta = new_rel_pos - self.cur_rel_pos
        if delta != 0:
            self.move(delta)

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

    # -----------------------------------------------------------------------------------------------------
    def read_counter_a(self, direction):
        signal_a = self.read_signal_a()
        if signal_a != self.last_signal_A:
            if direction == CLOCKWISE:
                self.counter_A += 1
            else:
                self.counter_A -= 1
        self.last_signal_A = signal_a
        print("Counter A: " + str(self.counter_A))

    # -----------------------------------------------------------------------------------------------------
    def read_signal_a(self):
        #return bool((random.random() * 2) // 1)
        return GPIO.input(self.a_pin)

    # -----------------------------------------------------------------------------------------------------
    def check_end(self):
        #tmp = (random.random() * 1.1)
        #tmp = bool(tmp // 1)
        #return tmp
        return GPIO.input(self.end_pin)