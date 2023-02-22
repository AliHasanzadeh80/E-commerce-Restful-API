from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileSerializer, RegistrationSerializer
from .models import Profile
from product.models import Product


@api_view(['POST',])
def registration(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        response = {}
        if serializer.is_valid():
            new_account = serializer.save()
            response['username'] = new_account.username
            response['email'] = new_account.email           
        else:
            response = serializer.errors

        return Response(response, status=status.HTTP_201_CREATED)

class UserProfile(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

class AddToFavorites(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        favorite_products = self.get_object().first().favorites

        if not product in favorite_products.all():
            favorite_products.add(product)
        else:
            raise ValidationError('This product is already in your favorites.')

class RemoveFromFavorites(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return Profile.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        favorite_products = self.get_object().first().favorites

        if product in favorite_products.all():
            favorite_products.remove(product)
