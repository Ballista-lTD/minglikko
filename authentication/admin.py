from django.contrib import admin

# Register your models here.
from .models import Tokens


@admin.register(Tokens)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'total']
    search_fields = ['name', 'user', ]



