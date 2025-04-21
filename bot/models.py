from django.db import models

class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True)  # ID пользователя в Telegram [cite: 57]
    username = models.CharField(max_length=255, blank=True, null=True)  # Никнейм [cite: 57]
    created_at = models.DateTimeField(auto_now_add=True)  # Дата регистрации [cite: 58]

    def __str__(self):
        return f"{self.username} ({self.user_id})"