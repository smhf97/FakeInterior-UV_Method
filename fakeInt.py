# notes:
# felan ba 4 noghte --> shayad behtar bashe safhamoon bishtar noghte dashte bashe?
# todo age perspective, moraba' nabood chi? noghte ha ro yeki yeki harekat bedim nesbat be gooshe ha
# todo why x? should be the normal axis of the window plane
# todo window vasat nabashe

# imports and defines
import bpy
import mathutils
from mathutils import Vector
import math
import sys
import os
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)
from importlib import reload
from UV_Util import UV_Util
reload(sys.modules['UV_Util']) # todo check existance

bpy.app.handlers.frame_change_pre.clear()

TOP_L = 0
BUTTOM_L = 1
BUTTOM_R = 2
TOP_R = 3

# give these info from user
# moraba'e perspective: (with grease pencil preferably)
image_size = bpy.data.images['one-room-apartment.jpg'].size
pers_TL = Vector((92, 388))
pers_BL = Vector((92, 159))
pers_TR = Vector((424, 390))
pers_BR = Vector((422, 163))

window_length = 1
room_x_size = 4
room_y_size = 4
# room_height = 4
# window_height = 1.5
window_point = Vector(bpy.data.objects['Window'].location[:2])
window_left = window_point - Vector((window_length/2, 0))
window_right = window_point + Vector((window_length/2, 0))
room_TL = window_point + Vector((-room_x_size/2, room_y_size))
room_TR = window_point + Vector((room_x_size/2, room_y_size))
room_BL = window_point - Vector((room_x_size/2, 0))
room_BR = window_point + Vector((room_x_size/2, 0))

# logic
obj = bpy.context.active_object
cam = bpy.data.objects['Camera']
uv_util = UV_Util(obj)

def distance_po_po_2d(point1, point2):
    diff = point1 - point2
    return math.sqrt(diff.dot(diff))

def initialize_lengths():
    # todo note: if the window is not moving, can pre calculated these points
    window_point = bpy.data.objects['Window'].location[:2]
    window_left = window_point - Vector((window_length/2, 0))
    window_right = window_point + Vector((window_length/2, 0))
    room_TL = window_point + Vector((-room_x_size/2, room_y_size))
    room_TR = window_point + Vector((room_x_size/2, room_y_size))
    room_BL = window_point - Vector((room_x_size/2, 0))
    room_BR = window_point + Vector((room_x_size/2, 0))

def top_view_po_to_x(vis_point, state):
    if state == 'L':
        x_pos = (vis_point.y - window_point.y) / room_y_size * pers_BL.x
    elif state == 'T':
        x_pos = (vis_point.x - room_BL.x) / room_x_size * (pers_TR.x - pers_BL.x) + pers_BL.x
    else:
        x_pos = image_size[0] - (vis_point.y - window_point.y) / room_y_size * (image_size[0] - pers_TR.x)
    return x_pos

def calculate_state_and_vis_point(window_side_point):
    cam_point = Vector(cam.location[:2])

    vis_line_dir = (window_side_point - cam_point)
    vis_line_dir.normalize()
    window_side_point = window_side_point + vis_line_dir * (room_x_size + room_y_size)

    vis_point = mathutils.geometry.intersect_line_line_2d(cam_point, window_side_point, room_TL, room_TR)
    state = 'T'
    
    if vis_point is None:
        vis_point = mathutils.geometry.intersect_line_line_2d(cam_point, window_side_point, room_TL, room_BL)
        state = 'L'
        if vis_point is None:
            state = 'R'
            vis_point = mathutils.geometry.intersect_line_line_2d(cam_point, window_side_point, room_TR, room_BR)
    return state, vis_point

def calculate_horizontal_points():
    
    left_state, left_vis_point = calculate_state_and_vis_point(window_left)
    right_state, right_vis_point = calculate_state_and_vis_point(window_right)
        
    left_x_pos = top_view_po_to_x(left_vis_point, left_state)
    right_x_pos = top_view_po_to_x(right_vis_point, right_state)
    
    return left_x_pos, right_x_pos

def main(scene):
    print('main')
    
    # calculate the position of the vertical edges of uv
    left_x_pos, right_x_pos = calculate_horizontal_points()
    print(left_x_pos, right_x_pos)
    uv_util.set_edge_pos(left_x_pos/image_size[0], 'L', 'x')
    print('after set left edge')
    uv_util.set_edge_pos(right_x_pos/image_size[0], 'R', 'x')    

bpy.app.handlers.frame_change_pre.append(main)
