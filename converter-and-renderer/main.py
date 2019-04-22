
import converter
import banana
import cv2
import numpy as np

import os

from pathlib import Path, PureWindowsPath

BatchRun = False

if BatchRun == True:
    for root, dirs, files in os.walk("ShapeNetCore.v2/"):
        for file in files:
            if file.endswith("model_normalized.obj"):
                model_file = Path(os.path.join(root, file))
                model_folder = os.path.dirname(os.path.dirname(model_file))
                for root, dirs, files in os.walk(model_folder):
                    for file in files:
                        if file.endswith(".png") and file.startswith("texture"):
                            texture_file = Path(os.path.join(root, file))
                            print("Found model with texture")
                            print("Texture:",texture_file)
                            print("Model:",model_file)
                            try:
                                banana.devour(model_file,5,10,texture_file
                                              )
                                print("SUCCESS - Rendered with texture")
                            except:
                                try:
                                    banana.devour(model_file, 5, 10)
                                    print("SUCCESS - Rendered without texture")
                                except:
                                    print("Failed to render")

                            print("-----------")



model = 'data\Banana.obj'
# texture = 'data\Banana.png'
#
model = 'data/0.obj' # relative path to object file
# texture = 'data/13476.jpg' # relative path to texture file
texture=None
background_file_in = 'data/palm2.jpg'
banana.devour(model,background_file_in,40,170.5,texture) #Model path, Number of images, camera distance from object, optional:texture

# banana.look() # Visualize model



