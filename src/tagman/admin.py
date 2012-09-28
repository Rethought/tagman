"""Tagman admin classes and also helpers/mixins for users of Tagman"""
from django.contrib import admin
from tagman.models import TagGroup
from tagman.models import Tag
from django import forms


class TaggedContentItemForm(forms.ModelForm):
    """
    Form for use on model admins that have a 'tags' field in which you want
    a nice filtered list without system tags polluting it. Typical for all
    TaggedContentItem models.
    """
    def __init__(self, *args, **kwargs):
        """
        Find all fields in a page ending in 'tags', assume that they are a
        tags M2M and reset the widget's choices to a filtered list that
        excludes system tags.

        This is very crude and rather inelegant but it solved a particular
        problem. It is suggested this is used with care, or used as an
        example of how to manage filtering if you'd like to do some such
        in another way.
        """
        super(TaggedContentItemForm, self).__init__(*args, **kwargs)
        wtf = Tag.objects.filter(group__system=False)
        wlist = [w for t, w in self.fields.items() if t.endswith("tags")]
        choices = []
        for choice in wtf:
            choices.append((choice.id, str(choice)))
        [setattr(w, 'choices', choices) for w in wlist]


class TaggedContentAdminMixin(object):
    """
    When this is the first in the list of base classes for the admin class
    of a model that has tags it will ensure your 'tags' are filtered.
    """
    form = TaggedContentItemForm


class TagGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "system"]
    search_fields = ["name"]
    list_filter = ["system"]
    prepopulated_fields = {"slug": ("name",)}


class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "group", "system"]
    search_fields = ["name"]
    list_filter = ["group"]
    prepopulated_fields = {"slug": ("name",)}

    def system(self, _object):
        return _object.system
    system.short_description = u'System'
    system.boolean = True

    def queryset(self, request):
        # use our manager, rather than the default one
        qs = self.model.objects.get_query_set()

        # we need this from the superclass method
        # otherwise we might try to *None, which is bad ;)
        ordering = self.ordering or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

try:
    admin.site.register(Tag, TagAdmin)
    admin.site.register(TagGroup, TagGroupAdmin)
except admin.sites.AlreadyRegistered:
    pass
