import logging
from stepper_motor import StepperMotor

# Define GPIO output signals to use for motor x
# Physical pins 29,31,33,35 = GPIO5,GPIO6,GPIO13,GPIO19
STEP_PINS_MOTORX = [5, 6, 13, 19]
# Define GPIO input signal to use for end positions of motor x (physical pin 37)
ENDPIN_MOTORX = 26
# Define GPIO input signal to use for counter A of motor x (physical pin 3)
APIN_MOTORX = 17

# Define GPIO output signals to use for motor y
# Physical pins 12,16,18,22 = GPIO18,GPIO23,GPIO24,GPIO25
STEP_PINS_MOTORY = [18, 23, 24, 25]
# Define GPIO input signal to use for endpositions motor y (physical pin 32)
ENDPIN_MOTORY = 12
# Define GPIO input signal to use for counter A of motor y (physical pin 13)
APIN_MOTORY = 27


# ---------------------------------------------------------------------------------------------------------
def experiment():
    logging.basicConfig(level=logging.INFO)
    motor_x = StepperMotor(STEP_PINS_MOTORX, ENDPIN_MOTORX, APIN_MOTORX)
    motor_y = StepperMotor(STEP_PINS_MOTORY, ENDPIN_MOTORY, APIN_MOTORY)

    motor_x.move(10)
    motor_y.move(5)


# ---------------------------------------------------------------------------------------------------------
__name__ == '__main__' and experiment()
