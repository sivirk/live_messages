# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Station'
        db.create_table(u'stations_station', (
            (u'tag_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registers.Tag'], unique=True, primary_key=True)),
            ('type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('subscribers', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('vendor', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'stations', ['Station'])

        # Adding model 'Route'
        db.create_table(u'stations_route', (
            (u'tag_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registers.Tag'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stations.Station'])),
            ('signaling', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('channels', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'stations', ['Route'])

        # Adding model 'Subscriber'
        db.create_table(u'stations_subscriber', (
            (u'tag_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registers.Tag'], unique=True, primary_key=True)),
            ('number', self.gf('django.db.models.fields.BigIntegerField')()),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stations.Station'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'stations', ['Subscriber'])

        # Adding model 'Equipment'
        db.create_table(u'stations_equipment', (
            (u'tag_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registers.Tag'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stations.Station'])),
            ('subscribers', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'stations', ['Equipment'])


    def backwards(self, orm):
        # Deleting model 'Station'
        db.delete_table(u'stations_station')

        # Deleting model 'Route'
        db.delete_table(u'stations_route')

        # Deleting model 'Subscriber'
        db.delete_table(u'stations_subscriber')

        # Deleting model 'Equipment'
        db.delete_table(u'stations_equipment')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'registers.tag': {
            'Meta': {'object_name': 'Tag'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'stations.equipment': {
            'Meta': {'object_name': 'Equipment', '_ormbases': [u'registers.Tag']},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stations.Station']"}),
            'subscribers': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'tag_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['registers.Tag']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'stations.route': {
            'Meta': {'object_name': 'Route', '_ormbases': [u'registers.Tag']},
            'channels': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'signaling': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stations.Station']"}),
            u'tag_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['registers.Tag']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'stations.station': {
            'Meta': {'object_name': 'Station', '_ormbases': [u'registers.Tag']},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subscribers': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'tag_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['registers.Tag']", 'unique': 'True', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'vendor': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'stations.subscriber': {
            'Meta': {'object_name': 'Subscriber', '_ormbases': [u'registers.Tag']},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number': ('django.db.models.fields.BigIntegerField', [], {}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stations.Station']"}),
            u'tag_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['registers.Tag']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['stations']