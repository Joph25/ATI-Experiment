from stepper_motor import StepperMotor

# Define GPIO output signals to use for motor x
# Physical pins 29,31,33,35 = GPIO5,GPIO6,GPIO13,GPIO19
STEP_PINS_MOTORX = [5, 6, 13, 19]
# Define GPIO input signal to use for end positions motor x
ENDPIN_MOTORX = 26

# Define GPIO output signals to use for motor y
# Physical pins 12,16,18,22 = GPIO18,GPIO23,GPIO24,GPIO25
STEP_PINS_MOTORY = [18, 23, 24, 25]
# Define GPIO input signal to use for endpositions motor y
ENDPIN_MOTORY = 12


# ---------------------------------------------------------------------------------------------------------
def experiment():
    motor_x = StepperMotor(STEP_PINS_MOTORX, ENDPIN_MOTORX)
    motor_y = StepperMotor(STEP_PINS_MOTORY, ENDPIN_MOTORY)

    motor_x.move(10)
    motor_y.move(5)


# ---------------------------------------------------------------------------------------------------------
__name__ == '__main__' and experiment()
