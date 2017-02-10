from stepper_motor import StepperMotor


# ---------------------------------------------------------------------------------------------------------
def main():
    motor_x = StepperMotor()
    motor_y = StepperMotor()

    motor_x.counter_A=77
    motor_x.reset()

    motor_x.move(10)
    motor_y.reset()


# ---------------------------------------------------------------------------------------------------------
__name__ == '__main__' and main()
