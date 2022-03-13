import picamerax
import picamerax.array
from time import sleep
import numpy as np
import cv2
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import os
from copy import deepcopy
import csv
from numpy import interp

GPIO.setwarnings(False)

led_pin = 13

place_count = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

camera = picamerax.PiCamera()
camera.resolution = (2048, 1520)
camera.framerate = 5
camera.iso = 100
sleep(2)
shutter_speed = 10000 #us
camera.shutter_speed = shutter_speed
camera.exposure_mode = 'off'
camera.awb_mode = 'off'

stream = picamerax.array.PiBayerArray(camera)
camera.capture(stream, "jpeg", bayer=True)

wavelength = input("Wavelength (nm):")
name = input("Name:")
age = input("Age:")
arm_circumference = input("Arm circumference (mm):")
skin_tone = input("Skine tone:")

person_data = {"name": name, "age": age, "arm circumference": arm_circumference, "skin tone": skin_tone}

with open('data/{}.csv'.format(name), 'w') as f:
    for key in person_data.keys():
        f.write("%s,%s\n"%(key, person_data[key]))


def capture_data(lower_bound_sp, upper_bound_sp, count):
    shutter_speeds = np.linspace(lower_bound_sp, upper_bound_sp, count).astype(int)
    images = []

    GPIO.output(led_pin, GPIO.HIGH)
    for sp in shutter_speeds:
        camera.shutter_speed = sp
        sleep(0.1)
        camera.capture(stream, "jpeg", bayer=True)
        sleep(0.01)
        output = np.sum(stream.array, axis=2).astype(np.uint16)
        rgb = cv2.cvtColor(output, cv2.COLOR_BayerRG2RGB)

        image_r = rgb[:,:,0]

        image_r = np.rot90(image_r)

        print(camera.shutter_speed)
        images.append({"shutter_speed": camera.shutter_speed, "iso": camera.iso, "image": deepcopy(image_r)})

        show_r = cv2.resize(image_r, dsize=(int(image_r.shape[1]/5), int(image_r.shape[0]/5)))

        show_r = interp(show_r,[show_r.min(),show_r.max()],[0,255]).astype("uint8")

        cv2.imshow('r', show_r)

        cv2.waitKey(10)
    GPIO.output(led_pin, GPIO.LOW)
    return images


def save_images(images):
    global place_count
    directory = "data/{}nm/{}".format(wavelength, name)
    os.makedirs(directory, exist_ok=True)
    for image in images:
        cv2.imwrite(directory + "/{}_{}_{}_{}.png".format(place_count, image["shutter_speed"], wavelength, name), image["image"])
    place_count += 1


while True:
    state = input("state:")
    print(place_count)
    if state == "q":
        GPIO.output(led_pin, GPIO.LOW)
        break
    elif state == "w":
        wavelength = input("Wavelength (nm):")
        place_count = 1
    elif state == "l":
        capture_data(10000, 200000, 10)
    elif state == "r":
        place_count -= 1
    else:
        images = capture_data(10000, 200000, 10)
        save_images(images)