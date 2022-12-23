from django.db import models

# Create your models here.


class CoinData(models.Model):
    coinId = models.CharField(max_length=300, unique=True)
    coin_name = models.CharField(max_length=300, null=False, blank=False)
    price = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    def date_last_updated(self):
        return self.last_updated.strftime('%B %d %Y')

    def __str__(self):
        return self.coin_name




