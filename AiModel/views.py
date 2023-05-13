from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from .models import Xray
from .serializers import XraySerializer

# Create your views here.

class XrayViewSet(viewsets.ModelViewSet):
    queryset = Xray.objects.all()
    serializer_class = XraySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__email', 'user__phone', 'user__first_name',
                     'user__last_name', 'patient_name', 'result']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() :
            # serializer.save()
            instance = serializer.save()

            result = serializer.predict()

            instance.result = str(result)
            instance.save()
            print("$"*100)
            request.data["result"] = str(result)
            return Response({"response": request.data["result"]}, status=status.HTTP_201_CREATED)
            # return Response(chestTestSerializer.data.update(result=result), status=status.HTTP_201_CREATED)
        else:
            return Response({"response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

