from django.db import models
import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
# from administration.models import branches
# Create your models here.

# builten custom account manager from django project
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

class Employeement_type(models.Model):
    name = models.CharField(max_length=150)
    
    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.name


class Employeement_Info(models.Model):
    emp_type = models.ForeignKey(Employeement_type, verbose_name=_("Employee"), on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)

    

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.name



# Customer model that get the information of the users
class Employee(AbstractBaseUser, PermissionsMixin):
    emp_type = models.ForeignKey(Employeement_Info, verbose_name=_("Employee"), on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    is_employee = models.BooleanField(default=False)
    is_agree_policy = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # groups = models.ManyToManyField(
    #     Group,
    #     related_name="employee_groups",  # Custom related_name to avoid conflict
    #     blank=True,
    #     )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name="employee_user_permissions",  # Custom related_name to avoid conflict
    #     blank=True,
    # )


    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"
        permissions = [
            ("assign_permissions", "Can assign permissions"),
            # other permissions
        ]


    # def email_user(self, subject, message):
    #     send_mail(
    #         subject,
    #         message,
    #         'mobensediqi01@gmail.com',
    #         [self.email],
    #         fail_silently=False,
    #     )
    
    def __str__(self):
        return self.name


   

def create_Employee_permission():
    content_type = ContentType.objects.get_for_model(Employee)
    return Permission.objects.create(
        codename='can_create_mymodel',
        name='Can create MyModel instances',
        content_type=content_type,
    )

def edit_Employee_permission():
    content_type = ContentType.objects.get_for_model(Employee)
    return Permission.objects.create(
        codename='can_edit_mymodel',
        name='Can edit MyModel instances',
        content_type=content_type,
    )

def delete_Employee_permission():
    content_type = ContentType.objects.get_for_model(Employee)
    return Permission.objects.create(
        codename='can_delete_mymodel',
        name='Can delete MyModel instances',
        content_type=content_type,
    )


   

