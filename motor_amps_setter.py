import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

stepPin_1 = 24
dirPin_1 = 26
stepPin_2 = 18
dirPin_2 = 22

delta = 0.00005
steps = 80000

GPIO.setup(stepPin_1, GPIO.OUT)
GPIO.setup(dirPin_1, GPIO.OUT)
GPIO.setup(stepPin_2, GPIO.OUT)
GPIO.setup(dirPin_2, GPIO.OUT)
 
while True:
    print("GO!")
    GPIO.output(dirPin_1, GPIO.HIGH)
    GPIO.output(dirPin_2, GPIO.HIGH)
    for i in range(steps):
        GPIO.output(stepPin_1, GPIO.HIGH)
        GPIO.output(stepPin_2, GPIO.HIGH)
        sleep(delta)
        GPIO.output(stepPin_1, GPIO.LOW)
        GPIO.output(stepPin_2, GPIO.LOW)
        sleep(delta)
    sleep(3)
    
    GPIO.output(dirPin_1, GPIO.LOW)
    GPIO.output(dirPin_2, GPIO.HIGH)
    for i in range(steps):
        GPIO.output(stepPin_1, GPIO.HIGH)
        GPIO.output(stepPin_2, GPIO.HIGH)
        sleep(delta)
        GPIO.output(stepPin_1, GPIO.LOW)
        GPIO.output(stepPin_2, GPIO.LOW)
        sleep(delta)
    sleep(3)