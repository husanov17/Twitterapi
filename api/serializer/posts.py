from rest_framework import serializers
from api.models.posts import Post, Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    mediafiles = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    
    
    