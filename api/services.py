import requests
from rest_framework.response import Response
from rest_framework import status
from .serializers import CharacterSerializer
from .models import Rating

def generate_request(url, **kw):
    resp = requests.get(url, params=kw)
    return resp

class Database():

    def insert_rate(self, id, rate):
        session = Rating(character_id=id, rate=rate)
        session.save()

    def get_rates(self, id):
        session = Rating.objects.filter(character_id=id)
        return [s_obj.rate for s_obj in session]

class ApiCharacter():

    URL = str()
    response = Response()
    data = dict()
    ratings = list()

    def __init__(self):
        self.URL = 'http://swapi.dev/api/people/'

    @staticmethod
    def __filter_keys(json, fields):
        '''Se filtran el diccionario json, armando un nuevo diccionario solo con los campos necesarios'''

        return dict(filter(lambda x: x[0] in fields, json.items()))

    def __get_character(self, char_id):
        '''Se consume la api de personajes segun id personaje'''
        self.response = generate_request(self.URL+char_id)
    
    def set_ratings(self, char_id):
        db = Database()
        self.ratings = db.get_rates(char_id)

    def __add_average_rating(self):
        
        avg = (sum(self.ratings)/len(self.ratings))\
            if self.ratings\
                else 0
        
        self.data['average_rating'] = avg

    def __add_max_rating(self):
        self.data['max_rating'] = max(self.ratings, default=0)

    def __get_homeworld(self, hw_key):

        hw_dict = generate_request(self.data[hw_key]).json()
        hw_dict['known_residents_count'] = len(hw_dict['residents'])

        hw_dict = self.__filter_keys(
            hw_dict, ['known_residents_count', 'population', 'name'])
        
        self.data[hw_key] = hw_dict
    
    def __get_species_name(self, species):
        
        list_sp = self.data.pop(species)
        
        if list_sp: 
            
            resp = generate_request(list_sp[0])

            if resp.status_code == 200:

                self.data['species_name'] = resp.json()['name']
            
            else:
                self.data['species_name'] = "Error getting species"
        
        else:
            self.data['species_name'] = "Not Defined"


    def __parse_response(self):
        '''Hace un request a la url encontrada dentro,
        no es recursiva, no debe ser llamada por otras funciones que se disparen en la consulta
        '''
        
        self.data = self.__filter_keys(self.response.json(), CharacterSerializer.fields)
        
        self.__get_homeworld('homeworld')
        
        self.__get_species_name('species')

        self.__add_average_rating()
        
        self.__add_max_rating()
    
    def make_response(self):
        
        if self.response.status_code == 200:
            self.__parse_response()
            return Response(self.data, status=status.HTTP_200_OK)
        
        elif self.response.status_code == 400:
            return Response(self.response.json(), status=status.HTTP_400_BAD_REQUEST)

    def req(self, char_id):
        '''Se realiza un request con la url seteada, y el body pasado por parametro
        '''
        self.__get_character(char_id)

        self.set_ratings(char_id)
        
        self.response = self.make_response()
        
        return self.response
