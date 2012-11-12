# License:
''' Copyright (c) 2012 Jorge Hernandez - Melendez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
bl_info = {
    "name": "Automatic UVProjection",
    "description": "Quickly and easy create projects of Camera Mapping",
    "author": "Jorge Hernandez - Melenedez",
    "version": (1, 6),
    "blender": (2, 63, 0),
    "api": 31236,
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": ""}

#import os
#print( str( os.getcwd() ) )
#C:\Program Files\Blender Foundation\blender-2.64-RC2-windows64

import sys
#RUTA="C:/Users/tux/AppData/Roaming/Blender Foundation/Blender/2.63/scripts/addons/UVProjection"
RUTA="/home/zenx/Blender/blender-2.64a-linux-glibc27-x86_64/2.64/scripts/addons/uvprojection"
sys.path.append(RUTA)

import bpy
from Vistas import *
from Unwrap import *
from Uvmod import *
from Material import *
from Proyector import *
from Tipocoordenadas import *
from Update import *

u = Unwrap()
v = Vistas()
um = Uvmod()
m = Material()
p = Proyector()
tc = Tipocoordenadas()
up = Update()

# para el listado de objetos esto es necesario:
# son como propiedades para el item de interfaz:
bpy.types.Object.Proyector = bpy.props.StringProperty()
bpy.types.Scene.IBPath = bpy.props.StringProperty(name="", attr="custompath", description="Base Image Path", maxlen= 1024, default="")


# el comodin contiene la imagen actual del loader.
comodin = bpy.data.textures.new(type='IMAGE', name='comodin')

# intento de hacer un boton de reload addon (pero no tiene mucho sentido crear este boton)
#def restart_addon():
#    bpy.ops.wm.addon_disable(module='UVProjection')
#    bpy.ops.wm.addon_enable(module='UVProjection')

# Menu in toolprops region
class Botones_UVProjection(bpy.types.Panel):
    bl_label = "Automatic UVProjection v16"
    bl_space_type = "VIEW_3D"
    #bl_region_type = "TOOL_PROPS"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        #layout.label("hola mundo")
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'
        
        # intento de hacer un boton de reload addon (pero no tiene mucho sentido crear este boton)
        #col.operator("restarta.restarta", text='Reload Addon')
                
        #col.operator("object.custom_path")
        #col.prop(context.scene,"IBPath")
        
        #Al crear una nueva escena con ctrl + n el addon no se recargaba y el comodin no se volvia a crear, de esta manera si no esta se crea:
        try:
            # primero intento de manera normal:
            comodin = bpy.data.textures[0]
            col.template_image(comodin, "image", comodin.image_user)
            
        except:
            # si da error seguramente es una escena nueva por lo tanto lo creo otra vez:
            if bpy.data.textures[0].name != 'comodin':
                comodin = bpy.data.textures.new(type='IMAGE', name='comodin')
                
            comodin = bpy.data.textures[0]
            col.template_image(comodin, "image", comodin.image_user)

        ''' # Esto lo dejo para futuras versiones  :)
        # listado de objetos en desplegable: en concreto del objeto activo:
        #col.prop(context.scene.objects, "active", text="Proyector? :")
        
        # listado de objetos en la escena:
        # el string Proyector llama una parte creada arriba
        # donde el string cameras puede ir meshes dependiendo de lo que quisieramos :)
        col.prop_search(context.object, "Proyector", bpy.data, "cameras")
        # para obtener el valor de el item actual de el listado de objetos de la escena:
        # lo podemos sacar de: bpy.context.object.Proyector

        # para cambiar el nombre real de la camara:
        # bpy.data.cameras['Camera.001'].name = "jojo"
        # bpy.context.scene.camera.data.name = "grr"
        '''

        #col.operator("ol.ol", text='(Only) load image to blender')
        col.operator("toselected.toselected", text='To Selected')
        col.operator("mod.mod", text='To ALL')
        #col.operator("unwrapeado.unwrapeado", text='(Only) Auto UnWrap for all')
        col.operator("uprel.uprel", text='(Only) Update Relationships Mat-Rend')

# intento de hacer un boton de reload addon (pero no tiene mucho sentido crear este boton)        
#class RECARGA(bpy.types.Operator):
#    bl_idname = "restarta.restarta"
#    bl_label = "Reload Addon"
#
#    def execute(self, context):
#        restart_addon()

def imagen():
    #img = bpy.data.images.load(filepath=bpy.context.scene.IBPath)
    img = bpy.data.textures[0].image
    #img.use_premultiply = True
    return img


class AccionToselected(bpy.types.Operator):
    bl_idname = "toselected.toselected"
    bl_label = "To Selected"
    
    def execute(self, context):
        # capturo el objeto en cuestion:
        ob = bpy.context.selected_objects
        # acciones:
        p.proyectorcillo(ob)
                
        if ob:
            try:
                img = imagen()
                
                # si son muchos por eso me lo recorro:
                for i in range(len(ob)):
                    if ob[i].type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                        sobject = ob[i]
                        # selecciono el objeto correspondiente a esa pasada:
                        sobject.select = True

                        # hago las acciones:
                        u.unwraping(sobject)
                        # uvmod requiere de la imagen se la paso por argumentos:
                        um.uvmod(sobject,img)
                        m.trymat(sobject,img)

                        # seteamos la imagen al modificador
                        sobject.modifiers['UV_PROJECT'].image = img # seteamos la imagen
                        # le seteamos las coordenadas de tipo de mapeo:
                        tc.uvgenerated(sobject)
                        # actualizamos las relaciones:
                        
                        up.update(ob)
                        v.vision()
                        
            except:
                pass
        
        
        return{'FINISHED'}
        
class Accion_ToALL(bpy.types.Operator):
    bl_idname = "mod.mod"
    bl_label = "Apply/Update Modifier"

    def execute(self, context):

        try:
        
            img = imagen()

            for ob in bpy.data.objects:
                if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                    p.proyectorcillo(ob)         
                    xloc = bpy.data.objects['Locator']
                    xloc.show_x_ray = True

                    
                     # hago las acciones:
                    u.unwraping(ob)
                    # uvmod requiere de la imagen se la paso por argumentos:
                    um.uvmod(ob,img)
                    m.trymat(ob,img)

                    # seteamos la imagen al modificador
                    ob.modifiers['UV_PROJECT'].image = img # seteamos la imagen
                    # le seteamos las coordenadas de tipo de mapeo:
                    tc.uvgenerated(ob)
                    # actualizamos las relaciones:

                    up.update(ob)
                    v.vision()
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
        v.vision()
        return{'FINISHED'}

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()