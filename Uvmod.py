import bpy

# Aplicando Modificador al objeto

class Uvmod(object):

    def __init__(self, ob = None, img = None):
        self.ob = None
        self.img = None
    
    def uvmod(self,ob,img):
        try:
            
            #img = imagen()
            # img viene por parametros
            
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