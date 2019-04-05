#!/usr/bin/env python3

import os
import numpy as np
from PIL import Image, ImageOps, ImageMath, ImageDraw
from application import Application

def local(*path):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), *path))

class BananaApp(Application):
    RESOLUTION = (640,480)

    model           = 'data/Banana.obj'    # relative path to object file
    # model           = 'data/test.obj'    # relative path to object file


    # texture         = 'data/Banana.png'    # relative path to texture file
    texture         = 'data/test5.png'    # relative path to texture file

    color       = 0.2, 0.8, 0.2, 0.3   # model color (overlay)
    # color       = 0.8, 0.8, 0.2, 0.5   # model color (overlay)
    position    = 0.0, 0.0, 0.0        # model position
    orientation = 0.0, 00.0, 0.0        # model orientation (degrees)


    light       = 10.0, 10.0, 10.0     # light source position

    fov         = 58.0                 # camera field of view in degrees
    cam         = 0.5, 0.0, 0.0        # camera position
    target      = 0 , 0.0, 0.0       # camera target position
    roll        = 0.0                  # camera roll in degrees

    def __init__(self):
        super(BananaApp, self).__init__()
        self._index = 0

        self.load_model(self.model, self.texture)   # load model with texture
        # self.load_model(self.model)               # load model
        # self.set_model_texture(self.texture)      # load, set and enable texture
        # self.disable_texture()                    # disable texture

        self.set_model_color(self.color)       # set and enable color (overlay)
        self.disable_color()                  # disable color (overlay)

        self.set_light_position(self.light)    # set and enable light
        self.disable_light()                  # disable light

        self.set_model_from_euler(self.position, self.orientation)    # position object in scene
        self.set_view_from_target(self.cam, self.target, self.roll)   # position camera in scene
        self.set_perspective_projection(self.fov, 0.10, 100.0)          # use perspective projection for rendering (float fieldOfView, float aspectRatio, float nearPlane, float farPlane)

    def update(self, info):
        pass

    def postprocess(self):
        images = self.buffer_to_images()
        self.save_to_file(images)


    def save_to_file(self, images, folder='output'):

        rgb_file       = local(folder, 'rgb_{:04}.png'.format(self._index))
        depth_file     = local(folder, 'depth_{:04}.png'.format(self._index))
        mask_file      = local(folder, 'mask_{:04}.png'.format(self._index))
        annotated_file = local(folder, 'annotated_{:04}.png'.format(self._index))
        roi_file       = local(folder, 'roi_{:04}.txt'.format(self._index))
        cam_pose_file  = local(folder, 'camera_{:04}.txt'.format(self._index))
        obj_pose_file  = local(folder, 'model_{:04}.txt'.format(self._index))
        self._index += 1

        os.makedirs(local(folder), exist_ok=True)

        images['RGB'].save(rgb_file)
        images['DEPTH'].save(depth_file)
        images['MASK'].save(mask_file)

        roi = images['MASK'].getbbox()
        if roi is None: roi = (0,0,0,0)
        annotated = images['RGB'].copy()
        draw = ImageDraw.Draw(annotated)
        draw.rectangle(roi, outline=(255,0,0))
        annotated.save(annotated_file)

        with open(roi_file,'wb') as f:
            np.savetxt(f, [roi], fmt='%d', delimiter=' ')

        cam = self.get_camera_pose()
        with open(cam_pose_file,'wb') as f:
            np.savetxt(f, [cam], fmt='%.5f', delimiter=' ')

        obj = self.get_model_pose()
        with open(obj_pose_file,'wb') as f:
            np.savetxt(f, [obj], fmt='%.5f', delimiter=' ')

        print('Saved {} banana'.format(self._index))


