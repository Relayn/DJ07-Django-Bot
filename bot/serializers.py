from rest_framework import serializers
from .models import TelegramUser

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__' # Включаем все поля модели [cite: 62]
        # Если нужно выбрать определенные поля, используй: fields = ['user_id', 'username'] [cite: 63]