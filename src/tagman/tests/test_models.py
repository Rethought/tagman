from django.test import TestCase
from django.db import IntegrityError

from tagman.models import Tag, TagGroup
from tagman.tests.models import TestItem

class TestTags(TestCase):

    def setUp(self):
        self.tag1 = Tag(name="test-tag1")
        self.tag1.save()
        self.tag2 = Tag(name="test-tag2")
        self.tag2.save()
        self.group = TagGroup(name="test-group")
        self.group.save()
        self.item = TestItem(name="test-item")
        self.item.save()
        self.tags = [self.tag1, self.tag2]

    def test_create_tag(self):

        self.assertIsNotNone(self.tag1.pk)

    def test_create_group(self):

        self.assertIsNotNone(self.group.pk)

    def test_add_tag_to_item(self):

        [self.item.tags.add(tag) for tag in self.tags]
        self.assertTrue([tag for tag in self.item.tags.all() if tag in self.tags])

    def test_tags_in_group(self):

        [self.group.tag_set.add(tag) for tag in self.tags]
        self.assertTrue([tag for tag in self.group.tags_for_group() if tag in self.tags])

    def test_unique_tag_in_group(self):

        self.group.tag_set.add(self.tag1)
        tag2 = Tag(name=self.tag1.name)
        self.assertRaises(IntegrityError, self.group.tag_set.add, tag2)

    def test_get_tagged_items(self):

        self.item.tags.add(self.tag1)
        model_items = self.tag1.tagged_model_items(model_cls=self.item.__class__)
        self.assertTrue(self.item in model_items)

    def test_get_tag_for_string(self):

        self.group.tag_set.add(self.tag1)
        self.assertTrue(self.tag1 == Tag.tag_for_string(str(self.tag1)))

    def test_get_tags_for_string(self):

        string = ""
        for idx, tag in enumerate(self.tags):
            self.group.tag_set.add(tag)
            string += "%s%s" % (str(tag), "," if idx+1 is not len(self.tags) else "")
        self.assertTrue([tag for tag in Tag.tags_for_string(string) if tag in self.tags])

    def test_get_all_tag_groups(self):

        [self.item.tags.add(tag) for tag in self.tags]
        [self.group.tag_set.add(tag) for tag in self.tags]
        self.assertTrue([group for group in self.item.all_tag_groups() if group == self.group])

    def test_add_tag_str(self):

        [self.item.add_tag_str("%s:%s" % (self.group, tag)) for tag in self.tags]
        self.assertTrue([tag for tag in self.item.tags.all() if tag in self.tags])



class TestSystemTags(TestCase):
    """ System tags are designed not to appear in most UI - they are auto-added by models
so that they can be searched on and have other functionality. A custom manager on the Tag
prevents these appearing in e.g. admin for users when tagging items. But other managers allow
access to the whole world of tags. Here we test these managers, as well as the rendering of
system tags."""
    def setUp(self):
        self.sys_group = TagGroup(name="system_group", system=True)
        self.sys_group.save()
        self.nonsys_group = TagGroup(name="normal_group", system=False)
        self.nonsys_group.save()

        self.tag_a = Tag(group = self.sys_group, name="tag_a")
        self.tag_b = Tag(group = self.sys_group, name="tag_b")
        self.tag_c = Tag(group = self.nonsys_group, name="tag_c")
        self.tag_d = Tag(group = self.nonsys_group, name="tag_d")
        [getattr(self, "tag_%s"%x).save() for x in "abcd"]

        self.systags = set([self.tag_a, self.tag_b])
        self.nonsystags = set([self.tag_c, self.tag_d])

    def test_manager_default(self):
        nonsystags = set(Tag.objects.all())
        self.assertEquals(nonsystags, self.nonsystags)

    def test_manager_systags(self):
        systags = set(Tag.sys_objects.all())
        self.assertEquals(systags, self.systags)

    def test_manager_alltags(self):
        alltags = set(self.systags)
        alltags.update(self.nonsystags)
        returnedtags = set(Tag.all_objects.all())
        self.assertEquals(alltags, returnedtags)

    def test_sysgroup_representations(self):
        self.assertEquals(str(self.tag_a), "*system_group:tag_a")

    def test_non_sysgroup_representation(self):
        self.assertEquals(str(self.tag_c), "normal_group:tag_c")

    def test_tag_for_string_system_group(self):
        t = Tag.tag_for_string("*system_group:tag_a")
        self.assertEquals(t, self.tag_a)


class TestSlugification(TestCase):
    def setUp(self):
        self.group = TagGroup(name="normal group", system=False)
        self.group.save()

        self.tag_a = Tag(group = self.group, name="tag a")
        self.tag_b = Tag(group = self.group, name="TAG b")
        self.tag_a.save()
        self.tag_b.save()

    def test_slug_values_a(self):
        self.assertEquals(self.tag_a.slug, "tag-a")
        
    def test_slug_values_b(self):
        self.assertEquals(self.tag_b.slug, "tag-b")

