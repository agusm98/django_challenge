from django.shortcuts import render
from .serializers import RatingSerializer, UrlSerializer, CharacterSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .services import ApiCharacter, Database

class CharacterViewSet(viewsets.ViewSet):

    def get(self, request, id):
        conn = ApiCharacter()

        valURL = UrlSerializer(data={'URL':conn.URL, 'Slug':id})

        if not valURL.is_valid():
            return Response({'Error': 'URL no valida'}, status=status.HTTP_404_NOT_FOUND)

        resp = conn.req(id)
        
        return resp


class RatingViewSet(viewsets.ModelViewSet):

    serializer_class = RatingSerializer

    def post(self, request, id):
        rate = request.data.get('rate')
        
        if rate and 1 <= rate <= 5: #Deberia parametrizarse
            db = Database()
            db.insert_rate(id, rate)
            data = {'status': 'ok', 'ID': id, 'Rate': rate}
            stat = status.HTTP_201_CREATED
        
        else:
            data = {'status': 'rate error', 'ID': id, 'Rate': rate}
            stat = status.HTTP_406_NOT_ACCEPTABLE
        
        return Response(data, status=stat)
