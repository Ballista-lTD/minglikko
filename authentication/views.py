from django.contrib.auth.models import User, Group
from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Tokens
from rest_framework_social_oauth2.authentication import SocialAuthentication
from .authentication import CsrfExemptSessionAuthentication
from .permissions import IsOwner
from .serializer import UserSerializer, GroupSerializer, GetTokensSerializer


class UserApiViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    serializer_class = UserSerializer
    authentication_classes = [CsrfExemptSessionAuthentication, SocialAuthentication, OAuth2Authentication]
    queryset = User.objects.all()
    http_method_names = ['get', "patch", "options", 'put', 'post']

    def get_queryset(self):
        try:
            return User.objects.filter(id=self.request.user.id)
        except User.DoesNotExist:
            return User.objects.none()
        except Exception:
            return User.objects.none()

    def list(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            self.queryset = self.queryset.filter(pk=request.user.pk)
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)

    @action(detail=False, methods=["get", "post", 'patch', 'put'], url_path='me')
    def me(self, request, *args, **kwargs):
        print(request.method)
        if request.method == "PATCH" or request.method == "PUT":
            print("patch is called")
            try:
                print(request.data)
                token_data = request.data.get("tokens")
                print(token_data)
                token = Tokens.objects.get(user=request.user)
                print(token)
                serializer = GetTokensSerializer(token, data=token_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except KeyError:
                pass
        else:
            self.queryset = self.queryset.filter(id=request.user.id)
            return viewsets.ModelViewSet.list(self, request, *args, **kwargs)
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TokenApiviewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tokens.objects.all()
    serializer_class = GetTokensSerializer
    http_method_names = ['get', 'patch', 'post']

    def get_queryset(self):
        return Tokens.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        tkn = request.user.tokens
        #TODO flip this
        if tkn.total == 0:
            intelligence = request.data['intelligence']
            strength = request.data['strength']
            beauty = request.data['beauty']
            charisma = request.data['charisma']
            wealth = request.data['wealth']
            will_help_poor = request.data['will_help_poor']
            religiousity = request.data['religiousity']
            liberal = request.data['liberal']
            total = sum([intelligence, strength, beauty, charisma, wealth, will_help_poor, religiousity, liberal])
            print(total)
            if total <= 20:
                serializer = GetTokensSerializer(tkn, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)

            return Response({"detail": "total point must be less than 20"})
        return Response({"detail": "thanik orale kitya pore"})
