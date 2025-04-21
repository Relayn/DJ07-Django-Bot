from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TelegramUser
from .serializers import TelegramUserSerializer
from rest_framework import status

@api_view(['POST']) # Этот декоратор указывает, что представление обрабатывает только POST-запросы [cite: 65]
def register_user(request):
    data = request.data # Получаем данные из запроса [cite: 64]

    # Используем get_or_create для регистрации или получения существующего пользователя [cite: 64]
    user, created = TelegramUser.objects.get_or_create(
        user_id=data.get('user_id'), # Получаем user_id из данных запроса
        defaults={'username': data.get('username', '')} # Устанавливаем username при создании, если он есть
    )

    if created:
        # Если пользователь создан успешно
        serializer = TelegramUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED) # Возвращаем данные нового пользователя и статус 201 [cite: 67]
    else:
        # Если пользователь уже существует
        return Response({'message': 'User is already registered'}, status=status.HTTP_200_OK) # Возвращаем сообщение и статус 200