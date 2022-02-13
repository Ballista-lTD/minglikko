from django.contrib import admin

# Register your models here.
from .models import Tokens


@admin.register(Tokens)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'total']
    search_fields = ['name', 'user__username', 'user__firstname']
    actions = ['set_name']

    @staticmethod
    def total(request):
        return request.total

    def set_name(self, _, queryset):
        for i in queryset:
            i.set_name()
