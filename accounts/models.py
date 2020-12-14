from django.db import models

from django.contrib.auth.models import (User, AbstractUser, BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin, Permission)

from django.utils import timezone

from django.conf import settings

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


######################################################################################################################


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


##############################################################################################################


def get_default_profile_pic():
    return 'images/profile_pics/default_profile_pics/profile_pic.jpg'


class CustomUser(AbstractUser, PermissionsMixin):

    # required fields
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # login parameter
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()

    def get_all_permissions(self, obj=None):
        if self.is_superuser:
            return Permission.objects.all()
        return Permission.objects.filter(group__user=self)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        if perm in self.get_all_permissions() or perm in self.get_group_permissions():
            return True
        return False

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile',  on_delete=models.CASCADE)

    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)

    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile_pics/')
    uplay_nickname = models.CharField(max_length=60, null=True, blank=True, unique=True)

    @property
    def profile_pic_url(self):
        return str(self.profile_pic)[1:]

    def get_profile_pic_filename(self):
        return str(self.profile_pic)[str(self.profile_pic).index(f'profile_pics/{self.pk}/'):]

    def __str__(self):
        return f"Name: {self.last_name} {self.first_name}"
    



# class Editor(models.Model):
#     user = models.OneToOneField(User, related_name='editor', on_delete=models.CASCADE)
#
#     class Meta:
#         permissions = [
#             ('read_posts', "Can read posts"),
#             ('leave_comments', "Can leave comments"),
#             ('create_posts', "Can create new posts"),
#             ('edit_posts', "Can edit posts"),
#             ('delete_posts', "Can delete posts"),
#         ]


# class CustomUserProfile(models.Model):
#     user = models.OneToOneField(User, related_name='profile', null=True, on_delete=models.CASCADE)
#
#     bio = models.TextField(null=True, blank=True)
#     profile_pic = models.ImageField(null=True, blank=True, upload_to='images/profile_pics/')
#     uplay_nickname = models.CharField(null=True, blank=True, max_length=255)
#
#     def __str__(self):
#         return self.user.username




