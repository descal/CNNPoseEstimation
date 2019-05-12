
import converter
import banana
import cv2
import numpy as np
import os, random
from pathlib import Path, PureWindowsPath

i = 0 # Distance index
n = 2000 # Number of generated images per object
e = 2000 # Extra random images from pool
d = [250,300,270] # Camera distance from object (( NEEDS TO HAVE 1 PER CLASS - Chronologically ))
p = 0.20 #Scale change percent (distance +- 20%*distance)
RandTexture = False # Enables random textures
noise = None # Noise type ("gauss","s&p","poisson","speckle",None)


for root, dirs, files in os.walk("data/models/"):
    for file in files:
        if file.endswith(".obj"):
            model_file = Path(os.path.join(root, file))
            model_folder = os.path.dirname(os.path.dirname(model_file))
            if RandTexture == True:
                banana.devour(model_file, n, d[i],p,noise,True)  # Model path, Number of images, camera distance from object, optional:texture
                # banana.genRandom(model_file, n, e,noise)
                print("Rendered with texture")
            else:
                banana.devour(model_file, n, d[i],p,noise)
                # banana.genRandom(model_file, n, e,noise)
                print("Rendered with color")
            i = i + 1

os.rmdir("output/temp")

print("DONE !! Whoop Whoop")
