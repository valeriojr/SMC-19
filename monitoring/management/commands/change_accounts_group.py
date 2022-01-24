from django.core.management import BaseCommand

from accounts.models import Group, Account


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('group', nargs=1, type=str)

    def handle(self, *args, **options):
        group = Group.objects.get(name=options['group'][0])
        if group is not None:
            Account.objects.all().update(group=group)
        else:
            print('Error: group %s not found' % options[group])
