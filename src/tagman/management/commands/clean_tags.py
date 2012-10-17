from django.core.management.base import BaseCommand, CommandError
from tagman.models import Tag


class Command(BaseCommand):
    args = ''
    help = 'Removes all archived Tags'

    def handle(self, *args, **options):
        try:
            archived_tags = Tag.objects.filter(archived=True)
            archived_tags.delete()
        except:
            raise CommandError('does not exist')
