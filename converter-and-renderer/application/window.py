import time
import numpy as np

from PyQt5 import QtOpenGL, QtWidgets, QtCore


class WindowInfo:
    def __init__(self):
        self.size = (0, 0)
        self.mouse = (0, 0)
        self.old_mouse = (0, 0)
        self.wheel = 0
        self.time = 0
        self.dt = 0
        self.viewport = (0, 0, 0, 0)
        self.keys = np.full(256, False)
        self.old_keys = np.copy(self.keys)
        self.buttons = np.full(3, False)
        self.old_buttons = np.copy(self.buttons)

    def key_down(self, key):
        return self.keys[key]

    def key_pressed(self, key):
        return self.keys[key] and not self.old_keys[key]

    def key_released(self, key):
        return not self.keys[key] and self.old_keys[key]

    def mouse_down(self, key):
        return self.buttons[key]

    def mouse_pressed(self, key):
        return self.buttons[key] and not self.old_buttons[key]

    def mouse_released(self, key):
        return not self.buttons[key] and self.old_buttons[key]



class Window(QtOpenGL.QGLWidget):
    def __init__(self, size, title):
        fmt = QtOpenGL.QGLFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        fmt.setSwapInterval(1)
        fmt.setSampleBuffers(True)
        fmt.setDepthBufferSize(24)

        super(Window, self).__init__(fmt, None)
        self.setFixedSize(size[0], size[1])
        self.move(QtWidgets.QDesktopWidget().rect().center() - self.rect().center())
        self.setWindowTitle(title)

        self.start_time = time.clock()
        self.application = lambda: None
        self.app = None

        self.wnd = WindowInfo()
        self.wnd.viewport = (0, 0) + (size[0] * self.devicePixelRatio(), size[1] * self.devicePixelRatio())
        self.wnd.size = size


    def keyPressEvent(self, event):
        # Quit when ESC is pressed
        # print('Pressed {}'.format(event.nativeVirtualKey() & 0xFF))
        if event.key() == QtCore.Qt.Key_Escape:
            QtCore.QCoreApplication.instance().quit()
        elif event.key() == QtCore.Qt.Key_Q:
            QtCore.QCoreApplication.instance().quit()

        self.wnd.keys[event.nativeVirtualKey() & 0xFF] = True

    def keyReleaseEvent(self, event):
        self.wnd.keys[event.nativeVirtualKey() & 0xFF] = False

    def mouseMoveEvent(self, event):
        self.wnd.mouse = (event.x(), event.y())

    def mousePressEvent(self, event):
        self.wnd.mouse = (event.x(), event.y())
        self.wnd.old_mouse = self.wnd.mouse
        button = (event.button() & -event.button()).bit_length() - 1
        self.wnd.buttons[button] = True

    def mouseReleaseEvent(self, event):
        self.wnd.mouse = (0,0)
        self.wnd.old_mouse = (0,0)
        button = (event.button() & -event.button()).bit_length() - 1
        self.wnd.buttons[button] = False

    def wheelEvent(self, event):
        self.wnd.wheel += event.angleDelta().y()

    def resizeGL(self, w, h):
        self.wnd.size = (w, h)
        self.wnd.viewport = (0, 0, w * self.devicePixelRatio(), h * self.devicePixelRatio())

    def paintGL(self):
        if self.app is None:
            self.app = self.application()
        current = time.clock() - self.start_time
        self.wnd.dt = current - self.wnd.time
        self.wnd.time = current

        # update viewport
        self.app.set_viewport_size( self.wnd.viewport[2:4] )

        # toggle settings
        if self.wnd.key_pressed(114) or self.wnd.key_pressed(82): # r or R
            self.app.reset()

        if self.wnd.key_pressed(108) or self.wnd.key_pressed(76): # l or L
            self.app.toggle_light()

        if self.wnd.key_pressed(99) or self.wnd.key_pressed(67): # c or C
            self.app.toggle_color()

        if self.wnd.key_pressed(116) or self.wnd.key_pressed(84): # t or T
            self.app.toggle_texture()


        # if self.wnd.wheel != 0:
        #     if self.wnd.key_down(227): # Left CTRL
        #         self.app.camera_roll(self.wnd.dt * self.wnd.wheel * 30)
        #     else:
        #         self.app.camera_zoom(self.wnd.dt * self.wnd.wheel * 0.5)

        # if self.wnd.buttons[0]:
        #     distX = self.wnd.mouse[0] - self.wnd.old_mouse[0]
        #     distY = self.wnd.mouse[1] - self.wnd.old_mouse[1]
        #     if self.wnd.key_down(225): # Left SHIFT
        #         self.app.object_move(distX/1000.0, distY/1000.0)
        #     elif self.wnd.key_down(227): # Left CTRL
        #         self.app.camera_pitch(distX/10.0)
        #         self.app.camera_yaw(distY/10.0)
        #     else:
        #         self.app.camera_orbitH(distX/5.0)
        #         self.app.camera_orbitV(distY/5.0)

        if self.wnd.key_down(233):
            if self.wnd.wheel != 0:
                if self.wnd.key_down(227): # Left CTRL
                    self.app.object_roll(self.wnd.dt * self.wnd.wheel * 3)
                else:
                    self.app.object_zoom(self.wnd.dt * self.wnd.wheel * 0.1)

            if self.wnd.buttons[0]:
                distX = self.wnd.mouse[0] - self.wnd.old_mouse[0]
                distY = self.wnd.mouse[1] - self.wnd.old_mouse[1]
                if self.wnd.key_down(225): # Left SHIFT
                    self.app.object_move(distX/1000.0, distY/1000.0)
                elif self.wnd.key_down(227): # Left CTRL
                    self.app.object_pitch(distX/10.0)
                    self.app.object_yaw(distY/10.0)
                else:
                    self.app.object_orbitH(distX/5.0)
                    self.app.object_orbitV(distY/5.0)
        else:
            if self.wnd.wheel != 0:
                if self.wnd.key_down(227): # Left CTRL
                    self.app.camera_roll(self.wnd.dt * self.wnd.wheel * 30)
                else:
                    self.app.camera_zoom(self.wnd.dt * self.wnd.wheel * 0.1)
                    print(self.wnd.dt * self.wnd.wheel * 0.01)
            if self.wnd.buttons[0]:
                distX = self.wnd.mouse[0] - self.wnd.old_mouse[0]
                distY = self.wnd.mouse[1] - self.wnd.old_mouse[1]
                if self.wnd.key_down(225): # Left SHIFT
                    self.app.camera_move(distX/1000.0, distY/1000.0)
                elif self.wnd.key_down(227): # Left CTRL
                    self.app.camera_pitch(distX/10.0)
                    self.app.camera_yaw(distY/10.0)
                else:
                    self.app.camera_orbitH(distX/5.0)
                    self.app.camera_orbitV(distY/5.0)



        # keys_down = [key for key in range(255) if self.wnd.key_pressed(key)]
        # keys_up = [key for key in range(255) if self.wnd.key_released(key)]
        # if keys_down: print('Keys pressed: {}'.format(keys_down))
        # if keys_up: print('Keys released: {}'.format(keys_up))

        self.app.update(self.wnd.dt)
        self.app.render()

        if self.wnd.key_pressed(115) or self.wnd.key_pressed(83): # s or S
            self.app.postprocess()




        self.wnd.old_mouse = self.wnd.mouse
        self.wnd.old_keys = np.copy(self.wnd.keys)
        self.wnd.old_buttons = np.copy(self.wnd.buttons)
        self.wnd.wheel = 0
        # self.wnd.mouse = (0,0)
        self.update()


