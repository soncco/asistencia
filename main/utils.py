from models import Alumno, Curso, RegistroAlumno, RegistroPersonal, Opcion
import datetime

def get_opcion(clave):
  return Opcion.objects.get(clave = clave).valor

def set_opcion(clave, valor):
  opcion = Opcion.objects.get(clave = clave)
  opcion.valor = valor
  opcion.save()

def daterange(start_date, end_date):
  for n in range(int ((end_date - start_date).days + 1)):
    yield start_date + datetime.timedelta(n)

def get_alumnos_curso(curso):
  return Alumno.objects.filter(curso__pk = curso, activo = True).order_by('apellidos')

def get_registros_alumno(alumno, curso, fecha):
  if isinstance(fecha, basestring):
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
      'hora': '%02d' % (registro.marca.hour),
      'minuto': '%02d' % registro.marca.minute
    })

  return results

def get_registros_alumno_object(alumno, curso, fecha):
  if isinstance(fecha, basestring):
    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')

  results = []

  registros = RegistroAlumno.objects.filter(
    alumno = alumno,
    curso = curso,
    marca__year = fecha.year,
    marca__month = fecha.month,
    marca__day = fecha.day
  )

  return registros


def total_dias_curso(curso):
  total = 0
  for fecha in daterange(curso.fecha_inicio, curso.fecha_fin):
    total += 1
  return total

def get_fechas_curso(curso, formato):
  curso = Curso.objects.get(pk = curso)
  fechas = []
  for fecha in daterange(curso.fecha_inicio, curso.fecha_fin):
    if formato == 'obj':
      fechas.append({'fecha': fecha})
    else:
      fechas.append({'fecha': fecha.strftime("%d/%m")})
  return fechas

def get_porcentaje_alumno(alumno, curso):
  curso = Curso.objects.get(pk = curso)
  asistencias = 0
  total = total_dias_curso(curso)
  if total > 0:
    for fecha in daterange(curso.fecha_inicio, curso.fecha_fin):
      registros = get_registros_alumno(alumno, curso, fecha)
      if len(registros) > 1:
        asistencias += 1

    return (float(asistencias)/total) * 100
  else:
    return 0


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
      'hora': '%02d' % (registro.marca.hour),
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

def get_asistencias_alumno(alumno, curso):
  asistencias = []
  fechas = get_fechas_curso(curso, 'obj')

  for fecha in fechas:
    registros = get_registros_alumno(alumno, curso, fecha['fecha'])
    asistencias.append({'registros': registros})

  return asistencias

def difft(start, end):
    a,b,c,d = start.hour, start.minute, start.second, start.microsecond
    w,x,y,z = end.hour, end.minute, end.second, end.microsecond
    delt = (w-a)*60 + (x-b) + (y-c)/60. + (z-d)/60000000
    return delt + 1440 if delt<0 else delt