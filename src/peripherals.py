from xmlrpc.client import Boolean
import RPi.GPIO
import time


def Ultrasonic_Configure(TRIG_PIN:int,ECHO_PIN:int)->Boolean:
    GPIO.setmode(GPIO.BCM) #set pin numbering to broadcom chip standard
    if not isinstance(TRIG_PIN,int) or not isinstance(ECHO_PIN,int):
        print("Pins must be of type int")
        return False
    if TRIG_PIN not in range(1,28) or ECHO_PIN not in range(1,28):
        print("Pins must map to an actual GPIO Pin on Raspberry Pi Zero W")
        return False
    TRIG = TRIG_PIN 
    ECHO = ECHO_PIN

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    #Set output to false to avoid garbage signal at TRIG

    GPIO.output(TRIG,false)
    #allow the HC-SR04 two seconds to configure
    time.sleep(2)
    return True

#Takes x 1us pulses and returns the average measurement
def Ultrasonic_Measurement(TRIG_PIN:int,ECHO_PIN:int)->int:

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    while(GPIO.input(ECHO_PIN==0)):
        start_timer=time.time()

    while(GPIO.input(ECHO_PIN==0)):
        end_timer =time.time()
    
    return 17150(end_timer-start_timer)
        
    






###
# Tried to run requirements.txt to install RPi.GPIO
# Apparently only available on 
# 
# ###
