from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q
from django.utils.translation import gettext as _
from models import Curso, Horario, Alumno, Personal, Opcion

class CursoAdmin(admin.ModelAdmin):
  list_display = ('nombre', 'hora_inicio', 'hora_fin', 'fecha_inicio', 'fecha_fin', 'activo',)
  list_filter = ('activo',)
  search_fields = ['nombre']

class AlumnoAdmin(admin.ModelAdmin):
  list_display = ('nombres', 'apellidos', 'email', 'DNI', 'activo',)
  list_filter = ('nombres', 'apellidos', 'activo',)
  search_fields = ['nombres', 'apellidos', 'DNI']
  filter_vertical = ('curso',)

class PersonalAdmin(admin.ModelAdmin):
  list_display = ('nombres', 'apellidos', 'email', 'DNI', 'activo')
  list_filter = ('nombres', 'apellidos', 'activo')
  search_fields = ['nombres', 'apellidos', 'DNI']
  filter_vertical = ('horario',)

class HorarioAdmin(admin.ModelAdmin):
  list_display = ('hora', 'tipo',)
  list_filter = ('tipo',)

class OpcionAdmin(admin.ModelAdmin):
  list_display = ('clave', 'valor',)

class MyUserAdmin(UserAdmin):
  list_display = ('username',)
  list_filter = ()

  fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Staff'), {'fields': ('is_staff',)}),
        (_('Groups'), {'fields': ('groups',)}),
    )

  def queryset(self, request):
    qs = super(MyUserAdmin, self).queryset(request)
    qs = qs.filter(~Q(username = 'brau'))
    return qs

admin.site.register(Curso, CursoAdmin)
admin.site.register(Horario, HorarioAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Personal, PersonalAdmin)
admin.site.register(Opcion, OpcionAdmin)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)