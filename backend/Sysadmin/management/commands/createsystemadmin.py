from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a system admin user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        user = User.objects.create_user(
            username=options['username'],
            email=options['email'],
            password=options['password'],
            role='SYSTEM_ADMIN',
            is_staff=True,
            is_superuser=True
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully created system admin: {user.username}'))