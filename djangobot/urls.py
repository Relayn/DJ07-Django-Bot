from django.contrib import admin
from django.urls import path, include # Импортируем include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bot.urls')), # Включаем URL-адреса приложения bot под префиксом /api/
]