from django.contrib import admin

from app.models import CoinData


class CoinDataAdmin(admin.ModelAdmin):
    list_display = ('coin_name','price', 'last_updated')

# Register your models here.
admin.site.register(CoinData, CoinDataAdmin)
