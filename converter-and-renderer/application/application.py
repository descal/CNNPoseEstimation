
import os

import moderngl
import numpy as np
from .ext.obj import Obj
from PIL import Image, ImageOps, ImageMath, ImageDraw
from pyrr import Quaternion, Matrix33, Matrix44, matrix44

from PyQt5 import QtWidgets

from .window import Window


def local(*path):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), *path))


class Application(object):
    RESOLUTION = (1280, 720)
    standalone = True

    vertex_shader   = 'shader.vert'        # relative path to vertex shader
    fragment_shader = 'shader.frag'        # relative path to fragment shader

    def __init__(self, ):
        self._viewport = (0, 0) + self.RESOLUTION
        self._model_mat = Matrix44.identity()
        self._view_mat = Matrix44.identity()
        self._projection_mat = Matrix44.identity()

        if self.standalone:                                         # standalone mode
            self._ctx = moderngl.create_standalone_context()
        else:
            self._ctx = moderngl.create_context()                   # window mode

        self._fbo = self._ctx.framebuffer(                          # create framebuffer for rendering to file
            self._ctx.renderbuffer(self.RESOLUTION),
            self._ctx.depth_renderbuffer(self.RESOLUTION),
        )

        self.load_program(self.vertex_shader, self.fragment_shader) # load the shader program to GPU


    def load_program(self, vertex_shader_file, fragment_shader_file):
        vertex_shader = open(local(vertex_shader_file)).read()
        fragment_shader = open(local(fragment_shader_file)).read()

        self.prog = self._ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        self._M = self.prog['M']
        self._V = self.prog['V']
        self._P = self.prog['P']
        self._light = self.prog['Light']
        self._color = self.prog['Color']
        self._use_texture = self.prog['UseTexture']
        self._use_light = self.prog['UseLight']
        self._use_color = self.prog['UseColor']


    def load_model(self, obj_file, tex_file = None):
        vertex_data = Obj.open(local('..', obj_file))
        vbo = self._ctx.buffer(vertex_data.pack('vx vy vz nx ny nz tx ty tz'))
        vao = self._ctx.simple_vertex_array(self.prog, vbo, 'in_vert', 'in_norm', 'in_text')
        self._model = vao

        if tex_file is not None:
            self.set_model_texture(tex_file)
            self.disable_color()
        else:
            self.disable_texture()


    def set_model_texture(self, tex_file):
        texture = Image.open(local('..', tex_file)).transpose(Image.FLIP_TOP_BOTTOM).convert('RGB')
        print(texture.size)

        self.texture = self._ctx.texture(texture.size, 3, texture.tobytes())
        self.texture.build_mipmaps()
        self.texture.use()
        self._use_texture.value = True

    def enable_texture(self):
        self._use_texture.value = False

    def disable_texture(self):
        self._use_texture.value = False

    def toggle_texture(self):
        self._use_texture.value = not self._use_texture.value

    def set_model_color(self, color):
        self._color.value = color

    def disable_color(self):
        self._use_color.value = False

    def enable_color(self):
        self._use_color.value = True

    def toggle_color(self):
        self._use_color.value = not self._use_color.value


    def set_light_position(self, pos):
        self._light.value = pos
        self._use_light.value = True

    def disable_light(self):
        self._use_light.value = False

    def enable_light(self):
        self._use_light.value = True

    def toggle_light(self):
        self._use_light.value = not self._use_light.value


    def set_perspective_projection(self, fov, near=0.01, far=1.0):
        width, height = self.RESOLUTION
        self._projection_mat = Matrix44.perspective_projection(fov, width/height, near, far)

    def set_orthogonal_projection(self, near=0.01, far=1.0):
        width, height = self.RESOLUTION
        self._projection_mat = Matrix44.orthogonal_projection(-width/2, width/2, -height/2, height/2, near, far) #(left, right, bottom, top, near, far, dtype=None)


    def set_view_from_euler(self, pos, euler):
        T = Matrix44.from_translation(pos, dtype='f4')
        R = Matrix44.from_eulers(np.deg2rad(euler[::-1]), dtype='f4')
        self._view_mat = T * R

    def set_view_from_quaternion(self, pos, q):
        T = Matrix44.from_translation(pos, dtype='f4')
        R = Matrix44.from_quaternion(q, dtype='f4')
        self._view_mat = T * R

    def set_view_from_target(self, pos, target, roll=0):
        up = np.array([0.0, 1.0, 0.0])
        R = Matrix44.from_z_rotation(np.deg2rad(roll), dtype='f4')
        self._view_mat = R * Matrix44.look_at(pos, target, up)


    def set_model_from_euler(self, pos, euler):
        T = Matrix44.from_translation(pos, dtype='f4')
        R = Matrix44.from_eulers(np.deg2rad(euler), dtype='f4')
        self._model_mat = T * R

    def set_model_from_quaternion(self, pos, q):
        T = Matrix44.from_translation(pos, dtype='f4')
        R = Matrix44.from_quaternion(q, dtype='f4')
        self._model_mat = T * R


    def set_viewport_size(self, size):
        self._viewport = (0, 0) + size


    def camera_zoom(self, factor):
        T = Matrix44.from_translation([0,0,1*factor], dtype='f4')
        self._view_mat = T * self._view_mat

    def camera_roll(self, angle):
        R = Matrix44.from_z_rotation(np.deg2rad(angle), dtype='f4')
        self._view_mat = R * self._view_mat

    def camera_pitch(self, angle):
        R = Matrix44.from_y_rotation(np.deg2rad(angle), dtype='f4')
        self._view_mat = R * self._view_mat

    def camera_yaw(self, angle):
        R = Matrix44.from_x_rotation(np.deg2rad(angle), dtype='f4')
        self._view_mat = R * self._view_mat

    def camera_orbitH(self, angle):
        vec = self._view_mat[:3,1]
        R = matrix44.create_from_axis_rotation(vec, np.deg2rad(angle), dtype='f4')
        self._view_mat = self._view_mat * R

    def camera_orbitV(self, angle):
        vec = self._view_mat[:3,0]
        R = matrix44.create_from_axis_rotation(vec, np.deg2rad(angle), dtype='f4')
        self._view_mat = self._view_mat * R

    def camera_move(self, x, y):
        T = Matrix44.from_translation([x,-y,0], dtype='f4')
        self._view_mat = T * self._view_mat



    def object_zoom(self, factor):
        T = Matrix44.from_translation([0,0,-1*factor], dtype='f4')
        self._model_mat = self._model_mat * T

    def object_roll(self, angle):
        R = Matrix44.from_z_rotation(np.deg2rad(-angle), dtype='f4')
        self._model_mat = self._model_mat * R

    def object_pitch(self, angle):
        R = Matrix44.from_y_rotation(np.deg2rad(-angle), dtype='f4')
        self._model_mat = self._model_mat * R

    def object_yaw(self, angle):
        R = Matrix44.from_x_rotation(np.deg2rad(angle), dtype='f4')
        self._model_mat = self._model_mat * R

    def object_orbitH(self, angle):
        vec = self._model_mat[:3,1]
        R = matrix44.create_from_axis_rotation(vec, np.deg2rad(angle), dtype='f4')
        self._model_mat = self._model_mat * R

    def object_orbitV(self, angle):
        vec = self._model_mat[:3,0]
        R = matrix44.create_from_axis_rotation(vec, np.deg2rad(-angle), dtype='f4')
        self._model_mat = self._model_mat * R

    def object_move(self, x, y):
        vec = self._view_mat.dot(np.array([x,-y,0,1]))
        T = Matrix44.from_translation(vec, dtype='f4')
        self._model_mat = T * self._model_mat
        # T = Matrix44.from_translation([-x,-y,0], dtype='f4')
        # self._model_mat = T * self._model_mat



    def reset(self):
        self.reset_model()
        self.reset_view()

    def reset_model(self):
        self._model_mat = Matrix44.identity()

    def reset_view(self):
        self.set_view_from_target((0.5,0,0), (0,0,0), 0)


    def get_camera_pose(self):
        q = np.array(Quaternion.from_matrix(self._view_mat))
        t = np.array(self._view_mat[3,:3])
        return np.hstack((t,q))

    def get_model_pose(self):
        q = np.array(Quaternion.from_matrix(self._model_mat))
        t = np.array(self._model_mat[3,:3])
        return np.hstack((t,q))

    def get_pose(self):
        T = self._view_mat * self._model_mat
        q = np.array(Quaternion.from_matrix(T))
        t = np.array(T[3,:3])
        return np.hstack((t,q))


    def render(self):
        if self._ctx.screen is not None:
            self._ctx.screen.use()
            self._ctx.viewport = self._viewport
            self._render()

        self._fbo.use()
        self._ctx.viewport = (0,0) + self.RESOLUTION
        self._render()

    def _render(self):
        self._ctx.clear()
        self._ctx.enable(moderngl.DEPTH_TEST)
        self._ctx.enable(moderngl.CULL_FACE)
        # self._ctx.enable(moderngl.BLEND)

        self._M.write(self._model_mat.astype('f4').tobytes())
        self._V.write(self._view_mat.astype('f4').tobytes())
        self._P.write(self._projection_mat.astype('f4').tobytes())
        self._model.render()


    def buffer_to_images(self):
        rgb_data = self._fbo.read(components=3, attachment=0, alignment=1)
        depth_data = self._fbo.read(components=1, attachment=-1, alignment=4, dtype='f4')

        depth_raw = Image.frombytes('F', self._fbo.size, depth_data, 'raw', 'F', 0, -1)
        depth = 1.0 - np.array(depth_raw)
        mask = depth > 0.0
        if np.sum(mask) > 0:
            dmin, dmax = np.min(depth[mask]), np.max(depth[mask])
            depth[mask] = (depth[mask] - dmin) / (dmax-dmin)

        rgb_img = Image.frombytes('RGB', self._fbo.size, rgb_data, 'raw', 'RGB', 0, -1)
        depth_img = Image.fromarray((depth * 255).astype('uint8'),'P')
        mask_img = Image.fromarray((mask * 255).astype('uint8'),'P')

        return {'RGB': rgb_img, 'DEPTH': depth_img, 'MASK': mask_img}


    def update(self, info):
        pass

    def postprocess(self):
        pass

    def run_instance(self):
        self.update(None)
        self.render()
        self.postprocess()

    @classmethod
    def run(application):
        application.standalone = True
        app = application()
        app.update(None)
        app.render()
        app.postprocess()


    @classmethod
    def run_in_window(application):
        application.standalone = False
        app = QtWidgets.QApplication([])
        widget = Window(application.RESOLUTION, getattr(application, 'WINDOW_TITLE', application.__name__))
        widget.application = application
        widget.show()
        app.exec_()



