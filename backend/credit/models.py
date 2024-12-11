from decimal import Decimal
from django.db import models
from api.models import User
from ml_integration.models import LoanPrediction

class Credit(models.Model):
    STATUT_CHOICES = [
        ('encours', 'En cours'),
        ('approuvé', 'Approuvé'),
        ('refusé', 'Refusé'),
        ('remboursé', 'Remboursé'),
    ]
    
    TAUX_INTERET = Decimal('5.00')  # Constant interest rate of 5%
    
    montant_demande = models.DecimalField(max_digits=15, decimal_places=2)
    duree = models.IntegerField()  # Duration in months
    date_demande = models.DateTimeField(auto_now_add=True)
    date_approvee = models.DateTimeField(null=True, blank=True)
    montant_total_remboursement = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credits')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='encours') 
        # Foreign key to LoanPrediction
    loan_prediction = models.ForeignKey(
        LoanPrediction,
        on_delete=models.SET_NULL,  # Optional: set to null if the related LoanPrediction is deleted
        null=True,  # Allow null values if a Credit is not linked to a LoanPrediction
        blank=True,  # Allow the field to be optional in forms
        related_name='credits'  # Reverse relation name
    )


    def save(self, *args, **kwargs):
        # Automatically calculate the total repayment amount if not specified
        if not self.montant_total_remboursement:
            # Convert 'duree / 12' to Decimal
            duree_years = Decimal(self.duree) / Decimal(12)
            self.montant_total_remboursement = self.montant_demande * (1 + self.TAUX_INTERET / 100 * duree_years)
        super().save(*args, **kwargs)

    def get_users_with_ongoing_credits():
    # Filter users with ongoing credits
        ongoing_credits = User.objects.filter(credits__statut='encours').distinct()
        return ongoing_credits