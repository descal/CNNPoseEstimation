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

    # model           = 'data/Banana.obj'    # relative path to object file
    model           = 'data/model.obj'    # relative path to object file
    texture         = 'data/Banana.png'    # relative path to texture file
    # texture         = 'data/texture0.jpg'    # relative path to texture file

    color       = 0.2, 0.8, 0.2, 0.3   # model color (overlay)
    color       = 1, 1, 1, 1   # model color (overlay)

    # color       = 0.8, 0.8, 0.2, 0.5   # model color (overlay)
    position    = 0.0, 0.0, 0.0        # model position
    orientation = 0.0, 00.0, 0.0        # model orientation (degrees)


    light       = 100.0, 100.0, 100.0     # light source position


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
        self.disable_color()                  # disable color (overlay)

        self.set_light_position(self.light)    # set and enable light
        # self.disable_light()                  # disable light

        self.set_model_from_euler(self.position, self.orientation)    # position object in scene
        self.set_view_from_target(self.cam, self.target, self.roll)   # position camera in scene
        self.set_perspective_projection(self.fov, 0.10, 300.0)          # use perspective projection for rendering (float fieldOfView, float aspectRatio, float nearPlane, float farPlane)

    def update(self, info):
        pass

    def postprocess(self):
        images = self.buffer_to_images()
        self.save_to_file(images)


    def save_to_file(self, images, folder='output'):
        # # path = Path(self.model)
        # print(Path(self.model).filename)
        model_name = os.path.basename(Path(self.model))
        model_name = model_name[:len(model_name)-4]
        folder = 'output/'+str(model_name)
        rgb_file       = local(folder, 'rgb_{:04}.png'.format(self._index))
        depth_file     = local(folder, 'depth_{:04}.png'.format(self._index))
        mask_file      = local(folder, 'mask_{:04}.png'.format(self._index))
        annotated_file = local(folder, 'annotated_{:04}.png'.format(self._index))
        roi_file       = local(folder, 'roi_{:04}.txt'.format(self._index))
        yolo_file       = local(folder, model_name+'_{:04}.txt'.format(self._index))
        dataset_file = local(folder,'model.txt')

        cam_pose_file  = local(folder, 'camera_{:04}.txt'.format(self._index))
        obj_pose_file  = local(folder, 'pose_{:04}.txt'.format(self._index))
        self._index += 1

        os.makedirs(local(folder), exist_ok=True)

        images['RGB'].save(rgb_file)
        images['DEPTH'].save(depth_file)
        images['MASK'].save(mask_file)

        roi = images['MASK'].getbbox()
        left, upper, right, lower = images['MASK'].getbbox()
        if roi is None: roi = (0,0,0,0)
        annotated = images['RGB'].copy()
        draw = ImageDraw.Draw(annotated)
        draw.rectangle(roi, outline=(255,0,0))
        annotated.save(annotated_file)
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

        print(dataset_file)
        f = open(dataset_file, "a+")

        f.write("data/obj/"+model_name+'_{:04}.png'.format(self._index)+ "\n")
        f.close()


        with open(roi_file,'wb') as f:
            np.savetxt(f, [roi], fmt='%d', delimiter=' ')

        cam = self.get_camera_pose()
        with open(cam_pose_file,'wb') as f:
            np.savetxt(f, [cam], fmt='%.5f', delimiter=' ')

        obj = self.get_model_pose()
        with open(obj_pose_file,'wb') as f:
            np.savetxt(f, [obj], fmt='%.5f', delimiter=' ')

        print('Saved {} banana'.format(self._index))


