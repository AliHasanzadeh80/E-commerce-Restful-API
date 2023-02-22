from rest_framework import serializers

from .models import Comment, Rating


class CommentSerializer(serializers.ModelSerializer):
    sub_comments = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='product-comment-detail',
        required=False
    )
    parent = serializers.SlugRelatedField(
        queryset=Comment.objects.all(),
        slug_field='id',
        required=False
    )
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'parent', 'sub_comments')

class UserCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content')

class RatingSerializer(serializers.ModelSerializer):
    product = serializers.CharField(required=False)
    
    class Meta:
        model = Rating
        fields = '__all__'