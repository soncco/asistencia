from models import Alumno, RegistroAlumno, RegistroPersonal, Opcion
import datetime

def get_opcion(clave):
  return Opcion.objects.get(clave = clave).valor

def set_opcion(clave, valor):
  opcion = Opcion.objects.get(clave = clave)
  opcion.valor = valor
  opcion.save()

def get_alumnos_curso(curso):
  return Alumno.objects.filter(curso__pk = curso).order_by('apellidos')

def get_registros_alumno(alumno, curso, fecha):
  fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')

  results = []

  registros = RegistroAlumno.objects.filter(
    alumno = alumno,
    curso = curso,
    marca__year = fecha.year,
    marca__month = fecha.month,
    marca__day = fecha.day
  )

  for registro in registros:
    results.append({
      'hora': '%02d' % (registro.marca.hour-5),
      'minuto': '%02d' % registro.marca.minute
    })

  return results

def get_registros_personal(personal, fecha):
  fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')

  results = []

  registros = RegistroPersonal.objects.filter(
    personal = personal,
    marca__year = fecha.year,
    marca__month = fecha.month,
    marca__day = fecha.day
  )

  for registro in registros:
    results.append({
      'hora': '%02d' % (registro.marca.hour-5),
      'minuto': '%02d' % registro.marca.minute
    })

  return results

def get_horarios_personal(personal):
  horarios = personal.horario.all()

  print(dir(personal))

  results = []
  for horario in horarios:
    results.append({
      'marca': "%s, %s" % (horario.tipo, horario.hora)
    })

  return results