from UL.views.geoviews import  carte, analyse,analyse_1,analyse_2
from UL.views.formsviews import formassainisement,collecteur, formbatiment,faire_alerte
from UL.views.basicviews import statistique,geomaprecherche,telecharger_donnees,telecharger_data,telecharger_data_geojson,telecharger_data_gpkg
from django.contrib import admin
from django.urls import path
app_name='UL'
urlpatterns = [
    path('georecherche/', geomaprecherche, name='map'),
    path('alerte/', faire_alerte, name="alerte"), 
    path('analyse/', analyse, name="analyse"), 
    path('analyse_py/', analyse_1, name="analyse1"), 
    path('analyse_js/', analyse_2, name="analyse2"), 
    path('statistique/', statistique, name="statistique"), 
    path('carte/', carte, name="carte"),  
    path('collecte/',collecteur, name="collecte"),
    path('collecte_assainis/',formassainisement, name="assainis"),
    path('collecte_bat/',formbatiment, name="batiment"),
    path('telecharger/',telecharger_donnees, name='telecharger'),
    path('telecharger_csv/', telecharger_data, name='telecharger_csv'),
    path('telecharger_json/', telecharger_data_geojson, name='telecharger_json'),
    path('telecharger_gpkg/', telecharger_data_gpkg, name='telecharger_gpkg'),

  ]

