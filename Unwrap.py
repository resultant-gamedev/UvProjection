import bpy

def uwap_cn_nombre(): 
    # mapas uv
    slots_uvs = bpy.context.object.data.uv_textures

    # obteniendo los mapas uv existentes:
    muvex = []
    for i in range(len(slots_uvs)):
        muvex.append(slots_uvs[i].name)

    numero_slots = len(slots_uvs)
    
    # hacemos backup de todo lo que no es un backups previo ni uvprojection:
    for i in range(numero_slots):
        # chekeo backup previo (si da 0 es que hay coincidencias):
        if slots_uvs[i].name.find('bkup_') != 0 and slots_uvs[i].name != 'uvprojection':
            slots_uvs[i].name = "bkup_" + slots_uvs[i].name

    # si solo tiene un backup tendremos que agregar un nuevo slot:
    for i in range(numero_slots):
        # chekeo backup previo (si da 0 es que hay coincidencias):
        if slots_uvs[i].name.find('bkup_') == 0 and numero_slots == 1:
            bpy.ops.mesh.uv_texture_add() # agregando slot de mapa uv (por defecto de nombre UVMap)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.uv.unwrap(method='ANGLE_BASED', fill_holes=True, \
            correct_aspect=True,use_subsurf_data=False, uv_subsurf_level=6)
            bpy.ops.object.mode_set(mode='OBJECT')
    
    # si no tiene nada:
    if numero_slots < 1: # si no hay algun mapa uv
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.uv_texture_add() # agregando slot de mapa uv (por defecto de nombre UVMap)
        bpy.ops.uv.unwrap(method='ANGLE_BASED', fill_holes=True, \
        correct_aspect=True,use_subsurf_data=False, uv_subsurf_level=6)
        bpy.ops.object.mode_set(mode='OBJECT')
        
    try:
        # renombrar mapa uv
        bpy.context.object.data.uv_textures['UVMap'].name = "uvprojection"
    except:
        pass

class Unwrap(object):
    
    def __init__(self, ob = None):
        self.ob = None
        
    def unwraping(self,ob):
        if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
            bpy.context.scene.objects.active = bpy.data.objects[str(ob.name)] # seteando objeto activo
            myobject = bpy.data.objects[str(ob.name)]
            myobject.select = True
   
            uwap_cn_nombre()
            
            bpy.data.meshes[bpy.context.active_object.data.name].uv_textures["uvprojection"].active_render = True # aciendo el uvmap activo en el render
            
            myobject.select = False
            bpy.context.active_object.name = '' # deseteando active object
            bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
