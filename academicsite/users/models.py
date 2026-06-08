from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Расширенная модель пользователя с дополнительными полями"""
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Фотография'
    )
    date_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username