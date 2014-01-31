from models import Opcion

def get_opcion(clave):
  return Opciones.objects.get(clave = clave).values('valor')