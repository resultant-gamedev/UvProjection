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
    "version": (1, 7),
    "blender": (2, 64, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": ""}

import bpy
import os, sys

# rutas ##############################################
NAB = "rojection" #<- Nombre Addon a Buscar

if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
    barra = "/"
elif sys.platform.startswith("win") or sys.platform.startswith("dos") or sys.platform.startswith("ms"):
    barra = "\\"
    
# rutas conocidas:
rutas_scripts = bpy.utils.script_paths()
rutas_addons = []
for i in range(len(rutas_scripts)):
    rutas_addons.append(str(rutas_scripts[i])+"/addons")

# creando array de addons disponibles:
all_addons = [] # contendra un array con 0 y 1 con los addons del usuario y los de el path de blender.
for i in range(len(rutas_addons)):
    all_addons.append(os.listdir(rutas_addons[i]))

# buscando en que ruta esta el addon:
for i in range(len(all_addons)):
    for a in all_addons[i]:
        if a.find(NAB) >= 0:
            ruta_encontrado = str(rutas_addons[i])
            print(ruta_encontrado)

# todos los addons del directorio en el que se encuentra mi addon:
addons_hermanos = os.listdir(ruta_encontrado)
for a in addons_hermanos:
    if a.find(NAB) >= 0:
        FOLDER_NAME=str(a)

#FOLDER_NAME="uvprojection"

for i in range(len(rutas_addons)):
    if os.path.exists(rutas_addons[i]+barra+FOLDER_NAME):
        RUTA = rutas_addons[i]+barra+FOLDER_NAME

sys.path.append(RUTA)
# fin rutas ##########################################

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




# intento de hacer un boton de reload addon (pero no tiene mucho sentido crear este boton)
#def restart_addon():
#    bpy.ops.wm.addon_disable(module='UVProjection')
#    bpy.ops.wm.addon_enable(module='UVProjection')

# Menu in toolprops region
class Botones_UVProjection(bpy.types.Panel):
    bl_label = "Automatic UVProjection"
    bl_space_type = "VIEW_3D"
    #bl_region_type = "TOOL_PROPS"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        #layout.label("hola mundo")
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'
        
        # el comodin contiene la imagen actual del loader.
        comodin = bpy.data.textures.new(type='IMAGE', name='comodin')
        
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
        
        col.label("Apply projections:")
        #col.operator("ol.ol", text='(Only) load image to blender')
        col.operator("toselected.toselected", text='To Selected')
        col.operator("mod.mod", text='To ALL')
        #col.operator("unwrapeado.unwrapeado", text='(Only) Auto UnWrap for all')
        col.operator("uprel.uprel", text='Update Relationships Mat-Rend')

        subrow0 = col.row(align=True)
        subrow0.operator("setwire.setwire", text='Wire On')
        subrow0.operator("unsetwire.unsetwire", text='Wire Off')
        
        # lock unlock
        subrow1 = col.row(align=True)
        subrow1.operator("lock.lock", text='Lock')
        subrow1.operator("unlock.unlock", text='Unlock')

        
        # para el modo de coordenadas:
        col.label("Handlers Orientations:")
        view = context.space_data
        orientation = view.current_orientation

        row = layout.row(align=True)
        col.prop(view, "transform_orientation", text="")
        #col.operator("transform.create_orientation", text="", icon='ZOOMIN')
        if orientation:
            row = layout.row(align=True)
            col.prop(orientation, "name", text="")
            col.operator("transform.delete_orientation", text="", icon="X")
        # fin modo coordenadas ################################################
        
        col.label("Camera/Locator settings:")
        
        # por ahora lo dejo inhabilitado
        #col.operator("updaterot.updaterot", text='Update locator orientation')
        
        col.operator("influencek.influencek", text='With influence Keep position')
        col.operator("noinfluencek.noinfluencek", text='Without influence Keep position')
        #subrow = col.row(align=True)
        #subrow.operator("influence.influence", text='With influence')
        #subrow.operator("noinfluence.noinfluence", text='Without influence')
        #subrow2 = col.row(align=True)
        #subrow2.operator("setinverse.setinverse", text='Set inverse')
        #subrow2.operator("clearinverse.clearinverse", text='Clear inverse')
        
        

def imagen():
    #img = bpy.data.images.load(filepath=bpy.context.scene.IBPath)
    img = bpy.data.textures[0].image
    #img.use_premultiply = True
    return img

class LockOb(bpy.types.Operator):
    bl_idname = "lock.lock"    
    bl_label = "Lock"
    bl_description = "Lock objects"
    def execute(self, context):
        
        if bpy.context.selected_objects:
            for o in bpy.context.selected_objects:
                for x in range(len(o.lock_location)):
                    o.lock_location[x] = True
                    o.lock_rotation[x] = True
                    o.lock_scale[x] = True
        else:
            for o in bpy.data.objects:
                for x in range(len(o.lock_location)):
                    o.lock_location[x] = True
                    o.lock_rotation[x] = True
                    o.lock_scale[x] = True

        return{'FINISHED'}

class UnLockOb(bpy.types.Operator):
    bl_idname = "unlock.unlock"    
    bl_label = "Lock"
    bl_description = "Lock objects"
    def execute(self, context):
        
        if bpy.context.selected_objects:
            for o in bpy.context.selected_objects:
                for x in range(len(o.lock_location)):
                    o.lock_location[x] = False
                    o.lock_rotation[x] = False
                    o.lock_scale[x] = False
        else:
            for o in bpy.data.objects:
                for x in range(len(o.lock_location)):
                    o.lock_location[x] = False
                    o.lock_rotation[x] = False
                    o.lock_scale[x] = False

        return{'FINISHED'}
    
class WireOn(bpy.types.Operator):
    bl_idname = "setwire.setwire"    
    bl_label = "Set wireframe mode On"
    bl_description = "Set wireframe mode On"
    def execute(self, context):
        if bpy.context.selected_objects:
            for o in bpy.context.selected_objects:
                o.show_wire = True
        else:
            for o in bpy.data.objects:
                o.show_wire = True
        return{'FINISHED'}

class WireOff(bpy.types.Operator):
    bl_idname = "unsetwire.unsetwire"
    bl_label = "UnSet wireframe mode Off"
    bl_description = "Set wireframe mode Off"
    
    def execute(self, context):
        if bpy.context.selected_objects:
            for o in bpy.context.selected_objects:
                o.show_wire = False
        else:
            for o in bpy.data.objects:
                o.show_wire = False
        return{'FINISHED'}
        
# no consigo hacer que funcione desde script ni script editor, solo funciona si lo ejecuto en la consola :S
# asi que por ahora lo dejare inhabilitado.
class UpdateRott(bpy.types.Operator):
    bl_idname = "updaterot.updaterot"
    bl_label = "Update orientation locator"
    bl_description = "Update orientation locator"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        myplocator = bpy.data.objects["Locator"]
        myplocator.select = True
        bpy.context.scene.objects.active = myplocator # lo hago objeto activo

        #bpy.ops.object.constraint_add(type='TRACK_TO')
        myplocator.constraints.new('TRACK_TO')
        myplocator.constraints["TrackTo"].target = bpy.data.objects["Proyector"]
        myplocator.constraints["TrackTo"].up_axis = 'UP_Y'
        myplocator.constraints["TrackTo"].track_axis = 'TRACK_Z'

        rotacion = []
        rotquat = []
        for i in myplocator.matrix_world.to_euler():
            rotacion.append(i)
            
        for i in myplocator.matrix_world.to_quaternion():
            rotquat.append(i)

        for i in range(len(rotacion)):
            if len(str(rotacion[i])) > 4:
                rotacion[i] = round(rotacion[i],4)

        for i in range(len(rotquat)):
            if len(str(rotquat[i])) > 4:
                rotquat[i] = round(rotquat[i],4)
                
        #rotaciones = [rotacion[0],rotacion[1],rotacion[2]]
        #rotaciones = [rotacion.x,rotacion.y,rotacion.z]

        cons = myplocator.constraints['TrackTo']
        myplocator.constraints["TrackTo"].target = None
        myplocator.constraints.remove(cons)
        bpy.context.active_object.rotation_mode='QUATERNION'
        bpy.context.active_object.rotation_euler = rotquat[0],rotquat[1],rotquat[2]
        bpy.context.active_object.rotation_mode='XYZ'
        bpy.context.active_object.rotation_euler = rotacion[0],rotacion[1],rotacion[2]
        #myplocator.rotation_euler = rotacion[0],rotacion[1],rotacion[2]
        
        return{'FINISHED'}
    
class Influence(bpy.types.Operator):
    bl_idname = "influence.influence"
    bl_label = "With influence"
    bl_description = "The projector will influence for locator"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        camara = bpy.data.objects["Proyector"]
        camara.select = True # la selecciono
        bpy.context.scene.objects.active = camara
        try:
            bpy.context.object.constraints["ChildOf"].influence = 1
            bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        except:
            pass
        return{'FINISHED'}

class NoInfluence(bpy.types.Operator):
    bl_idname = "noinfluence.noinfluence"
    bl_label = "Without influence"
    bl_description = "The projector will not influence for locator"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        camara = bpy.data.objects["Proyector"]
        camara.select = True # la selecciono
        bpy.context.scene.objects.active = camara
        try:
            bpy.context.object.constraints["ChildOf"].influence = 0
            bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        except:
            pass
        return{'FINISHED'}

class InfluenceK(bpy.types.Operator):
    bl_idname = "influencek.influencek"
    bl_label = "With influence Keep position"
    bl_description = "The projector will influence the locator and projector(camera) maintain the current position"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        camara = bpy.data.objects["Proyector"]
        camara.select = True # la selecciono
        bpy.context.scene.objects.active = camara
        locator = bpy.data.objects["Locator"]
        try:
            coordenada = bpy.data.objects['Proyector'].matrix_world.translation
            coordenadas = [coordenada.x,coordenada.y,coordenada.z]
            bpy.context.object.constraints["ChildOf"].influence = 1
            bpy.data.objects['Proyector'].matrix_world.translation = coordenadas
            bpy.ops.constraint.childof_set_inverse(constraint="ChildOf", owner='OBJECT')
            influencia = bpy.context.object.constraints["ChildOf"].influence #<- truco para q refreske
            bpy.context.object.constraints["ChildOf"].influence = influencia+1 #<- truco para q refreske
            bpy.context.object.constraints["ChildOf"].influence = influencia #<- truco para q refreske
            #bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
            locator.select = True # la selecciono
            bpy.context.scene.objects.active = locator
        except:
            pass
        return{'FINISHED'}
        
class NoInfluencek(bpy.types.Operator):
    bl_idname = "noinfluencek.noinfluencek"
    bl_label = "Without influence Keep position"
    bl_description = "The projector will not influence the locator and projector(camera) maintain the current position"
    
    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        camara = bpy.data.objects["Proyector"]
        camara.select = True # la selecciono
        bpy.context.scene.objects.active = camara
        locator = bpy.data.objects["Locator"]
        try:
            coordenada = bpy.data.objects['Proyector'].matrix_world.translation
            coordenadas = [coordenada.x,coordenada.y,coordenada.z]
            bpy.context.object.constraints["ChildOf"].influence = 0
            bpy.data.objects['Proyector'].matrix_world.translation = coordenadas
            #bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
            locator.select = True # la selecciono
            bpy.context.scene.objects.active = locator
        except:
            pass
        return{'FINISHED'}
    
class Inverse(bpy.types.Operator):
    bl_idname = "setinverse.setinverse"
    bl_label = "Set inverse"
    bl_description = "Inverse influence from locator"

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        camara = bpy.data.objects["Proyector"]
        camara.select = True # la selecciono
        bpy.context.scene.objects.active = camara
        try:
            bpy.ops.constraint.childof_set_inverse(constraint="ChildOf", owner='OBJECT')
            influencia = bpy.context.object.constraints["ChildOf"].influence #<- truco para q refreske
            bpy.context.object.constraints["ChildOf"].influence = influencia+1 #<- truco para q refreske
            bpy.context.object.constraints["ChildOf"].influence = influencia #<- truco para q refreske
            #bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        except:
            pass
        return{'FINISHED'}
        
class ClearInverse(bpy.types.Operator):
    bl_idname = "clearinverse.clearinverse"
    bl_label = "Clear inverse"
    bl_description = "Dont Inverse influence from locator"
    
    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        camara = bpy.data.objects["Proyector"]
        camara.select = True # la selecciono
        bpy.context.scene.objects.active = camara
        try:
            bpy.ops.constraint.childof_clear_inverse(constraint="ChildOf", owner='OBJECT')
            influencia = bpy.context.object.constraints["ChildOf"].influence #<- truco para q refreske
            bpy.context.object.constraints["ChildOf"].influence = influencia+1 #<- truco para q refreske
            bpy.context.object.constraints["ChildOf"].influence = influencia #<- truco para q refreske
            #bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
        except:
            pass
        return{'FINISHED'}
    
        
class AccionToselected(bpy.types.Operator):
    bl_idname = "toselected.toselected"
    bl_label = "To Selected"
    bl_description = "Apply projections to selected objects"
    
    def execute(self, context):
        # capturo el objeto en cuestion:
        ob = bpy.context.selected_objects
        # acciones:
        p.proyectorcillo(ob)

        if ob:
            img = imagen()
            v.vision()
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

                    # le seteamos las coordenadas de tipo de mapeo:
                    tc.uvgenerated(sobject) # este setea en las coordenadas de textura que use uv
                    # actualizamos las relaciones:
                    up.update(ob)

        
        return{'FINISHED'}
        
class Accion_ToALL(bpy.types.Operator):
    bl_idname = "mod.mod"
    bl_label = "Apply/Update Modifier"
    bl_description = "Apply projections to all objects"

    def execute(self, context):

        img = imagen()
        v.vision()
        for ob in bpy.data.objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                p.proyectorcillo(ob)         
                
                # hago las acciones:
                u.unwraping(ob)
                # uvmod requiere de la imagen se la paso por argumentos:
                um.uvmod(ob,img)
                m.trymat(ob,img)

                # le seteamos las coordenadas de tipo de mapeo:
                tc.uvgenerated(ob)
                # actualizamos las relaciones:
                up.update(ob)
    
        return{'FINISHED'}
    
class RELATIONS(bpy.types.Operator):
    bl_idname = "uprel.uprel"
    bl_label = "Update Relationship Material Modifier - Material Renderable"
    bl_description = "Only Update Relationship Material Modifier - Material Renderable"
    
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
