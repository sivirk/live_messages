# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'registers_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'registers', ['Tag'])

        # Adding model 'Register'
        db.create_table(u'registers_register', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'registers', ['Register'])

        # Adding M2M table for field groups on 'Register'
        m2m_table_name = db.shorten_name(u'registers_register_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('register', models.ForeignKey(orm[u'registers.register'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['register_id', 'group_id'])

        # Adding M2M table for field content_types on 'Register'
        m2m_table_name = db.shorten_name(u'registers_register_content_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('register', models.ForeignKey(orm[u'registers.register'], null=False)),
            ('contenttype', models.ForeignKey(orm[u'contenttypes.contenttype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['register_id', 'contenttype_id'])

        # Adding M2M table for field tags on 'Register'
        m2m_table_name = db.shorten_name(u'registers_register_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('register', models.ForeignKey(orm[u'registers.register'], null=False)),
            ('tag', models.ForeignKey(orm[u'registers.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['register_id', 'tag_id'])

        # Adding model 'Message'
        db.create_table(u'registers_message', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('stamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('purpose', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('register', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registers.Register'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'registers', ['Message'])

        # Adding M2M table for field tags on 'Message'
        m2m_table_name = db.shorten_name(u'registers_message_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('message', models.ForeignKey(orm[u'registers.message'], null=False)),
            ('tag', models.ForeignKey(orm[u'registers.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['message_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'registers_tag')

        # Deleting model 'Register'
        db.delete_table(u'registers_register')

        # Removing M2M table for field groups on 'Register'
        db.delete_table(db.shorten_name(u'registers_register_groups'))

        # Removing M2M table for field content_types on 'Register'
        db.delete_table(db.shorten_name(u'registers_register_content_types'))

        # Removing M2M table for field tags on 'Register'
        db.delete_table(db.shorten_name(u'registers_register_tags'))

        # Deleting model 'Message'
        db.delete_table(u'registers_message')

        # Removing M2M table for field tags on 'Message'
        db.delete_table(db.shorten_name(u'registers_message_tags'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'registers.message': {
            'Meta': {'object_name': 'Message'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.SmallIntegerField', [], {}),
            'register': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registers.Register']"}),
            'stamp': ('django.db.models.fields.DateTimeField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registers.Tag']", 'null': 'True', 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'registers.register': {
            'Meta': {'object_name': 'Register'},
            'content_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'symmetrical': 'False'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'null': 'True', 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registers.Tag']", 'null': 'True', 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'registers.tag': {
            'Meta': {'object_name': 'Tag'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['registers']