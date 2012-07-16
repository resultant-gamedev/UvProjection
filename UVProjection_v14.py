# License:
# Automatic UVProjection by Jorge Hernandez - Melendez is licensed under a 
# Creative Commons Attribution-NoComercial-CompartirIgual 3.0 Unported.
# http://creativecommons.org/licenses/by-nc-sa/3.0/

# Release date: 20/04/2012
# format date:  DD/MM/YY

bl_info = {
    "name": "Automatic UVProjection",
    "description": "Quickly and easy create projects of Camera Mapping",
    "author": "Jorge Hernandez - Melenedez",
    "version": (1, 4),
    "blender": (2, 63, 0),
    "api": 31236,
    "location": "View3D > Add > Mesh",
    "warning": "", 
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

import bpy
from bpy.props import *


bpy.types.Scene.IBPath = StringProperty(name="", attr="custompath", description="Base Image Path", maxlen= 1024, default="")

def modificar_textura_default():
    #configuro la imagen por default para poder usar el loader de imagenes:
    #textura = bpy.data.textures[0]
    textura = bpy.data.scenes.data.textures['Tex']
    #textura = bpy.data.textures['Tex']
    #text = D.textures[0]
    #tex = D.objects[1].active_material.texture_slots[0].texture
    textura.type = 'IMAGE'
    return textura

textura = modificar_textura_default()

# Botones ############################################:

# Menu in toolprops region
class Botones(bpy.types.Panel):
    bl_label = "Automatic UVProjection v14"
    bl_space_type = "VIEW_3D"
    #bl_region_type = "TOOL_PROPS"
    bl_region_type = "TOOLS"
    
    # desde aqui si puede cambiar el type pero luego desde draw usando self la primera vez va bien pero 
    # si creas una escena nueva peta :S 
    #textura = modificar_textura_default()
    
    def draw(self, context):
        layout = self.layout
        #layout.label("hola mundo")
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'

        #col.operator("object.custom_path")
        #col.prop(context.scene,"IBPath")
        
        # le vuelvo a decir quien es la imagen por default por que parece que no la pillaba...
        textura = bpy.data.textures['Tex']
        #col.template_image(self.textura, "image", self.textura.image_user) #<-- uso la imagen por default para que se despliegue el loader
        col.template_image(textura, "image", textura.image_user) #<-- uso la imagen por default para que se despliegue el loader
         
        #col.operator("ol.ol", text='(Only) load image to blender')
        col.operator("toselected.toselected", text='To Selected')
        col.operator("mod.mod", text='To ALL') 
        #col.operator("unwrapeado.unwrapeado", text='(Only) Auto UnWrap for all')
        col.operator("uprel.uprel", text='(Only) Update Relationships Mat-Rend')
        


class OBJECT_OT_custompath(bpy.types.Operator):
    bl_idname = "object.custom_path"
    bl_label = "Browse Base Image..."
    __doc__ = ""
    #this can be look into the one of the export or import python file.
    #need to set a path so so we can get the file name and path
    filepath = StringProperty(name="ruta2", description="rutika", maxlen= 1024, default= "")
    
    def execute(self, context):
        #set the string path fo the file here.
        #this is a variable created from the top to start it
        bpy.context.scene.IBPath = self.properties.filepath
        print(self.properties.filepath)#display the file name and current path        
        return {'FINISHED'}
        
    def invoke(self, context, event):
        wm = context.window_manager
        wm.fileselect_add(self)
        return {'RUNNING_MODAL'}

    
def viewports():
    # Poniendo todos los viewports comunes en modo textured:
    bpy.context.blend_data.screens[0].areas[4].spaces[0].viewport_shade = 'TEXTURED' # vista animation a textured
    bpy.context.blend_data.screens[2].areas[4].spaces[0].viewport_shade = 'TEXTURED' # vista default a textured
    bpy.context.blend_data.screens[4].areas[2].spaces[0].viewport_shade = 'TEXTURED' # vista scripting a textured
    #bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
    bpy.data.scenes['Scene'].game_settings.material_mode = 'GLSL'
    # ponemos todas las imagenes en premultiply:
    for i in bpy.data.images[:]:
        bpy.data.images[i.name].use_premultiply = True

def imagen():
    #img = bpy.data.images.load(filepath=bpy.context.scene.IBPath)
    img = bpy.data.textures[0].image
    #img.use_premultiply = True
    return img
    
def uvgenerated(ob):
        # seteando uv en lugar de generated al shader
        ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].texture_coords = 'UV'
        
        ob.modifiers['UV_PROJECT'].uv_layer = "UVTex" # seteando su valor a UVTex (Nomenglatura antigua)
        if ob.modifiers['UV_PROJECT'].uv_layer == '':
            ob.modifiers['UV_PROJECT'].uv_layer = "UVMap" # seteando su valor a UVMap
        
        UVMapeado = ob.modifiers['UV_PROJECT'].uv_layer
        
        if ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].uv_layer == '':
            ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].uv_layer = UVMapeado
        
        #seteando que use tb como alpha:
        ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].use_map_alpha = True
    
def trymat(ob,img):
    try:
        
        if "MatScreen" not in ob.data.materials or img != ob.data.materials[0].texture_slots[0].texture.image.name:
            
            ######## materiales ############
            def MiMaterial():
                mat = bpy.data.materials.new("MatScreen")
                mat.use_shadeless = True
                mat.use_transparency = True
                mat.alpha = 0
                return mat
            multimat = MiMaterial()

            if len(ob.data.materials) == 0:
                ob.data.materials.append(multimat)    

            ob.data.materials[0] = multimat
        
            slot = ob.data.materials[ob.data.materials[0].name].texture_slots.add()
            ob.data.materials[ob.data.materials[0].name].texture_slots.clear(1)
            
        
            
            if ob.data.materials[ob.data.materials[0].name].texture_slots[0].name == '':
                tipoimg = bpy.data.textures.new(type='IMAGE', name='ImageBase')
                slot.texture = tipoimg
                
            

            ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].texture.image = img
        
            ######## fin materiales ######## 

            # reaplicando settings al modificador:
            camara = bpy.data.objects["Proyector"]
            modificador = ob.modifiers["UV_PROJECT"]
            modificador.projector_count = 1
            modificador.projectors[0].object = camara
            
    except:
        pass
    
def proyectorcillo():
    #if 'Proyector' in bpy.context.scene.objects:
    if 'Proyector' in bpy.data.objects:
    # al parecer al borrar con x y con supr no elimina los objetos de bpy.data.objects, les hace un unlink
    # por eso, si existe le digo que le haga link para que vuelva a aparecer el proyector:
        try:
            bpy.context.scene.objects.link(bpy.data.objects['Proyector'])
        except:
            pass
    else:
        # creamos el proyector:
        bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0, -9, 0), rotation=(1.5708, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        ob = bpy.context.active_object  # obteniendo objeto activo 
        ob.name = "Proyector" 
        
        bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        emp = bpy.context.active_object  # obteniendo objeto activo
        emp.name = "Locator"
        
        
        #bpy.ops.object.select_name(name=ob.name, extend=True) # <--- OLD
        #bpy.ops.object.select_name(name=emp.name, extend=True) # <--- OLD
        myobject = bpy.data.objects[str(ob.name)]
        myobject.select = True
        myobject = bpy.data.objects[str(emp.name)]
        myobject.select = True
        
        
        bpy.ops.object.parent_set(type='OBJECT')
        bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        #bpy.ops.object.select_name(name=emp.name, extend=False) # <--- OLD
        myobject = bpy.data.objects[str(emp.name)]
        myobject.select = True
            
        
    if 'Locator' not in bpy.data.objects:	
        bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        emp = bpy.context.active_object  # obteniendo objeto activo
        emp.name = "Locator"
        
        #bpy.ops.object.select_name(name='Proyector', extend=True)
        myobject = bpy.data.objects['Proyector']
        myobject.select = True
        #bpy.ops.object.select_name(name=emp.name, extend=True)
        myobject = bpy.data.objects[str(emp.name)]
        myobject.select = True
        
        bpy.ops.object.parent_set(type='OBJECT')
        bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        #bpy.ops.object.select_name(name=emp.name, extend=False)
        myobject = bpy.data.objects[str(emp.name)]
        myobject.select = True
        
        
def uvmod(ob):
    try:
        img = imagen()
    
        if "UV_PROJECT" not in ob.modifiers:
            ob.modifiers.new(name='UV_PROJECT', type='UV_PROJECT')
            ob.modifiers['UV_PROJECT'].use_image_override = True
            proyectorcillo()
            xloc = bpy.data.objects['Locator']
            xloc.show_x_ray = True
            camara = bpy.data.objects["Proyector"]
            modificador = ob.modifiers["UV_PROJECT"]
            modificador.projector_count = 1
            modificador.projectors[0].object = camara
            ob.modifiers['UV_PROJECT'].image = img # seteamos la imagen
            
        
    except:
        pass
    
    
def unwraping(ob):
    if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
        bpy.context.scene.objects.active = bpy.data.objects[str(ob.name)]  # seteando objeto activo
        myobject = bpy.data.objects[str(ob.name)]
        myobject.select = True
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.unwrap(method='ANGLE_BASED', fill_holes=True, correct_aspect=True, use_subsurf_data=False, uv_subsurf_level=1)
        bpy.ops.object.mode_set(mode='OBJECT')
        myobject.select = False
        bpy.context.active_object.name = '' # deseteando active object
        bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo


def seleccion():
    ob = bpy.context.selected_objects
    if ob:
        try:
            img = imagen()
            for i in range(len(ob)):
                if ob[i].type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                    sobject = ob[i]
                    sobject.select = True
                
                    unwraping(sobject)
                    uvmod(sobject)
                    trymat(sobject,img)
                    
                    #img = imagen()
                    
                    sobject.modifiers['UV_PROJECT'].image = img # seteamos la imagen
                    uvgenerated(sobject)
                    viewports()
                    update(sobject)
                
        except:
            pass
            
def update(ob):
    try:
        ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].texture.image = ob.modifiers['UV_PROJECT'].image
    except:
        pass


# Acciones ###########################################:
"""class OLOAD(bpy.types.Operator):
    bl_idname = "ol.ol"
    bl_label = "(Only) load image to blender"
    img = imagen()
    def execute(self, context):
        try:
            #bpy.data.images.load(filepath=bpy.context.scene.IBPath)
            bpy.data.images.load(filepath=img)
        except:
            pass
        return{'FINISHED'}"""

"""class UNWRAPEADO(bpy.types.Operator):
    bl_idname = "unwrapeado.unwrapeado"
    bl_label = "(Only) Auto UnWrap for all"
    def execute(self, context):
        for ob in bpy.data.objects:
            unwraping(ob)
        return{'FINISHED'}"""


class TOSEL(bpy.types.Operator):
    bl_idname = "toselected.toselected"
    bl_label = "To Selected"
    def execute(self, context):
        #img = imagen()
        seleccion()
        return{'FINISHED'}
        
class MODIFICADOR(bpy.types.Operator):
    bl_idname = "mod.mod"
    bl_label = "Apply/Update Modifier"
    
    def execute(self, context):
        try:
            img = imagen()
            proyectorcillo()
            xloc = bpy.data.objects['Locator']
            xloc.show_x_ray = True
            
            for ob in bpy.data.objects:
                if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                    
                        
                        unwraping(ob)
                        uvmod(ob)
                        trymat(ob,img)
                    
                        ob.modifiers['UV_PROJECT'].image = img # seteamos la imagen
                        uvgenerated(ob)
                        viewports()                        
                        update(ob)
        except:
            pass
                
                
        
        
        return{'FINISHED'}

class RELATIONS(bpy.types.Operator):
    bl_idname = "uprel.uprel"
    bl_label = "Update Relationship Material Modifier - Material Renderable"
    def execute(self, context):
        ob = bpy.context.active_object
        for ob in bpy.data.objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                try:
                    ob.material_slots[ob.data.materials[0].name].material.texture_slots[0].texture.image = ob.modifiers['UV_PROJECT'].image
                except:
                    pass
        viewports()
        return{'FINISHED'}

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
