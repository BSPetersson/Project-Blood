import RPi.GPIO as GPIO
import time

ledPin = 2

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output

GPIO.output(ledPin, GPIO.HIGH)
time.sleep(10)
GPIO.output(ledPin, GPIO.LOW)
