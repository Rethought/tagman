from django.db import models
from django.template.defaultfilters import slugify

TAG_SEPARATOR = ":"

class TagGroup(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, default = "")
    system = models.BooleanField(default=False,
                                help_text = "Set True for system groups that should not appear for general use")

    def __unicode__(self):
        prefix = "*" if self.system else ""
        return prefix+self.name

    def tags_for_group(self):
        """ Return the set of tags that are associated with this group """
        return self.tag_set.all()

    def save(self, *args, **kwargs):
        """ assign slug if empty """
        if not self.slug:
            self.slug = slugify(self.name)
        super(TagGroup, self).save(*args, **kwargs)

class TagManager(models.Manager):
    def __init__(self, sys=False):
        """ If sys = True, this will return only system tags. If False, the default, will
return non-system tags only."""        
        super(TagManager, self).__init__()
        self.system_tags = sys

    def get_query_set(self):
        """ By default return only those objects that are not flagged as 'system' tags """
        return super(TagManager, self).get_query_set().exclude(group__system = not self.system_tags)

class Tag(models.Model):
    name = models.CharField(verbose_name='Name', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, default="")
    group = models.ForeignKey(TagGroup, verbose_name='Group', blank=True, null=True)

    objects = TagManager(sys=False)
    sys_objects = TagManager(sys=True)
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        """ assign slug if empty """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("id", "group",)

    def __unicode__(self):
        return "%s%s" % (str(self.group) + TAG_SEPARATOR if self.group else "", self.name)

    @property
    def system(self):
        return self.group.system

    def models_for_tag(self):
        """ Return the unique set of model names, all of which have had
        instances tagged with this tag.
        @todo: This is hacky. Can we do it more elegantly?
        """
        return [s[:-4] for s in dir(self) if s[-4:]=='_set']

    def tagged_model_items(self, model_cls=None, model_name=""):
        """ Return list of instances of a given model, the class for which
        is passed into model_cls OR the name for which is passed in model_name, 
        that are tagged with this tag"""
        if model_cls:
            cls_name = model_cls.__name__.lower()
        else:
            cls_name = model_name.lower()

        try:
            _set = getattr(self, "%s_set" % cls_name)
        except AttributeError:
            return []
        return _set.all()

    def tagged_items(self):
        """ Return a dictionary, keyed on model name, with each value the 
        list of items of that model tagged with this tag. """
        models = self.models_for_tag()
        rdict = {}
        for model in models:
            rdict[model] = self.tagged_model_items(model_name = model)
        return rdict

    @classmethod
    def tag_for_string(cls, s):
        """ Given a tag representation as "[*]GRP:NAME", return 
        the tag instance. 
        @todo: handle the [TagGroup|Tag].DoesNotExist exceptions
        """
        s = s.replace('*','') # representation of system group prefixed *
        groupname, tagname = s.split(TAG_SEPARATOR)
        grp = TagGroup.objects.get(name = groupname)
        tag = Tag.all_objects.get(name = tagname, group = grp)
        return tag

    @classmethod
    def tags_for_string(cls, s):
        """ Given a comma delimited list of tag string representations, e.g.::

        <GRP>:<NAME>,<GRP>:<NAME2>...

        return the list of tag instances that these represent.
        @todo: handle case where no tag instance returned
        """
        tokens = s.strip().split(',')
        _tags = [Tag.tag_for_string(t) for t in tokens]
        if not _tags:
            return None
        return _tags

class TaggedItem(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        abstract = True

    def add_tag_str(self, string):
        group_name, tag_name = string.strip().split(TAG_SEPARATOR)
        tag = Tag.all_objects.get_or_create(name=tag_name)[0]
        group = TagGroup.objects.get_or_create(name=group_name)[0]
        if tag and group:
            tag.save()
            group.save()
            self.tags.add(tag)
            group.tag_set.add(tag)

    def all_tag_groups(self):
        """ Return all set of unique tag groups of tags associated with this 
        instance """
        return set(tag.group for tag in self.tags.all())
