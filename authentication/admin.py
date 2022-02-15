from django.contrib import admin

# Register your models here.
from .models import Tokens


@admin.register(Tokens)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'total']
    search_fields = ['name', ]
    # actions = ['set_chat_friend']
    #
    # def set_chat_friend(self, tkn):
    #     admin_tkn = Tokens.objects.get(user__email='admin@trebuchet.one')
    #     admin_tkn.chat_friends.add(tkn)
