
from django.db import models

from tagman.models import TaggedItem

class TestItem(TaggedItem):

    name = models.CharField(max_length=100, default="test")

    class Meta:
        app_label = "tagman"

    def __unicode__(self):
        return str(self.name)
