# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['group', 'id']
        db.delete_unique('tagman_tag', ['group_id', 'id'])

        # Adding field 'Tag.archived'
        db.add_column('tagman_tag', 'archived',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'Tag.group'
        db.alter_column('tagman_tag', 'group_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['tagman.TagGroup']))
        # Adding unique constraint on 'Tag', fields ['group', 'name']
        db.create_unique('tagman_tag', ['group_id', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['group', 'name']
        db.delete_unique('tagman_tag', ['group_id', 'name'])

        # Deleting field 'Tag.archived'
        db.delete_column('tagman_tag', 'archived')


        # Changing field 'Tag.group'
        db.alter_column('tagman_tag', 'group_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagman.TagGroup'], null=True))
        # Adding unique constraint on 'Tag', fields ['group', 'id']
        db.create_unique('tagman_tag', ['group_id', 'id'])


    models = {
        'tagman.tag': {
            'Meta': {'unique_together': "(('name', 'group'),)", 'object_name': 'Tag'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagman.TagGroup']"}),
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