import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from os import listdir
import matplotlib.patches as patches
from PIL import Image
from skimage.draw import line_aa
from mpl_toolkits.axes_grid1 import ImageGrid
from numpy import diff
from scipy import ndimage
from scipy.optimize import curve_fit
from numpy import inf
from numpy import interp

def split(path):
    s = path.replace('.', '_')
    s = s.split('_')
    return s

def transform_for_show(image):
    image = interp(image, [image.min(),image.max()],[0,255]).astype("uint8")
    return image

def get_images(path, shutter_speed):
    image_names = listdir(path)
    image_names = list(filter(lambda k: shutter_speed in k, image_names))
    images = []
    for image_name in image_names:
        full_path = path + image_name
        images.append(cv2.imread(full_path, cv2.IMREAD_UNCHANGED))
    images = np.array(images).astype("uint16")
    images = images[:,200:,400:2800]
    return images, image_names

def show_grid_of(images, size):
    fig = plt.figure(figsize=(20, 20*size[0]/2))
    grid = ImageGrid(fig, 111, nrows_ncols=size, axes_pad=0.2)

    for ax, im in zip(grid, images):
        im = transform_for_show(im)
        ax.imshow(im, cmap='gray')

    plt.show()

def log_transform(images):
    log_images = []
    for image in images:
        c = 4095 / np.log(1 + np.max(image))
        log_image = c * (np.log(image + 1))
        log_image = np.array(log_image, dtype = np.uint16)
        log_images.append(log_image)
    return log_images

def local_log_transform(images):
    log_images = []
    for image in images:
        c = 4095 / np.log(1 + np.max(image))
        log_image = c * (np.log(image + 1))
        log_image = np.array(log_image, dtype = np.uint16)
        log_images.append(log_image)
    return log_images

def get_median_image(images):
    return np.median(images, axis=0).astype('uint16')

def get_mean_image(images):
    return np.mean(images, axis=0).astype('uint16')

def median_subtraction(images, median):
    subs = []
    median = median.astype("int32")
    for image in images:
        image = image.astype("int32")
        sub = (image-median)
        subs.append(sub)
    return subs

def plot_hist(image):
    fig = plt.figure(figsize=(20, 10))
    x = image.flatten()
    plt.hist(x, bins=int((x.max()-x.min()-2)/10), range=(x.min()+1, x.max()-1))
    plt.show()

def map_percentile_bounds(images, bounds=(5, 95)):
    mapped = []
    for image in images:
        lower, upper = np.percentile(image.flatten(), bounds)
        image = interp(image, [lower,upper],[0,4095]).astype("uint16")
        mapped.append(image)
    return mapped

def gamma_mapping(images, gamma=1.0):
    gamma_images = []
    for image in images:
        gamma_image = (np.power((image/4095), gamma)*4095).astype("uint16")
        gamma_images.append(gamma_image)
    return gamma_images

def mean_filter_subtraction(images, size=(200,200)):
    background_subtracted = []
    for image in images:
        image = image.astype("int16")
        background = cv2.blur(image, size).astype("int32")
        image = image.astype("int32")
        subtracted = (image-background)
        background_subtracted.append(subtracted)
    return background_subtracted

def raise_from_negative(images):
    raised = []
    for image in images:
        image = image-image.min()
        raised.append(image)
    return(raised)