from picamera import PiCamera
from time import sleep
import numpy as np
import cv2
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import os
from copy import deepcopy
import csv

GPIO.setwarnings(False)


led_pin = 13

rg = 2.0
bg = 2.0

place_count = 1
output = np.empty((1520, 2048, 3), dtype=np.uint8)


GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

camera = PiCamera()
camera.resolution = (2048, 1520)
camera.framerate = 5
camera.iso = 100
sleep(2)
shutter_speed = 10000 #us
camera.shutter_speed = shutter_speed
camera.exposure_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = (rg, bg)


wavelength = input("Wavelength (nm):")
name = input("Name:")
age = input("Age:")
weight = input("Weight (kg):")
arm_circumference = input("Arm circumference (mm):")
skin_tone = input("Skine tone:")

person_data = {"name": name, "age": age, "weight": weight, "arm circumference": arm_circumference, "skin tone": skin_tone}

with open('../data/{}.csv'.format(name), 'w') as f:
    for key in person_data.keys():
        f.write("%s,%s\n"%(key, person_data[key]))


def capture_data(lower_bound_sp, upper_bound_sp, count):
    shutter_speeds = np.linspace(lower_bound_sp, upper_bound_sp, count).astype(int)
    images = []

    GPIO.output(led_pin, GPIO.HIGH)
    for sp in shutter_speeds:
        camera.shutter_speed = sp
        sleep(0.1)
        camera.capture(output, 'rgb')
        image = output[:,:,0]
        image = np.rot90(image)
        images.append({"shutter_speed": camera.shutter_speed, "iso": camera.iso, "image": deepcopy(image)})
        cv2.imshow('image90', image)
        cv2.waitKey(160)
    GPIO.output(led_pin, GPIO.LOW)
    return images


def save_images(images):
    global place_count
    directory = "../data/{}nm/{}".format(wavelength, name)
    os.makedirs(directory, exist_ok=True)
    for image in images:
        cv2.imwrite(directory + "/{}_{}.png".format(place_count, image["shutter_speed"]), image["image"])
    place_count += 1


while True:
    state = input("state:")
    if state == "q":
        GPIO.output(led_pin, GPIO.LOW)
        break
    elif state == "w":
        wavelength = input("Wavelength (nm):")
    elif state == "l":
        capture_data(10000, 150000, 5)
    else:
        images = capture_data(10000, 150000, 20)
        save_images(images)