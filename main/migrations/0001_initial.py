# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Curso'
        db.create_table(u'main_curso', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('hora_inicio', self.gf('django.db.models.fields.TimeField')()),
            ('hora_fin', self.gf('django.db.models.fields.TimeField')()),
            ('fecha_inicio', self.gf('django.db.models.fields.DateField')()),
            ('fecha_fin', self.gf('django.db.models.fields.DateField')()),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'main', ['Curso'])

        # Adding model 'Horario'
        db.create_table(u'main_horario', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hora', self.gf('django.db.models.fields.TimeField')()),
            ('tipo', self.gf('django.db.models.fields.CharField')(default='E', max_length=1)),
        ))
        db.send_create_signal(u'main', ['Horario'])

        # Adding model 'Personal'
        db.create_table(u'main_personal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombres', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('DNI', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('foto', self.gf('django.db.models.fields.files.FileField')(default='default.jpg', max_length=100)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'main', ['Personal'])

        # Adding M2M table for field horario on 'Personal'
        m2m_table_name = db.shorten_name(u'main_personal_horario')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('personal', models.ForeignKey(orm[u'main.personal'], null=False)),
            ('horario', models.ForeignKey(orm[u'main.horario'], null=False))
        ))
        db.create_unique(m2m_table_name, ['personal_id', 'horario_id'])

        # Adding model 'Alumno'
        db.create_table(u'main_alumno', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nombres', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('apellidos', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('DNI', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('foto', self.gf('django.db.models.fields.files.FileField')(default='default.jpg', max_length=100)),
            ('activo', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'main', ['Alumno'])

        # Adding M2M table for field curso on 'Alumno'
        m2m_table_name = db.shorten_name(u'main_alumno_curso')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('alumno', models.ForeignKey(orm[u'main.alumno'], null=False)),
            ('curso', models.ForeignKey(orm[u'main.curso'], null=False))
        ))
        db.create_unique(m2m_table_name, ['alumno_id', 'curso_id'])

        # Adding model 'RegistroPersonal'
        db.create_table(u'main_registropersonal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('personal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Personal'])),
            ('marca', self.gf('django.db.models.fields.DateTimeField')()),
            ('tipo', self.gf('django.db.models.fields.CharField')(default='E', max_length=1)),
        ))
        db.send_create_signal(u'main', ['RegistroPersonal'])

        # Adding model 'RegistroAlumno'
        db.create_table(u'main_registroalumno', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alumno', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Alumno'])),
            ('marca', self.gf('django.db.models.fields.DateTimeField')()),
            ('tipo', self.gf('django.db.models.fields.CharField')(default='E', max_length=1)),
        ))
        db.send_create_signal(u'main', ['RegistroAlumno'])

        # Adding model 'Opciones'
        db.create_table(u'main_opciones', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('opcion', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('valor', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'main', ['Opciones'])


    def backwards(self, orm):
        # Deleting model 'Curso'
        db.delete_table(u'main_curso')

        # Deleting model 'Horario'
        db.delete_table(u'main_horario')

        # Deleting model 'Personal'
        db.delete_table(u'main_personal')

        # Removing M2M table for field horario on 'Personal'
        db.delete_table(db.shorten_name(u'main_personal_horario'))

        # Deleting model 'Alumno'
        db.delete_table(u'main_alumno')

        # Removing M2M table for field curso on 'Alumno'
        db.delete_table(db.shorten_name(u'main_alumno_curso'))

        # Deleting model 'RegistroPersonal'
        db.delete_table(u'main_registropersonal')

        # Deleting model 'RegistroAlumno'
        db.delete_table(u'main_registroalumno')

        # Deleting model 'Opciones'
        db.delete_table(u'main_opciones')


    models = {
        u'main.alumno': {
            'DNI': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'Meta': {'object_name': 'Alumno'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'curso': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Curso']", 'symmetrical': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'foto': ('django.db.models.fields.files.FileField', [], {'default': "'default.jpg'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombres': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.curso': {
            'Meta': {'object_name': 'Curso'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fecha_fin': ('django.db.models.fields.DateField', [], {}),
            'fecha_inicio': ('django.db.models.fields.DateField', [], {}),
            'hora_fin': ('django.db.models.fields.TimeField', [], {}),
            'hora_inicio': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.horario': {
            'Meta': {'object_name': 'Horario'},
            'hora': ('django.db.models.fields.TimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'})
        },
        u'main.opciones': {
            'Meta': {'object_name': 'Opciones'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opcion': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'valor': ('django.db.models.fields.TextField', [], {})
        },
        u'main.personal': {
            'DNI': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'Meta': {'object_name': 'Personal'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'apellidos': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'foto': ('django.db.models.fields.files.FileField', [], {'default': "'default.jpg'", 'max_length': '100'}),
            'horario': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['main.Horario']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombres': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.registroalumno': {
            'Meta': {'object_name': 'RegistroAlumno'},
            'alumno': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Alumno']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.DateTimeField', [], {}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'})
        },
        u'main.registropersonal': {
            'Meta': {'object_name': 'RegistroPersonal'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.DateTimeField', [], {}),
            'personal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Personal']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'})
        }
    }

    complete_apps = ['main']