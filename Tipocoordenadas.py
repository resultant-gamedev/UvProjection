import bpy

class Tipocoordenadas(object):
    
    def __init__(self, ob = None):
        self.ob = None
        
    def uvgenerated(self,ob):
    
            """if len(ob.data.materials) == 0: # si no tiene material por lo que sea...
            #if len(ob.material_slots) == 0:
                if len(bpy.data.materials) != 0: # compruebo si existe algun material y si existe le aplico el primero:
                    ob.data.materials.append(bpy.data.materials[0])
                #else:
                    # si no existen materiales creo uno
                    #bpy.ops.material.new()
            """
            
            # seteando el tipo de coordenadas "UV" en lugar de "Generated"
            ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].texture_coords = 'UV'

            ob.modifiers['UV_PROJECT'].uv_layer = "UVTex" # seteando su valor a UVTex (Nomenglatura antigua)
            if ob.modifiers['UV_PROJECT'].uv_layer == '':
                ob.modifiers['UV_PROJECT'].uv_layer = "UVMap" # seteando su valor a UVMap

            UVMapeado = ob.modifiers['UV_PROJECT'].uv_layer

            if ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].uv_layer == '':
                ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].uv_layer = UVMapeado

            #seteando que use tb como alpha:
            ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].use_map_alpha = True