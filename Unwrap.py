import bpy

class Unwrap(object):
    
    def __init__(self, ob = None):
        self.ob = None
        
    def unwraping(self,ob):
        if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
            bpy.context.scene.objects.active = bpy.data.objects[str(ob.name)] # seteando objeto activo
            myobject = bpy.data.objects[str(ob.name)]
            myobject.select = True

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.uv.unwrap(method='ANGLE_BASED', fill_holes=True, correct_aspect=True, use_subsurf_data=False, uv_subsurf_level=1)
            bpy.ops.object.mode_set(mode='OBJECT')
            myobject.select = False
            bpy.context.active_object.name = '' # deseteando active object
            bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
