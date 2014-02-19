# -*- coding: utf-8 -*-

from django.db import models

TIPOS = (
  ('E', 'Entrada'),
  ('S', 'Salida'),
)

class Categoria(models.Model):
  nombre = models.CharField(max_length = 255)
  descripcion = models.TextField(blank = True)

  def __unicode__(self):
    return self.nombre

class Curso(models.Model):
  nombre = models.CharField(max_length = 255)
  hora_inicio = models.TimeField()
  hora_fin = models.TimeField()
  fecha_inicio = models.DateField()
  fecha_fin = models.DateField()
  activo = models.BooleanField(default = True)
  categoria = models.ForeignKey(Categoria, blank = True, null = True)

  def __unicode__(self):
    return self.nombre

class Horario(models.Model):
  hora = models.TimeField(help_text = "Ingresar con el formato HH:MM")
  tipo = models.CharField(max_length = 1, choices = TIPOS, default = 'E')

  def __unicode__(self):
    return "%s: %s" % (self.tipo, self.hora)

class Personal(models.Model):
  nombres = models.CharField(max_length = 255)
  apellidos = models.CharField(max_length = 255)
  email = models.EmailField()
  dni = models.CharField(name = 'DNI', max_length = 8)
  horario = models.ManyToManyField(Horario)
  foto = models.FileField(upload_to = 'fotos', default = 'default.jpg')
  activo = models.BooleanField(default = True)

  class Meta:
    verbose_name = ('Personal')
    verbose_name_plural = ('Personal')

  def __unicode__(self):
    return "%s %s" % (self.nombres, self.apellidos)

class Alumno(models.Model):
  nombres = models.CharField(max_length = 255)
  apellidos = models.CharField(max_length = 255)
  email = models.EmailField()
  dni = models.CharField(name = 'DNI', max_length = 8)
  curso = models.ManyToManyField(Curso)
  foto = models.FileField(upload_to = 'fotos', default = 'default.jpg')
  activo = models.BooleanField(default = True)

  def __unicode__(self):
    return "%s %s" % (self.nombres, self.apellidos)

class RegistroPersonal(models.Model):
  personal = models.ForeignKey(Personal)
  marca = models.DateTimeField()
  tolerancia = models.IntegerField()

class RegistroAlumno(models.Model):
  alumno = models.ForeignKey(Alumno)
  marca = models.DateTimeField()
  curso = models.ForeignKey(Curso)
  tolerancia = models.IntegerField()

class Opcion(models.Model):

  class Meta:
    verbose_name = ('Opción')
    verbose_name_plural = ('Opciones')

  clave = models.CharField(max_length = 20)
  valor = models.TextField()