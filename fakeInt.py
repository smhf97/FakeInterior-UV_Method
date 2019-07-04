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
BOTTOM_L = 1
BOTTOM_R = 2
TOP_R = 3

# give these info from user
# moraba'e perspective: (with grease pencil preferably)
image_size = bpy.data.images['one-room-apartment.jpg'].size
pers_TL = Vector((92, 388))
pers_BL = Vector((92, 159))
pers_TR = Vector((424, 390))
pers_BR = Vector((422, 163))

window_length = 1
window_height = 1.5
windwo_size = Vector((1, 1.5))

room_x_size = 4
room_y_size = 4
room_height = 4
room_size = Vector((4, 4, 4))

window_point = Vector(bpy.data.objects['Window'].location)
window_point_right_view = Vector((window_point.z, window_point.y))
window_point_top_view = Vector(window_point[:2])
window_left = window_point_top_view - Vector((windwo_size[0]/2, 0))
window_right = window_point_top_view + Vector((windwo_size[0]/2, 0))
window_top = window_point_right_view + Vector((windwo_size[1]/2, 0))
window_bottom = window_point_right_view - Vector((windwo_size[1]/2, 0))

# (x (top view), z (right view))
room_TL = (window_point_top_view + Vector((-room_size.x/2, room_size.y)), window_point_right_view + Vector((room_size.z/2, room_size.y)))
room_TR = (window_point_top_view + Vector((room_size.x/2, room_size.y)), window_point_right_view + Vector((-room_size.z/2, room_size.y)))
room_BL = (window_point_top_view + Vector((-room_size.x/2, 0)), window_point_right_view + Vector((room_size.z/2, 0)))
room_BR = (window_point_top_view + Vector((room_size.x/2, 0)), window_point_right_view + Vector((-room_size.z/2, 0)))

obj = bpy.context.active_object
cam = bpy.data.objects['Camera'] # from user

# logic
uv_util = UV_Util(obj)

def distance_po_po_2d(point1, point2):
    diff = point1 - point2
    return math.sqrt(diff.dot(diff))

def map_3d_to_uv(axis, vis_point, state):
    if state == 'L':
        pos = abs(vis_point.y - window_point.y) / room_size.y * pers_BL[axis//2]
    elif state == 'T':
        pos = abs(vis_point.x - room_BL[axis//2].x) / room_size[axis] * abs(pers_TR[axis//2] - pers_BL[axis//2]) + pers_BL[axis//2]
    else:
        pos = image_size[axis//2] - abs(vis_point.y - window_point.y) / room_size.y * abs(image_size[axis//2] - pers_TR[axis//2])
    return pos

def calculate_state_and_vis_point(axis, window_side_point):
    cam_point = Vector((cam.location[axis], cam.location[1]))

    vis_line_dir = window_side_point - cam_point
    vis_line_dir.normalize()
    window_side_point = window_side_point + vis_line_dir * (room_size[axis] + room_size.y)

    vis_point = mathutils.geometry.intersect_line_line_2d(cam_point, window_side_point, room_TL[axis//2], room_TR[axis//2])
    state = 'T'
    if vis_point is None:
        vis_point = mathutils.geometry.intersect_line_line_2d(cam_point, window_side_point, room_TL[axis//2], room_BL[axis//2])
        state = 'L'
        if vis_point is None:
            state = 'R'
            vis_point = mathutils.geometry.intersect_line_line_2d(cam_point, window_side_point, room_TR[axis//2], room_BR[axis//2])
    return state, vis_point

def calculate_UV_co():
    left_state, left_vis_point = calculate_state_and_vis_point(0, window_left)
    right_state, right_vis_point = calculate_state_and_vis_point(0, window_right)
        
    left_x_pos = map_3d_to_uv(0, left_vis_point, left_state)
    right_x_pos = map_3d_to_uv(0, right_vis_point, right_state)
    
    top_state, top_vis_point = calculate_state_and_vis_point(2, window_top)
    bottom_state, bottom_vis_point = calculate_state_and_vis_point(2, window_bottom)

    top_y_pos = map_3d_to_uv(2, top_vis_point, top_state)
    bottom_y_pos = map_3d_to_uv(2, bottom_vis_point, bottom_state)
 
    return left_x_pos, right_x_pos, top_y_pos, bottom_y_pos

def main(scene):
    print('main')

    # calculate the position of the edges of uv plane 
    left_x_pos, right_x_pos, top_y_pos, bottom_y_pos = calculate_UV_co()
    print(top_y_pos, bottom_y_pos)
    uv_util.set_edge_pos(left_x_pos/image_size[0], 'L', 'x')
    uv_util.set_edge_pos(right_x_pos/image_size[0], 'R', 'x')
    uv_util.set_edge_pos(1 - top_y_pos/image_size[1], 'T', 'y')
    uv_util.set_edge_pos(1 - bottom_y_pos/image_size[1], 'B', 'y')   

bpy.app.handlers.frame_change_pre.append(main)
