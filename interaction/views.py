from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Comment, Rating
from product.models import Product
from .serializers import CommentSerializer, UserCommentsSerializer, RatingSerializer
from .permissions import IsAuthorOrIsAuthenticated


class ProductCommentsList(generics.ListAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        return Comment.objects.filter(product__id=self.kwargs['product_pk'])

class ProductCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthorOrIsAuthenticated]

class AddProductComment(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def perform_create(self, serializer):
        req = dict(serializer.validated_data)
        product = Product.objects.get(pk=self.kwargs['product_pk'])
        parent = req.get('parent', None)
        user = self.request.user
        
        if parent:
            parent = Comment.objects.get(pk=parent.id)
            serializer.save(product=product, parent=parent, user=user)
        else:
            serializer.save(product=product, user=user)

class UserCommentsList(generics.ListAPIView):
    serializer_class = UserCommentsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

class RateProduct(generics.CreateAPIView):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        req = dict(serializer.validated_data)
        user = self.request.user
        product = Product.objects.get(pk=self.kwargs['product_pk'])
        rating = req.get('value')

        if Rating.objects.filter(user=user, product=product).exists():
            raise ValidationError('you have already rated this product.')
        
        product.average_rating = (product.average_rating + rating) / 2 if product.average_rating else rating
        product.save()

        serializer.save(user=user, product=product)
