from rest_framework import serializers
from .models import CustomUser, Tag, Post, Comment

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'bio']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)
    # comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'tags']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', None)
        post = Post.objects.create(**validated_data)
        if tags_data:
            post.tags.set(tags_data)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return representation
