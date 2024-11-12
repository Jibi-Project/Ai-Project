from rest_framework import serializers
from .models import ROLE_CHOICES, User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES, default='client')

    class Meta:
        model = User
        fields = ["id", "username", "password", "role", "nom", "prenom", "email", "telephone", "adresse"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"required": False},
            "email": {"required": True},
        }

    def create(self, validated_data):
        role = validated_data.get('role', 'client')
        
        if not validated_data.get("username"):
            validated_data["username"] = validated_data["email"]
        
        # Create the user with the additional fields
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            nom=validated_data["nom"],
            prenom=validated_data["prenom"],
            telephone=validated_data["telephone"],
            adresse=validated_data["adresse"],
            role=role
        )
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Ajouter des informations supplémentaires sur l'utilisateur
        user = self.user
        data['user'] = {
            'id': user.id,
            'nom': user.nom,
            'prenom': user.prenom,
            'email': user.email,
            'telephone': user.telephone,
            'adresse': user.adresse,
            'role': user.role,
        }
        
        return data
