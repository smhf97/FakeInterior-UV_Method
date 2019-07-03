# notes:
# felan ba 4 noghte --> shayad behtar bashe safhamoon bishtar noghte dashte bashe?

# imports and defines
import bpy
import mathutils
import math
import sys
import os
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
from importlib import reload
reload(sys.modules['UV_Util']) 
from UV_Util import UV_Util

bpy.app.handlers.frame_change_pre.clear()

TOP_L = 0
BUTTOM_L = 1
BUTTOM_R = 2
TOP_R = 3

# logic

obj = bpy.context.active_object
cam = bpy.data.objects['Camera']
uv_util = UV_Util(obj)

def main(scene):
    print('main')
    # todo why x? should be the normal axis of the window plane
    x_distance = (cam.location.x - obj.location.x) # todo abs (ghadre motlagh)
    scaler = 10/x_distance
    uv_util.set_scale(scaler, 'xy')
    

def distance_from_cam(cam):
    obj_pos = mathutils.Vector(obj.location)
    cam_pos = mathutils.Vector(cam.location)
    diff = obj_pos - cam_pos
    return math.sqrt(diff.dot(diff))

bpy.app.handlers.frame_change_pre.append(main)

#for i, loop in enumerate(obj.data.loops):
#   obj.data.uv_layers.active.data[loop.index].uv = (0, 0)
#loops = obj.data.loops
#obj.data.uv_layers.active.data[loop.index].uv = (0, 0)