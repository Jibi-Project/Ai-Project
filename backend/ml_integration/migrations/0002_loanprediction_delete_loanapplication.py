# Generated by Django 5.1.3 on 2024-12-03 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ml_integration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10)),
                ('married', models.CharField(max_length=10)),
                ('dependents', models.IntegerField()),
                ('education', models.CharField(max_length=20)),
                ('self_employed', models.CharField(max_length=10)),
                ('applicant_income', models.FloatField()),
                ('coapplicant_income', models.FloatField()),
                ('loan_amount', models.FloatField()),
                ('loan_amount_term', models.IntegerField()),
                ('credit_history', models.FloatField()),
                ('property_area', models.CharField(max_length=20)),
                ('loan_status', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='LoanApplication',
        ),
    ]