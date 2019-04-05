# BananaRenderer

Renders a banana (or any other textured CAD model) from a given perspective to an image/depth file with annotated bounding box.

## Requirements
python > 3.5
moderngl
numpy
pillow
pyrr
PyQt5 == 5.9.1
matplotlib

## Installation
`python3 -m pip install --user -r requirements.txt`

## Usage

Four modes are available for rendering:
* banana look: Render banana using an interactive window
* banana peel: Render banana from N random camera poses
* banana chop: Render banana from given camera pose
* banana eat: Render banana from given camera pose files

### Look
usage: `./banana look`

Use mouse and keyboard to renderer current view to file.
Keys:
* l/L: toggle light source
* t/T: toggle texture
* c/C: toggle color overlay
* r/R: reset camera/model
* s/S: save current view
* q/Q/ESC: Quit application

Mouse:
* Left button + move: Rotate (yaw, pitch)
* Ctrl + Wheel: Rotate (roll)
* Shift + move: Translate (x,y)
* Wheel: Zoom in/out (z)

Holding the _Alt_ key modifies the object frame instead of the camera frame.

### Peel
usage: `./banana peel [-d distance] N`

Generate rendered images from _N_ random camera position looking towards the world origin from an optionally given distance _d_ (in meter).

### Chop
usage: `./banana peel x y z [qx qy qz qw] [roll pitch yaw]`

Generate a single rendered image from a given position (x,y,z).
Optionally, the orientation of the camera can be specified using a quaternion or euler angles (in degrees).

### Eat
usage: `./banana eat file [file ...]`

Generate rendered images from multiple pose files (each line has to be in the format `x y z qx qy qz qw` or `x y z roll pitch yaw`).
Note that each file can have multiple lines with poses.


## ToDo

* Wrong Euler convention for quaternion conversion. So use quaternions for now.
* Model matrix can only edited from interactive mode. Need option when using cli/file as well.
* Improve camera control.

