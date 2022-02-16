from django.contrib import admin

# Register your models here.
from .models import Tokens


@admin.register(Tokens)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'total', 'friend']
    search_fields = ['name', ]
    list_per_page = 600

    # actions = ['set_chat_friend']
    #
    # def set_chat_friend(self, tkn):
    #     admin_tkn = Tokens.objects.get(user__email='admin@trebuchet.one')
    #     admin_tkn.chat_friends.add(tkn)tk
    def friend(self, request):
        return "\n".join([f"{tkn.user.username}: o-{tkn.priority_list.index(request.name)}" for tkn in
                          request.chat_friends.all()])
    # #
    # def get_queryset(self, request):
    #     return Tokens.objects.all().exclude(total=0)
