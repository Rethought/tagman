import logging
from django.db import models
from django.template.defaultfilters import slugify

TAG_SEPARATOR = ":"
logger = logging.getLogger('cms')

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
    name = models.CharField(verbose_name='Name', max_length=100)
    slug = models.SlugField(max_length=100, default="")
    group = models.ForeignKey(TagGroup, verbose_name='Group')

    objects = models.Manager()
    sys_objects = TagManager(sys=True)
    public_objects = TagManager(sys=False)

    def save(self, *args, **kwargs):
        """ assign slug if empty """
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("name", "group",)

    def __unicode__(self):
        return "{0}{1}".format(str(self.group) + TAG_SEPARATOR if self.group else "", self.name)

    def __repr__(self):
        return "{0}{1}".format(str(self.group.slug) + TAG_SEPARATOR if self.group else "", self.slug)

    @property
    def system(self):
        return self.group.system

    def models_for_tag(self):
        """ Return the unique set of model names, all of which have had
        instances tagged with this tag.
        @todo: This is hacky. Can we do it more elegantly?
        """
        return [s[:-4] for s in dir(self) if s[-4:]=='_set']

    def tagged_model_items(self, model_cls=None, model_name="", limit=None):
        """ Return a unique set of instances of a given model, the class for which
        is passed into model_cls OR the name for which is passed in model_name, 
        that are tagged with this tag"""
        def _get_models_items(query_set):
            try:
                _set = getattr(self, query_set)
            except AttributeError:
                return set()
            else:
                return set(_set.all()[:limit] if limit else _set.all())

        if model_cls:
            cls_name = model_cls.__name__.lower()
        else:
            cls_name = model_name.lower()

        model_set = set()
        model_set.update(_get_models_items("{0}_set".format(cls_name)))
        model_set.update(_get_models_items("{0}_auto_tagged_set".format(cls_name)))

        return model_set

    def tagged_items(self, limit=None):
        """ Return a dictionary, keyed on model name, with each value the 
        set of items of that model tagged with this tag. """
        models = self.models_for_tag()
        rdict = {}
        for model in models:
            rdict[model] = self.tagged_model_items(model_name = model, limit=limit)
        return rdict

    @classmethod
    def tag_for_string(cls, s):
        """ Given a tag representation as "[*]GRP:NAME", return 
        the tag instance. 
        @todo: handle the [TagGroup|Tag].DoesNotExist exceptions
        """
        s = s.strip('* ') # representation of system group prefixed *
        groupname, tagname = s.split(TAG_SEPARATOR)
        try:
            grp = TagGroup.objects.get(name = groupname)
            tag = Tag.objects.get(name = tagname, group = grp)
        except TagGroup.DoesNotExist:
            raise Tag.DoesNotExist()
        return tag

    @classmethod
    def get_or_create(cls, group_name, tag_name, system=False):
        """ Like get_or_create on a manager but driven by distinct strings
and creates the TagGroup if required. """
        group, _ = TagGroup.objects.get_or_create(name=group_name, system=system)
        tag, created = Tag.objects.get_or_create(name=tag_name, slug=slugify(tag_name), group=group)
        if created:
            logger.debug("Created tag via get_or_create with repr {0} and ID {1}".format(repr(tag), tag.id))
        return tag

    @classmethod
    def get_or_create_tag_for_string(cls, s):
        """ Given a tag representation as "[*]GRP:NAME", return the
tag instance. """
        group,name = s.strip('* ').split(':')
        is_system = True if s.strip()[0]=='*' else False
        return Tag.get_or_create(group, name, is_system)
           
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
    tags = models.ManyToManyField(Tag, related_name="%(class)s_set", blank=True)
    auto_tags = models.ManyToManyField(Tag, related_name="%(class)s_auto_tagged_set", blank=True, editable=False)

    class Meta:
        abstract = True

    def add_tag_str(self, string, auto_tag=False):
        """ Create a tag from a string and add to tags.
If auto_tag = True, return from the auto_tags list instead of tags """
        tags = self.auto_tags if auto_tag else self.tags
        tag = Tag.get_or_create_tag_for_string(string)
        tags.add(tag)
        return tag

    def all_tag_groups(self, auto_tag=False):
        """ Return all set of unique tag groups of tags associated with this 
        instance. If auto_tag = True, return from the auto_tags list instead of tags """
        tags = self.auto_tags if auto_tag else self.tags
        return set(tag.group for tag in tags.all())

class TaggedContentItem(TaggedItem):
    """ Mixin for models that would have features such as auto-tagging
enabled. """
    class Meta:
        abstract = True

    def _make_self_tag_name(self):
        return self.slug

    def associate_auto_tags(self):
        """ Automatically tag myself (by adding to auto_tags):
 * <model name>:<slug>.

 Overide _make_self_tag_name(self) to change the slug used.
 """
        tag_group = self.__class__.__name__
        tag_name = self._make_self_tag_name()
        tag = self.add_tag_str("*{0}:{1}".format(tag_group, tag_name), auto_tag=True)
        logger.info("Auto tagging {0} with {1}".format(str(self), repr(tag)))
        return tag


