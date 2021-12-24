import io
import time
import threading
import picamera
from PIL import Image
import cv2
import numpy as np

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []

frame = None



class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.start()

    def run(self):
        # This method runs in a separate thread
        global done
        global frame
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                    
                    # Read the image and do some processing on it
                    image = Image.open(self.stream).convert('RGB')
                    image = np.array(image)

                    red = image[:,:,0]

                    #img = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)

                    img = cv2.adaptiveThreshold(img.astype("uint8"), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 89, 3)

                    img = cv2.bitwise_not(img)

                    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel_open)
                    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel_close)
                    
                    cv2.imshow("segmentation", img)
                    cv2.waitKey(1)
                    #rawCapture.truncate(0)
                    
                    #...
                    #...
                    # Set done to True if you want the script to terminate
                    # at some point
                    #done=True
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the pool
                    with lock:
                        pool.append(self)

def streams():
    while not done:
        with lock:
            if pool:
                processor = pool.pop()
            else:
                processor = None
        if processor:
            yield processor.stream
            processor.event.set()
        else:
            # When the pool is starved, wait a while for it to refill
            time.sleep(0.1)
            
        #if frame is not None:
            #red = frame[:,:,0]
            #green = frame[:,:,1]
            #blue = frame[:,:,2]
            
            #cv2.imshow("red", red)
            #cv2.imshow("green", green)
            #cv2.imshow("blue", blue)
            
            #cv2.imwrite("images/image_{}.png".format(int(time.time())), red)
            
            #cv2.imshow("frame", frame)
            #cv2.waitKey(1)
            #rawCapture.truncate(0)
            #print("a")

with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range(4)]
    camera.resolution = (2028, 1470)
    camera.framerate = 5
    
    camera.iso = 200
    
    #camera.start_preview()
    time.sleep(2)
    
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    #camera.awb_gains = (2.6914, 2.1016)
    camera.awb_gains = (1.0, 0.1)
    
    # 2.6914
    # 2.1016
    
    print(camera.shutter_speed)
    print(g)
    
    camera.capture_sequence(streams(), use_video_port=True)

# Shut down the processors in an orderly fashion
while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()