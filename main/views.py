# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from models import Alumno, Personal, Horario, Curso, RegistroPersonal, RegistroAlumno
from utils import get_opcion
import json, datetime

def index(request):
  return render_to_response('index.html', context_instance = RequestContext(request))

def asistencia_alumno(request):
  return render_to_response('asistencia-alumno.html', context_instance = RequestContext(request))

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
      seconds = 600

    if seconds >= 600:
      registro = RegistroPersonal(personal = personal, marca = ahora)
      registro.save()

      context = {
        'nombres': personal.nombres,
        'foto': str(personal.foto)
      }
      return HttpResponse(json.dumps(context), mimetype = "application/json")
    else:
      raise PermissionDenied

  return render_to_response('asistencia-personal.html', context_instance = RequestContext(request))
