# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

from app.models import Transaction, CoinData
from import_export import resources
from import_export.admin import ImportMixin


class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        fields = ['id', 'bill_for', 'issue_date', 'due_date', 'total', 'status', 'created_time']

@admin.register(CoinData)
class CoinDataAdmin(admin.ModelAdmin):
    list_display = ['coinId', 'coin_name', 'last_updated', 'price']
