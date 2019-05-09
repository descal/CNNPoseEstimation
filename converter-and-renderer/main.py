
import converter
import banana
import cv2
import numpy as np
import os, random
from pathlib import Path, PureWindowsPath


i = 0
n = 10 # Number of generated images per object
e = 10 # Extra random images from pool
d = [30,300] # Camera distance from object
p = 0.20 #Scale change percent (distance +- 10%*distance)
RandTexture = True

for root, dirs, files in os.walk("data/models/"):
    for file in files:
        if file.endswith(".obj"):
            renderedWtex = False
            model_file = Path(os.path.join(root, file))
            model_folder = os.path.dirname(os.path.dirname(model_file))
            if RandTexture == True:

                            banana.devour(model_file, n, d[i],p,
                                          True)  # Model path, Number of images, camera distance from object, optional:texture
                            banana.genRandom(model_file, n, e)

                            print("SUCCESS - Rendered with texture")

            else:
                banana.devour(model_file, n, d[i],p)
                banana.genRandom(model_file, n, e)
            i = i + 1


