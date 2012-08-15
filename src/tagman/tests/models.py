from django.db import models

from tagman.models import TaggedItem
from tagman.models import TaggedContentItem


class TestItem(TaggedItem):
    name = models.CharField(max_length=100, default="test")

    class Meta:
        app_label = "tagman"

    def __unicode__(self):
        return str(self.name)


class IgnoreTestItem(TaggedItem):
    name = models.CharField(max_length=100, default="test")

    class Meta:
        app_label = "tagman"

    def __unicode__(self):
        return str(self.name)


class TCI(TaggedContentItem):
    class Meta:
        app_label = "tagman"

    slug = "tci-slug"
