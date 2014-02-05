# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django_xhtml2pdf.utils import generate_pdf

from models import Alumno, Personal, Horario, Curso, RegistroPersonal, RegistroAlumno
import json, datetime
from utils import *

def the_login(request):
  if(request.user.is_authenticated()):
    return HttpResponseRedirect(reverse('index'))
  else:
    if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']

      user = authenticate(username = username, password = password)
      if user is not None:
        if user.is_active:
          login(request, user)
          return HttpResponseRedirect(reverse('index'))
        else:
          messages.error(request, 'El usuario no está activo. Contacte con el administrador.')
      else:
        messages.error(request, 'Revise el usuario o la contraseña.')

    usuarios = User.objects.filter(is_active = True)
    context = {'usuarios': usuarios}
  
  return render_to_response('login.html', context, context_instance = RequestContext(request))

@login_required
def index(request):
  return render_to_response('index.html', context_instance = RequestContext(request))


def the_logout(request):
  messages.success(request, 'Hasta pronto')
  logout(request)

  return HttpResponseRedirect(reverse('index'))

@login_required
def asistencia_alumno(request):
  if request.method == 'POST':
    dni = request.POST.get('dni')
    curso = request.POST.get('curso')
    alumno = get_object_or_404(Alumno, DNI = dni, activo = True)
    try:
      elcurso = alumno.curso.get(pk = curso)
    except:
      raise Http404

    registro = RegistroAlumno

    ahora = timezone.now()
    try:
      ultimo_registro = RegistroAlumno.objects.filter(alumno = alumno, curso = elcurso).order_by('-marca')[0]
      diferencia = ahora - ultimo_registro.marca
      seconds = diferencia.seconds
    except:
      ultimo_registro = ahora
      seconds = int(get_opcion('tiempo_entre_marcas')) * 60

    if seconds >= int(get_opcion('tiempo_entre_marcas')) * 60:
      registro = RegistroAlumno(alumno = alumno, curso = elcurso, marca = ahora, tolerancia = int(get_opcion('tolerancia')))
      registro.save()

      context = {
        'nombres': alumno.nombres,
        'foto': str(alumno.foto)
      }
      return HttpResponse(json.dumps(context), mimetype = "application/json")
    else:
      raise PermissionDenied
  
  cursos = Curso.objects.filter(activo = True)
  context = {'cursos': cursos, 'tiempo_entre_marcas': get_opcion('tiempo_entre_marcas')}
  return render_to_response('asistencia-alumno.html', context, context_instance = RequestContext(request))

@login_required
def asistencia_personal(request):
  if request.method == 'POST':
    dni = request.POST.get('dni')
    personal = get_object_or_404(Personal, DNI = dni, activo = True)

    ahora = timezone.now()
    try:
      ultimo_registro = RegistroPersonal.objects.filter(personal = personal).order_by('-marca')[0]
      diferencia = ahora - ultimo_registro.marca
      seconds = diferencia.seconds
    except:
      ultimo_registro = ahora
      seconds = int(get_opcion('tiempo_entre_marcas')) * 60

    if seconds >= int(get_opcion('tiempo_entre_marcas')) * 60:
      registro = RegistroPersonal(personal = personal, marca = ahora, tolerancia = int(get_opcion('tolerancia')))
      registro.save()

      context = {
        'nombres': personal.nombres,
        'foto': str(personal.foto)
      }
      return HttpResponse(json.dumps(context), mimetype = "application/json")
    else:
      raise PermissionDenied

  context = {'tiempo_entre_marcas': get_opcion('tiempo_entre_marcas')}

  return render_to_response('asistencia-personal.html', context, context_instance = RequestContext(request))

@login_required
def opciones(request):
  if request.method == 'POST':
    tiempo_entre_marcas = request.POST.get('tiempo_entre_marcas')
    tolerancia = request.POST.get('tolerancia')
    set_opcion('tiempo_entre_marcas', tiempo_entre_marcas)
    set_opcion('tolerancia', tolerancia)

    messages.success(request, 'Se guardaron las opciones correctamente.')

  if request.method == 'GET':
    messages.warning(request, 'Ten mucho cuidado al manejar estas opciones, todo el sistema depende de estos datos.')

  context = {
    'tolerancia': get_opcion('tolerancia'),
    'tiempo_entre_marcas': get_opcion('tiempo_entre_marcas')
  }
  return render_to_response('opciones.html', context, context_instance = RequestContext(request))

@login_required
def reporte_curso(request):
  if request.method == 'POST':
    curso = request.POST.get('curso')
    fecha = request.POST.get('fecha')

    alumnos = get_alumnos_curso(curso)
    results = []

    for alumno in alumnos:
      registros = get_registros_alumno(alumno, curso, fecha)
      results.append({
        'DNI': alumno.DNI,
        'nombres': alumno.nombres,
        'apellidos': alumno.apellidos,
        'registros': registros
      })

    return HttpResponse('{"alumnos": ' + json.dumps(results) + '}', mimetype = "application/json")

  cursos = Curso.objects.filter(activo = True)
  context = {'cursos': cursos}
  return render_to_response('reporte-curso.html', context, context_instance = RequestContext(request))

@login_required
def reporte_personal(request):
  if request.method == 'POST':
    fecha = request.POST.get('fecha')

    personal = Personal.objects.filter(activo = True)
    results = []

    for persona in personal:
      registros = get_registros_personal(persona, fecha)
      horarios = get_horarios_personal(persona)
      results.append({
        'DNI': persona.DNI,
        'nombres': persona.nombres,
        'apellidos': persona.apellidos,
        'horarios': horarios,
        'registros': registros
      })

    return HttpResponse('{"personal": ' + json.dumps(results) + '}', mimetype = "application/json")

  return render_to_response('reporte-personal.html', context_instance = RequestContext(request))

@login_required
def reporte_porcentaje(request):
  if request.method == 'POST':
    curso = request.POST.get('curso')

    alumnos = get_alumnos_curso(curso)

    results = []

    for alumno in alumnos:
      porcentaje = get_porcentaje_alumno(alumno, curso)
      results.append({
        'DNI': alumno.DNI,
        'nombres': alumno.nombres,
        'apellidos': alumno.apellidos,
        'porcentaje': '%.2f' % porcentaje
      })

    response = '{"alumnos": ' + json.dumps(results) + '}'
    return HttpResponse(response, mimetype = "application/json")

  cursos = Curso.objects.filter(activo = True)
  context = {'cursos': cursos}
  return render_to_response('reporte-porcentaje.html', context, context_instance = RequestContext(request))

@login_required
def reporte_curso_total(request):
  if request.method == 'POST':
    curso = request.POST.get('curso')
    alumnos = get_alumnos_curso(curso)

    results = []

    for alumno in alumnos:
      asistencias = get_asistencias_alumno(alumno, curso)
      results.append({
        'DNI': alumno.DNI,
        'nombres': alumno.nombres,
        'apellidos': alumno.apellidos,
        'asistencias': asistencias
      })

    fechas = get_fechas_curso(curso, 'str')

    response = '{"alumnos": ' + json.dumps(results) + ', "fechas": ' + json.dumps(fechas) + '}'
    return HttpResponse(response, mimetype = "application/json")

  cursos = Curso.objects.filter(activo = True)
  context = {'cursos': cursos}
  return render_to_response('reporte-curso-total.html', context, context_instance = RequestContext(request))

@login_required
def reporte_curso_print(request):
  
  curso = request.GET.get('curso')
  fecha = request.GET.get('fecha')

  alumnos = get_alumnos_curso(curso)
  results = []

  for alumno in alumnos:
    registros = get_registros_alumno(alumno, curso, fecha)
    results.append({
      'DNI': alumno.DNI,
      'nombres': alumno.nombres,
      'apellidos': alumno.apellidos,
      'registros': registros
    })

  curso = Curso.objects.get(pk = curso)

  resp = HttpResponse(content_type = 'application/pdf')
  context = {'results': results, 'curso': curso, 'fecha': datetime.datetime.strptime(fecha, '%Y-%m-%d')}
  return generate_pdf('reporte-curso-print.html', file_object = resp, context = context)

@login_required
def reporte_personal_print(request):
  fecha = request.GET.get('fecha')

  personal = Personal.objects.filter(activo = True)
  results = []

  for persona in personal:
    registros = get_registros_personal(persona, fecha)
    horarios = get_horarios_personal(persona)
    results.append({
      'DNI': persona.DNI,
      'nombres': persona.nombres,
      'apellidos': persona.apellidos,
      'horarios': horarios,
      'registros': registros
    })

  resp = HttpResponse(content_type = 'application/pdf')
  context = {'results': results, 'fecha': datetime.datetime.strptime(fecha, '%Y-%m-%d')}
  return generate_pdf('reporte-personal-print.html', file_object = resp, context = context)

@login_required
def reporte_porcentaje_print(request):
  curso = request.GET.get('curso')

  alumnos = get_alumnos_curso(curso)

  results = []

  for alumno in alumnos:
    porcentaje = get_porcentaje_alumno(alumno, curso)
    results.append({
      'DNI': alumno.DNI,
      'nombres': alumno.nombres,
      'apellidos': alumno.apellidos,
      'porcentaje': '%.2f' % porcentaje
    })

  curso = Curso.objects.get(pk = curso)

  resp = HttpResponse(content_type = 'application/pdf')
  context = {'results': results, 'curso': curso}
  return generate_pdf('reporte-porcentaje-print.html', file_object = resp, context = context)

@login_required
def reporte_curso_total_print(request):
  
  curso = request.GET.get('curso')
  alumnos = get_alumnos_curso(curso)

  results = []

  for alumno in alumnos:
    asistencias = get_asistencias_alumno(alumno, curso)
    results.append({
      'DNI': alumno.DNI,
      'nombres': alumno.nombres,
      'apellidos': alumno.apellidos,
      'asistencias': asistencias
    })

  fechas = get_fechas_curso(curso, 'str')

  curso = Curso.objects.get(pk = curso)

  resp = HttpResponse(content_type = 'application/pdf')
  context = {'results': results, 'curso': curso, 'fechas': fechas}
  return generate_pdf('reporte-curso-total-print.html', file_object = resp, context = context)
