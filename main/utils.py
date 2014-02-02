from models import Opcion

def get_opcion(clave):
  return Opcion.objects.get(clave = clave).valor

def set_opcion(clave, valor):
  opcion = Opcion.objects.get(clave = clave)
  opcion.valor = valor
  opcion.save()
