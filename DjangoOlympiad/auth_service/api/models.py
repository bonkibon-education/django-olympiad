from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, AbstractUser, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models


class SoftDeleteManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Role(models.Model):
    """
    Role model to which users are assigned.
    """
    name = models.CharField(
        verbose_name="Название роли",
        unique=True,
        max_length=50,
        null=False,
        blank=False,
        validators=[MinLengthValidator(1)]
    )

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser):
    """
    Custom user model with username, last and first name and hashed password. Also has roles list that allows to check
    if he's a doctor or maybe an admin (is_staff & is_superuser goes to play roblox)
    """
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    username = models.CharField(
        verbose_name='Никнейм',
        max_length=250,
        unique=True,
        null=False,
        blank=False,
        validators=[MinLengthValidator(1)]
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
        unique=False,
        null=False,
        blank=False,
        validators=[MinLengthValidator(1)]
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50,
        unique=False,
        null=False,
        blank=False,
        validators=[MinLengthValidator(1)]
    )

    role = models.ForeignKey(
        Role,
        verbose_name="Роль",
        related_name="users",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
        'password'
    )

    objects = SoftDeleteManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def soft_delete(self):
        self.is_active = False
        self.save()
