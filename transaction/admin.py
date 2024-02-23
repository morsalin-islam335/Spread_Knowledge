from django.contrib import admin

# Register your models here.

from . models import Transaction

# class TransactionAdmin(admin.ModelAdmin):
#     list_display = ['amount']


admin.site.register(Transaction)
