from datetime import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Credit
from .serializers import CreditSerializer
from django.shortcuts import get_object_or_404
from django.utils.timezone import now  # Importer la fonction now pour la date/heure actuelle
from django.core.mail import send_mail


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


    #URL : POST /credits/{id}/approve/

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        # Récupérer la demande de crédit
        credit = get_object_or_404(Credit, pk=pk)
        
        # Vérifier si l'utilisateur est un admin
        if request.user.role == 'admin':
            # Mettre à jour la date d'approbation et le statut
            credit.date_approvee = now()
            credit.statut = 'approuvé'
            credit.save()

            # Envoyer un email au client
            subject = "Votre crédit a été approuvé"
            message = (
                f"Bonjour {credit.client.nom},\n\n"
                f"Nous sommes heureux de vous informer que votre demande de crédit a été approuvée.\n"
                f"Détails du crédit :\n"
                f"- Montant demandé : {credit.montant_demande} €\n"
                f"- Durée : {credit.duree} mois\n"
                f"- Taux d'intérêt : {credit.taux_interet}%\n"
                f"- Montant total à rembourser : {credit.montant_total_remboursement} €\n\n"
                f"Cordialement,\nL'équipe de gestion des crédits."
            )
            send_mail(
                subject=subject,
                message=message,
                from_email="selfeni.company@gmail.com",  # Remplacez par votre adresse email
                recipient_list=[credit.client.email],
            )

            return Response(
                {"message": "Credit approved and email sent to the client."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Not authorized."},
                status=status.HTTP_403_FORBIDDEN,
            )
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        # Récupérer la demande de crédit
        credit = get_object_or_404(Credit, pk=pk)

        # Vérifier si l'utilisateur est un admin
        if request.user.role == 'admin':
            # Mettre à jour le statut à "refusé"
            credit.statut = 'refusé'
            credit.date_approvee = None  # Réinitialiser la date d'approbation si nécessaire
            credit.save()

            # Envoyer un email au client
            subject = "Votre demande de crédit a été refusée"
            message = (
                f"Bonjour {credit.client.nom},\n\n"
                f"Nous regrettons de vous informer que votre demande de crédit a été refusée.\n"
                f"Pour plus d'informations, veuillez contacter notre service client.\n\n"
                f"Cordialement,\nL'équipe de gestion des crédits."
            )
            send_mail(
                subject=subject,
                message=message,
                from_email="selfeni.company@gmail.com",  # Remplacez par votre adresse email
                recipient_list=[credit.client.email],
            )

            return Response(
                {"message": "Credit rejected and email sent to the client."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Not authorized."},
                status=status.HTTP_403_FORBIDDEN,
            )