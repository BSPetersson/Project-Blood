import RPi.GPIO as GPIO
from time import sleep
import time
import sys
from hx711 import HX711

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(-438.4)

hx.reset()

hx.tare()

delta = 0.000001

stepPin_1 = 8
dirPin_1 = 7
stepPin_2 = 24
dirPin_2 = 25
motor_stop_pin = 20
led_pin = 26
limit_switch_o_pin_1 = 14
limit_switch_c_pin_1 = 15
limit_switch_o_pin_2 = 18
limit_switch_c_pin_2 = 23

#GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(stepPin_1, GPIO.OUT)
GPIO.setup(dirPin_1, GPIO.OUT)
GPIO.setup(stepPin_2, GPIO.OUT)
GPIO.setup(dirPin_2, GPIO.OUT)
GPIO.setup(motor_stop_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(limit_switch_o_pin_1, GPIO.IN)
GPIO.setup(limit_switch_c_pin_1, GPIO.IN)
GPIO.setup(limit_switch_o_pin_2, GPIO.IN)
GPIO.setup(limit_switch_c_pin_2, GPIO.IN)


weight = hx.get_weight(3)
hx.power_down()
hx.power_up()

pt = 0

while True:
    limit_switch_1 = GPIO.input(limit_switch_o_pin_1)
    limit_switch_2 = GPIO.input(limit_switch_o_pin_2)
    
    t = int(time.time())
    if t != pt:
        pt = t
        weight = hx.get_weight(3)
        hx.power_down()
        hx.power_up()
        print(limit_switch_1)
        print(limit_switch_2)
        print(weight)
        print("\n")
    
    if limit_switch_1:
        GPIO.output(dirPin_1, GPIO.HIGH)
        GPIO.output(dirPin_2, GPIO.HIGH)
    else:
        GPIO.output(dirPin_1, GPIO.LOW)
        GPIO.output(dirPin_2, GPIO.LOW)
    
    if not limit_switch_2:
        GPIO.output(led_pin, GPIO.HIGH)
        GPIO.output(motor_stop_pin, GPIO.LOW)
        GPIO.output(stepPin_1, GPIO.HIGH)
        GPIO.output(stepPin_2, GPIO.HIGH)
        sleep(abs(delta/(weight/5000)))
        GPIO.output(stepPin_1, GPIO.LOW)
        GPIO.output(stepPin_2, GPIO.LOW)
        sleep(abs(delta/(weight/5000)))
    else:
        GPIO.output(motor_stop_pin, GPIO.HIGH)
        GPIO.output(led_pin, GPIO.LOW)
        
        
        
        
        
        
        