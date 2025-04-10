from django.utils import timezone
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        now = timezone.now()
        
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        is_staff = extra_fields.pop('is_staff', False)
        is_active = extra_fields.pop('is_active', True)
        is_superuser = extra_fields.pop('is_superuser', False)
        last_login = extra_fields.pop('last_login', now)
        date_joined = extra_fields.pop('date_joined', now)

        
        user = self.model(
            email=email, first_name=first_name,
            last_name=last_name,is_staff=is_staff, is_active=is_active, 
            is_superuser=is_superuser,
            last_login=last_login, date_joined=date_joined, **extra_fields)
        
        user.set_password(password)
        user.save()

        return user
        
        
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        user = self.create_user(email, first_name, last_name, password, **extra_fields)

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()

        return user   
