from stepper_motor_BIPol import StepperMotor


# ---------------------------------------------------------------------------------------------------------
def main():
    motor_x = StepperMotor([17, 18, 27, 22], 20, 21)
    print("Counter is: "+str(motor_x.counter_A))
    for i in range(0, 300):
        motor_x.step(1)
    print("Counter is: "+str(motor_x.counter_A))
    for i in range(0, 300):
         motor_x.step(0)
    print("Counter is: "+str(motor_x.counter_A))


# ---------------------------------------------------------------------------------------------------------
__name__ == '__main__' and main()
