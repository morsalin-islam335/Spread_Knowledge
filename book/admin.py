from django.contrib import admin

# Register your models here.
from . models import *

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",),} # eta ekta dictionary hoiba jar slug hoiba slug and onno jinish hoiba ekta value of  tuple

    list_display = ['name']
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Borrow)
