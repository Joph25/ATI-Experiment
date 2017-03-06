import xmltodict
from stepper_motor_BIPol import StepperMotor


# ---------------------------------------------------------------------------------------------------------
def main():
    #read config parameters from config.xml
    with open('config.xml') as fd:
        conf = xmltodict.parse(fd.read())
    print(conf)
    port_A = conf['config_stepper_motor']['motor1']['port_A']
    print(port_A)
    #motor_x = StepperMotor([17, 18, 27, 22], 20, 21)
    #print("Counter is: "+str(motor_x.counter_A))
    #for i in range(0, 300):
    #    motor_x.step(1)
    #print("Counter is: "+str(motor_x.counter_A))
    #for i in range(0, 300):
    #     motor_x.step(0)
    #print("Counter is: "+str(motor_x.counter_A))


# ---------------------------------------------------------------------------------------------------------
__name__ == '__main__' and main()
