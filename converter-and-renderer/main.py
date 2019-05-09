
import converter
import banana
import cv2
import numpy as np
import os, random
from pathlib import Path, PureWindowsPath


i = 0
n = 10 # Number of generated images per object
e = 10 # Extra random images from pool
d = [120,300] # Camera distance from object
p = 0.20 #Scale change percent (distance +- 10%*distance)
RandTexture = False

for root, dirs, files in os.walk("data/models/"):
    for file in files:
        if file.endswith(".obj"):
            renderedWtex = False
            model_file = Path(os.path.join(root, file))
            model_folder = os.path.dirname(os.path.dirname(model_file))
            if RandTexture == True:
                for root_t, dirs_t, files_t in os.walk("data/textures/"):
                    for file_t in files_t:
                        print("RANDOM",random.choice(files))
                        if file_t.endswith(".png") : #and file.startswith("texture")
                            print("Here",file)
                            texture_file = Path(os.path.join(root_t, file_t))
                            print("Found model with texture")
                            print("Texture:",texture_file)
                            print("Model:",model_file)
                            try:
                                banana.devour(model_file, n, d[i],p,
                                              texture_file)  # Model path, Number of images, camera distance from object, optional:texture
                                banana.genRandom(model_file, n, e)

                                print("SUCCESS - Rendered with texture")
                                renderedWtex = True
                            except:
                                print("Unable to render with texture")

                            if renderedWtex == False:
                                print("Rendering without texture")
                                banana.devour(model_file, n,d[i],p)
                                banana.genRandom(model_file, n, e)
            else:
                banana.devour(model_file, n, d[i],p)
                banana.genRandom(model_file, n, e)
            i = i + 1


