from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailAuthBackend(BaseBackend):
    """Бэкенд аутентификации по E-mail и паролю"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Аутентификация пользователя по email и паролю.
        Параметр username используется для совместимости, но интерпретируется как email.
        """
        user_model = get_user_model()
        try:
            # Пытаемся найти пользователя по email
            user = user_model.objects.get(email=username)
            # Проверяем пароль
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None
    
    def get_user(self, user_id):
        """Получение пользователя по ID"""
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None