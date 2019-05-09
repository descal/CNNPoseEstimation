#!/usr/bin/env python3

import os
import numpy as np
from PIL import Image, ImageOps, ImageMath, ImageDraw
from application import Application
from pathlib import Path
import os
def local(*path):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), *path))

class AutonanaApp(Application):
    RESOLUTION = (416,416)
    color       = 1, 1, 1, 1   # model color (overlay)
    position    = 0.0, 0.0, 0.0        # model position
    orientation = 0.0, 00.0, 0.0        # model orientation (degrees)
    light       = 400.0, 400.0, 400.0     # light source position
    fov         = 58.0                 # camera field of view in degrees
    cam         = 0.5, 0.0, 0.0        # camera position
    target      = 0.0 , 0.0, 0.0       # camera target position
    roll        = 0.0                  # camera roll in degrees

    def __init__(self,mod,tex=None):
        super(AutonanaApp, self).__init__()

        self.model = mod
        self.texture = tex

        self._index = 0
        self.load_model(self.model, self.texture)   # load model with texture
        # self.load_model(self.model)               # load model
        # self.set_model_texture(self.texture)      # load, set and enable texture
        # self.disable_texture()                    # disable texture

        self.set_model_color(self.color)       # set and enable color (overlay)
        #self.disable_color()                  # disable color (overlay)

        self.set_light_position(self.light)    # set and enable light
        # self.disable_light()                  # disable light

        self.set_model_from_euler(self.position, self.orientation)    # position object in scene
        self.set_view_from_target(self.cam, self.target, self.roll)   # position camera in scene
        self.set_perspective_projection(self.fov, 0.10, 700.0)          # use perspective projection for rendering (float fieldOfView, float aspectRatio, float nearPlane, float farPlane)

    def update(self, info):
        pass

    def postprocess(self):
        images = self.buffer_to_images()
        self.save_to_file(images)


    def save_to_file(self, images, folder='output'):

        model_name = os.path.basename(Path(self.model))
        model_name = model_name[:len(model_name)-4]
        folder = 'output/'+str(model_name)
        rgb_file       = local('output/temp/rgb_{:04}.png'.format(self._index))
        print(rgb_file)
        yolo_file       = local('output/'+model_name+'_{:04}.txt'.format(self._index))
        self._index += 1

        os.makedirs(local('output/temp'), exist_ok=True)

        images['RGB'].save(rgb_file)

        roi = images['MASK'].getbbox()
        left, upper, right, lower = images['MASK'].getbbox()
        if roi is None: roi = (0,0,0,0)
        annotated = images['RGB'].copy()
        draw = ImageDraw.Draw(annotated)
        draw.rectangle(roi, outline=(255,0,0))
        w = (right-left) #bbox width in pixles
        h = (lower-upper) #bbox height in pixles
        cx = float((left + w/2)/self.RESOLUTION[0]) #bbox center x
        cy = float((upper + h/2)/self.RESOLUTION[1])

        w = float(w/self.RESOLUTION[0]) #Yolo3 standard requires that values are relative to image size
        h = float(h/self.RESOLUTION[1])  #Yolo3 standard requires that values are relative to image size

        yolo3std = model_name+" "+"{:.6f}".format(cx)+" "+"{:.6f}".format(cy)+" "+"{:.6f}".format(w)+" "+"{:.6f}".format(h)

        #Write yolo annotation file
        yolo = open(yolo_file,'w')
        yolo.write(yolo3std)
        #
        # f = open(dataset_file, "a+")
        #
        # f.write("data/obj/"+model_name+'_{:04}.png'.format(self._index-1)+ "\n")
        # f.close()

        print('Saved {} banana(s) of class {}'.format(self._index,model_name))


