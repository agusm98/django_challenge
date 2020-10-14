from django.db import models

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    character_id = models.IntegerField() #Deberia ser una foreign key al modelo Character/People
    rate = models.IntegerField()

    def __str__(self):
        return f'rate: {self.rate}'