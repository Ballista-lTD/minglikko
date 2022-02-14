import random

from django.contrib.auth.models import User, Group
from django.db.models import Q
from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Tokens
from rest_framework_social_oauth2.authentication import SocialAuthentication
from .authentication import CsrfExemptSessionAuthentication
from .permissions import IsOwner
from .serializer import UserSerializer, GroupSerializer, GetTokensSerializer, GetTokensToOthersSerializer


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
        self.queryset = self.queryset.filter(id=request.user.id)
        return viewsets.ModelViewSet.list(self, request, *args, **kwargs)


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TokenApiviewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tokens.objects.filter(total__gt=0)
    serializer_class = GetTokensSerializer
    http_method_names = ['get', 'patch']

    def get_queryset(self):
        return Tokens.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get", ], url_path='others')
    def others(self, request, *args, **kwargs):

        tkns = list(Tokens.objects.filter(total__gt=0).filter(~Q(user=self.request.user)))
        random.shuffle(tkns)
        serializer = GetTokensToOthersSerializer(tkns, many=True)
        return Response(serializer.data, status=200)

    # @action(detail=False, methods=["get", ], url_path='o')
    # def o(self, request, *args, **kwargs):
    #     patient = [tkn.name for tkn in Tokens.objects.only('name').filter(~Q(user=request.user))]
    #     return Response(patient)

    def update(self, request, *args, **kwargs):
        tkn = request.user.tokens
        # if tkn.total == 0:
        #     intelligence = request.data['intelligence']
        #     strength = request.data['strength']
        #     beauty = request.data['beauty']
        #     charisma = request.data['charisma']
        #     wealth = request.data['wealth']
        #     will_help_poor = request.data['will_help_poor']
        #     religiousity = request.data['religiousity']
        #     liberal = request.data['liberal']
        #     total = sum([intelligence, strength, beauty, charisma, wealth, will_help_poor, religiousity, liberal])
        #     print(total)
        #     if total <= 20:
        #         serializer = GetTokensSerializer(tkn, data=request.data)
        #         serializer.is_valid(raise_exception=True)
        #         serializer.save()
        #         return Response(serializer.data)
        #     return Response({"detail": "total point must be less than 20"})
        try:
            tkns: str[:] = request.data['priority']
            print(tkns)
            if tkns and tkn.total:

                if len(tkns) != Tokens.objects.filter(total__gt=0).count() - 1:
                    return Response(
                        {"detail": f"you have to send the {Tokens.objects.filter(total__gt=0).count() - 1} tokens"},status=402)
                if tkns.__contains__(tkn.name):
                    return Response({"detail": "Ninak vere arem kitathond ano ninne thanne edukane"},status=402)
                tkn.priority_list = tkns
                tkn.save()
                serializer = GetTokensSerializer(tkn)
                print('ellam ith vare okey')
                return Response(serializer.data, status=200)
            else:
                return Response({"detail": "form fill akkathork optionum illa "}, status=402)
        except KeyError:
            print("priority not send")
        except Exception as e:
            print(f"{e = }")
        return Response({"detail": "thante avasram kazhinj sed avalle better luck next time"},status=402)
