from django.contrib import admin
from tagman.models import TagGroup
from tagman.models import Tag

class TagGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "system"]
    search_fields = ["name",]
    list_filter = ["system",]
    prepopulated_fields = {"slug": ("name",),}

class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "group", "system"]
    search_fields = ["name",]
    list_filter = ["group",]
    prepopulated_fields = {"slug": ("name",),}

    def system(self, _object):
        return _object.system
    system.short_description = u'System'
    system.boolean = True

    def queryset(self, request):
        # use our manager, rather than the default one
        qs = self.model.all_objects.get_query_set()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

try:
    admin.site.register(Tag, TagAdmin)
    admin.site.register(TagGroup, TagGroupAdmin)
except admin.sites.AlreadyRegistered:
    pass
    
