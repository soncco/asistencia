from django.contrib import admin
from models import Curso, Horario, Alumno, Personal, Opcion

class CursoAdmin(admin.ModelAdmin):
  list_display = ('nombre', 'hora_inicio', 'hora_fin', 'fecha_inicio', 'fecha_fin', 'activo',)
  list_filter = ('activo',)
  search_fields = ['nombre']

class AlumnoAdmin(admin.ModelAdmin):
  list_display = ('nombres', 'apellidos', 'email', 'DNI', 'activo',)
  list_filter = ('nombres', 'apellidos', 'activo',)
  search_fields = ['nombres', 'apellidos', 'dni']

class PersonalAdmin(admin.ModelAdmin):
  list_display = ('nombres', 'apellidos', 'email', 'DNI', 'activo')
  list_filter = ('nombres', 'apellidos', 'activo')
  search_fields = ['nombres', 'apellidos', 'dni']
  filter_vertical = ('horario',)

class HorarioAdmin(admin.ModelAdmin):
  list_display = ('hora', 'tipo',)
  list_filter = ('tipo',)

class OpcionAdmin(admin.ModelAdmin):
  list_display = ('clave', 'valor',)

admin.site.register(Curso, CursoAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Personal, PersonalAdmin)
admin.site.register(Opcion, OpcionAdmin)
