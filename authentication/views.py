from .models import users
from .serializers import UserSerializer
from .permissons import UserPermission

from rest_framework import viewsets, status, filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
# Create your views here.

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            # is_trainer = TRAINERS.objects.filter(user_id=user.pk).exists()

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
            })
        else:
            return Response({"Response": "username or password was incorrect"}, status=status.HTTP_401_UNAUTHORIZED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]  # Default permission class
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'username', 'email', 'first_name', 'last_name']
    search_fields = ('username','email', 'first_name', 'last_name', )

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        token = Token.objects.get(user=client.user).key
        data = serializer.data
        data['token'] = token
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        kewargs = {'partial': True}
        return super().update(request, *args, **kewargs)