from rest_framework import serializers
from .models import PageURL


class PageURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageURL
        fields = ('url_id', 'long_url', 'created',
                  'hits', 'title', 'description')


class PageURLCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = PageURL
        fields = ('author', 'long_url',)
