from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

# Create your models here.

class UserSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user'
    )
    session = models.OneToOneField(
        Session,
        on_delete=models.CASCADE,
        db_column='session'
    )
    def __str__(self):
        # 因为设置了外键，所以可以通过user 和 session获得
        return f"{self.user.username} - {self.session.session_key}"

class Post(models.Model):
    """
    Model to store user posts.
    """
    user_id = models.IntegerField()
    content = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.content} - {self.created_at}"

