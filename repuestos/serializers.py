from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Repuesto


class RepuestoSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Repuesto
        fields = '__all__'

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser un número entero positivo mayor a 0.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("La cantidad en stock no puede ser un número negativo.")
        return value

    def validate_nombre(self, value):
        nombre_limpio = value.strip()
        if len(nombre_limpio) < 3:
            raise serializers.ValidationError("El nombre del repuesto debe contener al menos 3 caracteres.")
        return nombre_limpio

    def validate_categoria(self, value):
        if not value.strip():
            raise serializers.ValidationError("La categoría es requerida.")
        return value.strip()


class UserRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=4)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
