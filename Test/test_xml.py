import xmltodict
from stepper_motor_BIPol import StepperMotor


# ---------------------------------------------------------------------------------------------------------
def main():
    #read config parameters from config.xml
    with open('config.xml') as fd:
        conf = xmltodict.parse(fd.read())
    #print(conf)
    port_A = int(conf['config_stepper_motor']['motor1']['port_A'])
    port_B = int(conf['config_stepper_motor']['motor1']['port_B'])
    port_C = int(conf['config_stepper_motor']['motor1']['port_C'])
    port_D = int(conf['config_stepper_motor']['motor1']['port_D'])
    port_end = int(conf['config_stepper_motor']['motor1']['port_end'])
    port_counter = int(conf['config_stepper_motor']['motor1']['port_counter'])
    motor_x = StepperMotor([port_A,port_B,port_C,port_D], port_end, port_counter)
    #motor_x = StepperMotor(conf['config_stepper_motor']['motor1'])
    print("Counter is: "+str(motor_x.counter_A))
    for i in range(0, 300):
        motor_x.step(1)
    print("Counter is: "+str(motor_x.counter_A))
    for i in range(0, 300):
         motor_x.step(0)
    print("Counter is: "+str(motor_x.counter_A))


# ---------------------------------------------------------------------------------------------------------
__name__ == '__main__' and main()
