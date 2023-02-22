from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Profile
from product.models import Product


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        email = self.validated_data['email']

        if password != password2:
            raise serializers.ValidationError({'error': 'entered passwords do not match!'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'this email is already taken!'})

        new_account = User(username=self.validated_data['username'], email=email)
        new_account.set_password(password)
        new_account.save()

        return new_account

class ProfileSerializer(serializers.ModelSerializer):
    favorites = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        many=True, 
        required=False,
        slug_field='name'
    )

    class Meta:
        model = Profile
        exclude = ('id', 'user')