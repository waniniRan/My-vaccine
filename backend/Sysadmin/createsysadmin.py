from django.core.management.base import BaseCommand
from django.contrib.auth.password_validation import validate_password
from Sysadmin.models import User

class Command(BaseCommand):
    help = 'Creates a new system administrator account'
    
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
    
    def handle(self, *args, **options):
        try:
            validate_password(options['password'])
            
            user = User.objects.create_user(
                username=options['username'],
                email=options['email'],
                password=options['password'],
                role=User.Role.SYSTEM_ADMIN,
                must_change_password=False  # System admins get permanent passwords
            )
            
            self.stdout.write
            self.style.SUCCESS(f'Successfully created system admin: {user.username}')
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))