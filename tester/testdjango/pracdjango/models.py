from django.db import models

# Create your models here.

class IPRequestLog(models.Model): # 不要忘记加 models.Model!!!
    """This is to record ip address apply log"""

    # id = models.AutoField(primary_key=True) Django 默认自动创建，没有特殊需要可以不加
    ip_address = models.CharField(max_length=64)
    request_count = models.IntegerField(default=1)
    last_request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.ip_address} - {self.last_request_time}"
    