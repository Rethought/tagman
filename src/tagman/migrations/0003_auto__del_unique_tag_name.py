# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['name']
        db.delete_unique('tagman_tag', ['name'])


    def backwards(self, orm):
        # Adding unique constraint on 'Tag', fields ['name']
        db.create_unique('tagman_tag', ['name'])


    models = {
        'tagman.tag': {
            'Meta': {'unique_together': "(('id', 'group'),)", 'object_name': 'Tag'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagman.TagGroup']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'})
        },
        'tagman.taggroup': {
            'Meta': {'object_name': 'TagGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '100'}),
            'system': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['tagman']