from django.db import models

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    character_id = models.IntegerField() #Deberia ser una foreign key al modelo Character/People
    character_name = models.CharField(max_length=100)
    rate = models.IntegerField()

'''class Character(models.Model):
    fields = ('', '', '', '', '', '', '')
    name = None
    height = None
    mass = None
    hair_color = None
    skin_color = None
    eye_color = None
    birth_year = None
    gender = None
    homeworld = 
'''
