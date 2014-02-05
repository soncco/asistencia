from django.conf.urls import patterns,url

urlpatterns = patterns('main.views',
  url(r'^$', 'index', name = 'index'),
  
  url(r'^login/$', 'the_login', name = 'the_login'),
  url(r'^logout/$', 'the_logout', name = 'the_logout'),

  url(r'^asistencia/alumno/$', 'asistencia_alumno', name = 'asistencia_alumno'),
  url(r'^asistencia/personal/$', 'asistencia_personal', name = 'asistencia_personal'),
  url(r'^opciones/$', 'opciones', name = 'opciones'),

  url(r'^reporte/curso/$', 'reporte_curso', name = 'reporte_curso'),
  url(r'^reporte/curso/porcentaje/$', 'reporte_porcentaje', name = 'reporte_porcentaje'),
  url(r'^reporte/curso/total/$', 'reporte_curso_total', name = 'reporte_curso_total'),
  url(r'^reporte/curso/print/$', 'reporte_curso_print', name = 'reporte_curso_print'),
  url(r'^reporte/curso/porcentaje/print/$', 'reporte_porcentaje_print', name = 'reporte_porcentaje_print'),
  url(r'^reporte/curso/total/print/$', 'reporte_curso_total_print', name = 'reporte_curso_total_print'),

  url(r'^reporte/personal/$', 'reporte_personal', name = 'reporte_personal'),
  url(r'^reporte/personal/print/$', 'reporte_personal_print', name = 'reporte_personal_print'),
)