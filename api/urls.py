from django.urls import include, path
from rest_framework import routers
from .views import CharacterViewSet, RatingViewSet

#Enrutamiento
urlpatterns = [
    path('character/<id>/', CharacterViewSet.as_view({'get':'get'})),
    path('character/<id>/rating/', RatingViewSet.as_view({'post':'post'})),
]


