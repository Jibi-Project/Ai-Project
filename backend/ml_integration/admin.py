from django.contrib import admin
from .models import LoanPrediction  # Replace LoanApplication with LoanPrediction

@admin.register(LoanPrediction)
class LoanPredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'gender', 'loan_status', 'created_at')

