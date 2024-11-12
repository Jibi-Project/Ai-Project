from datetime import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Credit
from .serializers import CreditSerializer
from django.shortcuts import get_object_or_404

class CreditViewSet(viewsets.ModelViewSet):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

    # Pour récupérer uniquement les crédits d'un utilisateur spécifique
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.role == 'client':
            queryset = Credit.objects.filter(client=user)
        elif user.is_authenticated and user.role == 'admin':
            queryset = Credit.objects.all()
        else:
            return Response({"detail": "Not authorized."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Override create to set client to the current user if it's a client
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if request.user.role == 'client':
            data['client'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # Endpoint pour approuver une demande de crédit (réservé aux admins)
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        credit = get_object_or_404(Credit, pk=pk)
        if request.user.role == 'admin':
            credit.date_approvee = timezone.now()
            credit.save()
            return Response({"status": "approved"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
