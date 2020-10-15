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

class ApiConnCharacter():

    URL = str()
    response = Response()
    data = dict()
    ratings = list()

    def __init__(self):
        """inicializa el objeto seteando la URL
        Deberia estar parametrizada por si cambia la url.
        """

        self.URL = 'http://swapi.dev/api/people/'

    @staticmethod
    def __filter_keys(json, fields):
        '''Se filtran el diccionario json, armando un nuevo diccionario solo con los campos necesarios'''

        return dict(filter(lambda x: x[0] in fields, json.items()))

    def __get_character(self, char_id):
        '''Se consume la api de personajes segun char_id'''

        self.response = generate_request(self.URL+char_id)
    
    def set_ratings(self, char_id):
        """Obtiene las calificaciones del personaje y se setea
        """

        db = Database()
        self.ratings = db.get_rates(char_id)

    def __add_average_rating(self):
        """Realiza un promedio de los ratings y se agrega el campo average_rating 
        """

        avg = (sum(self.ratings)/len(self.ratings))\
            if self.ratings\
                else 0
        
        self.data['average_rating'] = avg

    def __add_max_rating(self):
        """Obtiene el maximo rating y se agrega el campo max_rating
        """

        self.data['max_rating'] = max(self.ratings, default=0)

    def __get_homeworld(self, hw_key):
        """Se obtiene la direccion del campo con el mismo nombre del parametro hw_key.
        Para luego obtener informacion del mundo natal y reemplazar el campo en el json.
        Agregando los campos que nos interesan de dicho mundo natal
        """

        hw_dict = generate_request(self.data[hw_key]).json()
        hw_dict['known_residents_count'] = len(hw_dict['residents'])

        hw_dict = self.__filter_keys(
            hw_dict, ['known_residents_count', 'population', 'name'])
        
        self.data[hw_key] = hw_dict
    
    def __get_species_name(self, species):
        """Se obtiene la direccion del campo con el mismo nombre del parametro species.
        Para luego obtener informacion de la especie.
        Este metodo es destructivo, elimina el campo indicado en el parametro.
        Luego agrega el campo species_name en la data del personaje.
        """

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
        '''Aqui se haran la llamada a los methodos
        que modificaran la instancia json del personaje consultado,
        se filtraran los campos y luego se añadiran o modificaran campos al json
        '''
        
        self.data = self.__filter_keys(self.response.json(), CharacterSerializer.fields)
        
        self.__get_homeworld('homeworld')
        
        self.__get_species_name('species')

        self.__add_average_rating()
        
        self.__add_max_rating()
    
    def make_response(self, char_id):
        """Retorna un objeto response,
        En caso de no existir el id de personaje devolvera un error,
        caso contrario utilizara modificara la data del personaje.
        """
        if self.response.status_code == 200:
            self.set_ratings(char_id)
            self.__parse_response()
            return Response(self.data, status=status.HTTP_200_OK)
        
        elif self.response.status_code == 400:
            return Response(self.response.json(), status=status.HTTP_400_BAD_REQUEST)

    def req(self, char_id):
        '''Se realiza un request con la url seteada, y el body pasado por parametro
        '''
        self.__get_character(char_id)

        self.response = self.make_response(char_id)
        
        return self.response
