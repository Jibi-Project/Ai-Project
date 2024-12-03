from django.db import models

class LoanPrediction(models.Model):
    gender = models.CharField(max_length=10)
    married = models.CharField(max_length=10)
    dependents = models.IntegerField()
    education = models.CharField(max_length=20)
    self_employed = models.CharField(max_length=10)
    applicant_income = models.FloatField()
    coapplicant_income = models.FloatField()
    loan_amount = models.FloatField()
    loan_amount_term = models.IntegerField()
    credit_history = models.FloatField()
    property_area = models.CharField(max_length=20)
    loan_status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)