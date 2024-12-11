import os
import joblib
import numpy as np
import json
from django.http import JsonResponse, Http404
from .models import LoanPrediction
from rest_framework.decorators import api_view ,permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths for model and scaler
MODEL_PATH = os.path.join(BASE_DIR, 'ml_models', 'loan_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'ml_models', 'scaler.pkl')

# Load model and scaler
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
@csrf_exempt
def predict_loan_status(request, loan_id=None):
    """
    Handles GET requests to fetch loan prediction details by ID or all loans.
    """
    if request.method == 'GET':
        if loan_id:
            try:
                loan = LoanPrediction.objects.get(id=loan_id)
                response_data = {
                    'id': loan.id,
                    'user_id': loan.user.id,
                    'gender': loan.gender,
                    'married': loan.married,
                    'dependents': loan.dependents,
                    'education': loan.education,
                    'self_employed': loan.self_employed,
                    'applicant_income': loan.applicant_income,
                    'coapplicant_income': loan.coapplicant_income,
                    'loan_amount': loan.loan_amount,
                    'loan_amount_term': loan.loan_amount_term,
                    'credit_history': loan.credit_history,
                    'property_area': loan.property_area,
                    'loan_status': loan.loan_status,
                    'created_at': loan.created_at,
                }
                return JsonResponse(response_data)
            except LoanPrediction.DoesNotExist:
                raise Http404("Loan Prediction not found")
        else:
            loans = LoanPrediction.objects.all().values()
            return JsonResponse(list(loans), safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_loan_prediction(request):
    """
    Handles POST requests to add a new loan prediction.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Define mappings for categorical variables
            gender_mapping = {'Male': 0, 'Female': 1}
            married_mapping = {'No': 0, 'Yes': 1}
            education_mapping = {'Graduate': 0, 'Not Graduate': 1}
            self_employed_mapping = {'No': 0, 'Yes': 1}
            property_area_mapping = {'Urban': 0, 'Semiurban': 1, 'Rural': 2}

            # Map categorical values to numerical values
            gender = gender_mapping[data['Gender']]
            married = married_mapping[data['Married']]
            dependents = int(data['Dependents'])
            education = education_mapping[data['Education']]
            self_employed = self_employed_mapping[data['SelfEmployed']]
            property_area = property_area_mapping[data['Property_Area']]

            # Create feature array
            features = np.array([gender, married, dependents, education, self_employed, data['ApplicantIncome'],
                                 data['CoapplicantIncome'], data['LoanAmount'], data['Loan_Amount_Term'],
                                 data['Credit_History'], property_area]).reshape(1, -1)

            # Scale the features
            scaled_features = scaler.transform(features)

            # Make a prediction
            prediction = model.predict(scaled_features)
            loan_status = "Approved" if prediction[0] == 1 else "Rejected"

            # Save the data to the database
            LoanPrediction.objects.create(
                user = request.user,
                gender=data['Gender'], married=data['Married'], dependents=dependents, education=data['Education'],
                self_employed=data['SelfEmployed'], applicant_income=data['ApplicantIncome'],
                coapplicant_income=data['CoapplicantIncome'], loan_amount=data['LoanAmount'],
                loan_amount_term=data['Loan_Amount_Term'], credit_history=data['Credit_History'],
                property_area=data['Property_Area'], loan_status=loan_status
            )

            return JsonResponse({'loan_status': loan_status})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)