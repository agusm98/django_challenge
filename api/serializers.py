from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'date', 'character_id', 'character_name', 'rate')

class UrlSerializer(serializers.Serializer):
    '''Serializer para validacion de urls'''
    URL = serializers.URLField()
    Slug = serializers.SlugField()

class CharacterSerializer(serializers.Serializer):
    fields = ('name', 'height', 'mass', 'hair_color', 'skin_color', 'eye_color',\
        'birth_year', 'gender', 'homeworld')