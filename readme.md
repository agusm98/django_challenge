Django_challenge Swapi

Esta aplicacion consiste en recolectar datos de personajes de Stars Wars
Para esto consume un servicio y obtiene una informacion consistente.

La aplicacion cuenta tambien con dockerizacion, con tal de que pueda correr en otras plataformas

*Importante: Debido a un cambio de linux en el medio de desarrollo, es problable que el archivo docker-compose.yml haya que cambiarle su version, actualmente: 3.3*

Para contruir la imagen de esta api debe utilizarse el siguiente commando:

sudo docker-compose build

Luego se puede iniciarla

sudo docker-compose up

Notese que el puerto utilizado es el "8000"

La ruta de la aplicacion para consumir es: 'http://127.0.0.1:8000'

Por ahora solo se incluyen los siguientes endpoints:

1.GET /character/<id>/
2.POST /character/<id>/rating/

En el cual en el endpoint 1 podemos obtener los siguientes campos de informacion segun el id de personaje:

'name': text
'height': text
'mass': text
'hair_color': text
'skin_color': text
'eye_color': text
'birth_year': text
'gender': text
'homeworld': *dict con los sig campos.*
    'name': text
    'population': text
    'known_residents_count': int
'species': text

Para el segundo endpoint podremos calificar distintos personajes dependiendo el id.
Debemos incluir un body para esto:

{
    "rate": int [1 : 5]
}

Tener en cuenta que un rate distinto del rango mencionado devolvera el error http 406

Services.py:
Se cuenta con un modulo el cual se encargara de colectar la data, tanto sea la clase "Database" que maneja algunos metodos de la base de datos:

insert_rate: Inserta en la tabla "api_rating" una nueva calificacion al id de personaje proporcionado

get_rates: Devuelve una lista de calificaciones del id de personaje proporcionado.

ApiConnCharacter: Clase que se encarga de obtener la info del personaje, pasandole el id al metodo req() puede obtenerse la info del personaje, se utiliza un parseo y algunos requests para completar la data:

__init__: inicializa el objeto seteando la URL (deberia estar parametrizada por si cambia la url)

__filter_keys: Filtra un diccionario (json) dejando solo las keys necesarias a devolver, se utiliza el parametro fields para el filtro.

__get_character: obtiene en primera instancia el json con todos los campos que proporciona la api de Swapi

set_ratings: obtiene y setea las calificaciones en el atributo del objeto "ratings" para poder ser utilizado en distintos metodos del objeto

*los methodos privados add modifican la data del personaje traido en primera instancia*

__add_average_rating: utiliza el atributo "ratings" para obtener un promedio de estos y agregarlo al json del personaje, con el nombre de campo 'average_rating'

__add_max_rating: utiliza el atributo "ratings" para obtener el maximo de estos y agregarlo al json del personaje, con el nombre de campo 'max_rating'

__get_homeworld: utiliza la direccion url de campo pasado por parametro para obtener los datos del mundo natal

__get_species_name: utiliza la direccion url de campo pasado por parametro para obtener los datos de especie del personaje. A tener en cuenta: Swapi esta trayendo este campo vacio en la mayoria de los casos, se tuvo esto en cuenta para devolver un "Not Defined"
En caso de que no exista la especie a la que referencia la url, se completa el campo con un string que indica esto.

__parse_response: Aqui se haran la llamada a los methodos que modificaran la instancia json del personaje consultado, se filtraran los campos, se asignara un diccionario a modificar al atributo "data" y luego se añadiran o modificaran campos de este.

make_response: Retorna un objeto response, en donde en caso de no existir el id de personaje devolvera un error, caso contrario utilizara la data modificada por el objeto y se le asignara al objeto response a devolver.

req: se encarga de realizar las llamadas necesarias para devolver un objeto response relacionado al id del personaje pasado por el parametro "char_id"
