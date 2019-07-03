import bpy
import mathutils

class UV_Util:
    def __init__(self, plane_obj):
        print('init')
        self.obj = plane_obj
        self.scale = mathutils.Vector((1, 1))
        
    def move_uv_vert(self, index, new_coordinate):
        UV_DATA = self.obj.data.uv_layers.active.data
        UV_DATA[index].uv = new_coordinate

    def set_scale(self, abs_scale, axis):
        self.scale_uv(1/self.scale.x, 'x')
        self.scale_uv(1/self.scale.y, 'y')
        self.scale_uv(abs_scale, axis)
        print('scaler {}, self.scale {}'.format(abs_scale, self.scale))

    def normalize_scale(self):
        pass
        # todo bargardoondan uv be shekle mostatil (avalie) va ba scale abs 1

    def scale_uv(self, scaler, axis):
        # around center
        center = self.get_center()
        UV_DATA = self.obj.data.uv_layers.active.data
        if 'x' in axis:
            self.scale.x = self.scale.x * scaler
        if 'y' in axis:
            self.scale.y = self.scale.y * scaler

        for uv_data in UV_DATA:
            if 'x' in axis:
                uv_data.uv.x = ((uv_data.uv - center) * scaler + center).x
                
            if 'y' in axis:
                uv_data.uv.y = ((uv_data.uv - center) * scaler + center).y

        # todo check the boundaries
    
    def get_center(self):
        UV_DATA = self.obj.data.uv_layers.active.data
        center = mathutils.Vector((0,0))
        for uv_data in UV_DATA:
            center = center + mathutils.Vector(uv_data.uv)
        return center/len(UV_DATA)