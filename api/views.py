from django.shortcuts import render
from .models import Rating
from .serializers import RatingSerializer, UrlSerializer, CharacterSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .services import ApiCharacter

class CharacterViewSet(viewsets.ViewSet):

    def get(self, request, id):
        conn = ApiCharacter()

        valURL = UrlSerializer(data={'URL':conn.URL, 'Slug':id})

        if not valURL.is_valid():
            return Response({'Error': 'URL no valida'}, status=status.HTTP_404_NOT_FOUND)
        
        #que se encargue de parsear y toda la pelota
        resp = conn.req(id)
        
        return resp


class RatingViewSet(viewsets.ModelViewSet):

    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def post(self, request, id):
        rate = request.data.get('rate')

        #Utilizar RatingSerializer y encajar
        '''
        RatingSerializer.append('id', '')
        '''
        return Response({'Posteo': 'Si', 'ID': id, 'Rate': rate}, status=status.HTTP_200_OK)
