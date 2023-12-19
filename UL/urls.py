from UL.views.geoviews import  carte, analyse
from UL.views.formsviews import formassainisement,collecteur, formbatiment,faire_alerte
from UL.views.basicviews import statistique,geomaprecherche, telecharger_donnees,telecharger_geopackage
from django.contrib import admin
from django.urls import path
app_name='UL'
urlpatterns = [
    path('georecherche/', geomaprecherche, name='map'),
    path('alerte/', faire_alerte, name="alerte"), 
    # path('map/',map, name="map"), 
    path('analyse/', analyse, name="analyse"), 
    path('statistique/', statistique, name="statistique"), 
    path('carte/', carte, name="carte"),  
    path('collecte/',collecteur, name="collecte"),
    path('collecte_assainis/',formassainisement, name="assainis"),
    path('collecte_bat/',formbatiment, name="batiment"),
    # path('telecharger_data/',telecharger_donnees, name='telecharger'),
    path('telecharger-geojson/', telecharger_geopackage, name='telecharger'),
    

  ]

