from rest_framework import serializers
from api.models import Post, Media

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("content", )


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ("post", "media")