import requests
from rest_framework.response import Response
from rest_framework import status
from .serializers import CharacterSerializer


def generate_request(url, **kw):
    resp = requests.get(url, params=kw)
    return resp

class ApiCharacter():

    URL = None
    response = Response()

    def __init__(self):
        self.URL = 'http://swapi.dev/api/people/'

    def __get_character(self, char_id):
        '''Se consume la api de personajes segun id personaje'''
        return generate_request(self.URL+char_id)

    def __add_average_rating(self):
        return {'avg_rating': 8}

    def __add_max_rating(self):
        return {'rating': 8}

    @staticmethod
    def __filter_keys(json, fields):
        '''Se filtran el diccionario json, armando un nuevo diccionario solo con los campos necesarios'''

        return dict(filter(lambda x: x[0] in fields, json.items()))

    def __get_homeworld(self, hw_url):

        data = generate_request(hw_url).json()
        data['known_residents_count'] = len(data['residents'])

        data = self.__filter_keys(
            data, ['known_residents_count', 'population', 'name'])
        
        return data

    def __parse_response(self):
        '''Hace un request a la url encontrada dentro,
        no es recursiva, no debe ser llamada por otras funciones que se disparen en la consulta
        '''
        data = self.__filter_keys(self.response.json(), CharacterSerializer.fields)
        data['homeworld'] = self.__get_homeworld(data['homeworld'])
        # Se busca el rating
        data.update(self.__add_average_rating())
        data.update(self.__add_max_rating())

        # Se genera la respuesta final
        self.response = Response(data, status=status.HTTP_200_OK)

    def req(self, char_id):
        '''Se realiza un request con la url seteada, y el body pasado por parametro
        '''
        self.response = self.__get_character(char_id)  # En teoria
        self.__parse_response()
        
        return self.response
