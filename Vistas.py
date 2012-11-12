import bpy

class Vistas(object):

    def __init__(self, nada = None):
        self.nada = None

    def vision(self):
            # Poniendo todos los viewports comunes en modo textured en la 263:
            #bpy.context.blend_data.screens[0].areas[4].spaces[0].viewport_shade = 'TEXTURED' # vista animation a textured
            #bpy.context.blend_data.screens[2].areas[4].spaces[0].viewport_shade = 'TEXTURED' # vista default a textured
            #bpy.context.blend_data.screens[4].areas[2].spaces[0].viewport_shade = 'TEXTURED' # vista scripting a textured
            
            # en la 264a:
            # 0 0 npi
            # 1 4 animation
            # 2 3 compositing
            # 3 4 default
            # 4 4 game logic

            bpy.data.screens['Default'].areas[4].spaces[0].viewport_shade = 'TEXTURED'
            bpy.data.screens['Scripting'].areas[2].spaces[0].viewport_shade = 'TEXTURED'
            bpy.data.screens['Animation'].areas[4].spaces[0].viewport_shade = 'TEXTURED'

            #bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todo
            bpy.data.scenes['Scene'].game_settings.material_mode = 'GLSL'
            # ponemos todas las imagenes en premultiply:
            for i in bpy.data.images[:]:
                bpy.data.images[i.name].use_premultiply = True
