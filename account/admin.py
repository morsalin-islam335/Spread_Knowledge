from django.contrib import admin

# Register your models here.

from . models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'balance']

    def name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    def email(self, obj):
        return f"{obj.user.email}"


admin.site.register(Account, AccountAdmin)

