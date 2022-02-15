from django.contrib.auth.models import User, Group

from rest_framework import serializers

from chats.models import Bundle
from .models import Tokens

# first we define the serializers
ques = ['intelligence', 'strength',
        'beauty', 'charisma', 'wealth', 'will_help_poor',
        'religiousity', 'liberal']


class GetTokensSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    chat_friends = serializers.SerializerMethodField()

    class Meta:
        model = Tokens
        fields = [
            'id', 'user', 'intelligence', 'strength',
            'beauty', 'charisma', 'wealth', 'will_help_poor',
            'religiousity', 'liberal', 'total', 'chat_friends'
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'total': {'read_only': True},
        }

    def get_total(self, obj):
        return obj.total

    def get_chat_friends(self, tkn):
        return [{"name": chat_user.name, 'token': chat_user.name,
                 'bundle': Bundle.objects.filter(user=chat_user.user).exists()} for chat_user in
                tkn.chat_friends.all()]


class GetTokensToOthersSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    private_token = serializers.SerializerMethodField()

    class Meta:
        model = Tokens
        fields = [
            'name', 'intelligence', 'strength',
            'beauty', 'charisma', 'wealth', 'will_help_poor',
            'religiousity', 'liberal', 'total'
        ]

        extra_kwargs = {
            'user': {'read_only': True},
            'total': {'read_only': True},
        }

    def get_total(self, obj):
        return obj.total

    def get_private_token(self, obj):
        return obj.name


class UserSerializer(serializers.ModelSerializer):
    tokens = GetTokensSerializer(many=False, read_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', "first_name", "last_name", 'tokens',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)
