# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TagGroup'
        db.create_table('tagman_taggroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('system', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('tagman', ['TagGroup'])

        # Adding model 'Tag'
        db.create_table('tagman_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagman.TagGroup'], null=True, blank=True)),
        ))
        db.send_create_signal('tagman', ['Tag'])

        # Adding unique constraint on 'Tag', fields ['id', 'group']
        db.create_unique('tagman_tag', ['id', 'group_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['id', 'group']
        db.delete_unique('tagman_tag', ['id', 'group_id'])

        # Deleting model 'TagGroup'
        db.delete_table('tagman_taggroup')

        # Deleting model 'Tag'
        db.delete_table('tagman_tag')


    models = {
        'tagman.tag': {
            'Meta': {'unique_together': "(('id', 'group'),)", 'object_name': 'Tag'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagman.TagGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'tagman.taggroup': {
            'Meta': {'object_name': 'TagGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'system': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['tagman']
