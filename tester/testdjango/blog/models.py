from django.db import models

# Create your models here.

class Post(models.Model):
    """
    Model to store blog content.
    """
    title = models.CharField(max_length=50)
    content = models.TextField()
    user_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title}-{self.content}-{self.user_id}-{self.created_at}"