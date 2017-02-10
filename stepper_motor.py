import random

CLOCKWISE = 1
COUNTERCLOCKWISE = 0


class StepperMotor:
    # -----------------------------------------------------------------------------------------------------
    def __init__(self):
        self.counter_A = 0
        self.counter_B = 0
        self.counter_I = 0
        self.cur_rel_pos = 0  # percent value >=0 <= 100
        self.last_signal_A = False

    # ---------------------------------------------------------------------------------------------------------
    def reset(self):  # move to real world 0 position
        while not self.check_end():
            self.step(COUNTERCLOCKWISE)
        self.counter_A=0
        self.counter_B=0
        self.counter_I=0
        print("Motor is reset")

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
        self.read_counter_A(direction)
        while (self.counter_A - counter_start) < delta:
            self.step(direction)
            self.read_counter_A(direction)

    # -----------------------------------------------------------------------------------------------------
    def read_counter_A(self, direction):
        signal_A = self.read_signal_A()
        if signal_A != self.last_signal_A:
            if direction == CLOCKWISE:
                self.counter_A += 1
            else:
                self.counter_A -= 1
        print("Counter A: " + str(self.counter_A))

    # -----------------------------------------------------------------------------------------------------
    def read_signal_A(self):
        return bool(random.random() * 2)

    # -----------------------------------------------------------------------------------------------------
    def check_end(self):
        tmp=random.random() * 1.1
        tmp=bool(tmp//1)
        return tmp
