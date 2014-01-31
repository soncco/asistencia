from django.conf.urls import patterns,url

urlpatterns = patterns('main.views',
  url(r'^$', 'index', name = 'index'),
  url(r'^asistencia/alumno/$', 'asistencia_alumno', name = 'asistencia_alumno'),
  url(r'^asistencia/personal/$', 'asistencia_personal', name = 'asistencia_personal'),
)