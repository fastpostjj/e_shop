from django.core.management import BaseCommand
from user_auth.models import User


class Command(BaseCommand):
    """
    {
    "email":"admin@admin.pro",
    "password":"123abc123"
}
    {
    "email":"user@user.ru",
    "password":"123abc123"
}
    """

    def create_superuser(self, *args, **options):
        user = User.objects.create(
            email='admin@admin.pro',
            first_name='Admin',
            last_name='SuperAdmin',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('123abc123')
        user.save()

    def create_user(self, *args, **options):
        user = User.objects.create(
            email='user@user.ru',
            first_name='User',
            last_name='Just User',
            is_staff=False,
            is_superuser=False
        )
        user.set_password('123abc123')
        user.save()

    def change_password(self, *args, **options):
        user = User.objects.get(email='example@example.com')
        user.set_password('123abc123')
        user.save()

    def handle(self, *args, **options):
        self.create_superuser(*args, **options)
        self.create_user(*args, **options)
        # self.change_password(*args, **options)
