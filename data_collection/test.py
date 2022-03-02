from picamera import PiCamera
from time import sleep
import numpy as np
import cv2
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import os
from copy import deepcopy

GPIO.setwarnings(False)


output = np.empty((1520, 2048, 3), dtype=np.uint8)
led_pin = 13

rg = 2.0
bg = 2.0

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)


camera = PiCamera()
camera.resolution = (2048, 1520)
camera.framerate = 5
camera.iso = 100
sleep(2)
shutter_speed = 150000 #us
camera.shutter_speed = shutter_speed
camera.exposure_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = (rg, bg)


GPIO.output(led_pin, GPIO.HIGH)
for i in range(100):
    sleep(0.1)
    camera.capture(output, 'rgb')
    image_r = output[:,:,0]
    image = np.rot90(image_r)
    #image_g = output[:,:,1]
    #image_b = output[:,:,2]
    #image = np.rot90(image)
    cv2.imshow('red', image)
    #cv2.imshow('blue', image_b)
    cv2.waitKey(500)

GPIO.output(led_pin, GPIO.LOW)

