import os
from shapely.wkt import loads
import json
from django.shortcuts import render
from ..formulaire import geomaprechercheForm
from ..models import *  
from geopy.distance import geodesic
from django.http import FileResponse
import geopandas as gpd
import csv,pandas
from django.http import HttpResponse
#A.objects.all().update(lat=None, lon=None)

# fonction pour la rechere de tous les infrastricture
def geomaprecherche(request):
    if 'query' in request.GET:
        query = request.GET['query']
        #recuperer la position de l'utilisateur
        user_lat = float(request.GET['lat'])
        user_lon = float(request.GET['lon'])
        #obtenir les resultats
        #results1 = Zone_UL.objects.filter(nom__icontains=query)
        results2 = Assainissement.objects.filter(nom__icontains=query)
        results3 = Kiosque.objects.filter(nom__icontains=query)

        # Calcul des distances
        # trier les resultats par la distance refer utilisateur
        #results1 = sorted(results1, key=lambda x: geodesic((user_lat, user_lon), (x.lat, x.lon)).m)
        results2 = sorted(results2, key=lambda x: geodesic((user_lat, user_lon), (x.lat, x.lon)).m)
        results3 = sorted(results3, key=lambda x: geodesic((user_lat, user_lon), (x.lat, x.lon)).m)
        
    else:
        results1 = results2 = results3 = []

    form = geomaprechercheForm()

    context = {
        'form': form,
        # 'results1': results1,
        'results2': results2,
        'results3': results3,
    }
    return render(request, 'geospatial/map.html', context)
### telecharger les donneees

#APPEL DES CLASS
zones = Zone_UL.objects.all()

#STATISTIQUE
### statistique

def statistique(request,*args,**kwargs):
    return render(request,"geospatial/statistique.html")

def telecharger_donnees(request,*args,**kwargs):
    return render(request,"geospatial/donnee.html")

def telecharger_data(request):
    geometrie_zone = [loads(zone.geometrie.wkt) for zone in zones]
    les_zones = []
    for zone in zones:
        if zone.geometrie and zone.geometrie.geojson:
            geometrie = json.loads(zone.geometrie.geojson)
        else:
            geometrie = None
    
        une_zone = {
            'nom': zone.nom,
            'aire': zone.aire,
            'lon': zone.lon,
            'lat': zone.lat,
            'limite': zone.limite,
            # 'geometrie': geometrie
        }
        les_zones.append(une_zone)

    # Créer un GeoDataFrame à partir de la liste de dictionnaires
    gdf = gpd.GeoDataFrame(les_zones, geometry=geometrie_zone, crs='EPSG:32631')

    # Enregistrez le GeoDataFrame au format GeoPackage
    module_directory = os.path.dirname(__file__)
    csv_path = os.path.join(module_directory, '..', 'static', 'gis', 'zone_ul.csv')

    # Enregistrez le GeoDataFrame au format CSV
    gdf.to_csv(csv_path, index=False,encoding='latin')

    response = FileResponse(open(csv_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename=zone_ul.csv'

    return response
def telecharger_data_geojson(request):
    geometrie_zone = [loads(zone.geometrie.wkt) for zone in zones]
    les_zones = []
    for zone in zones:
        if zone.geometrie and zone.geometrie.geojson:
            geometrie = json.loads(zone.geometrie.geojson)
        else:
            geometrie = None
    
        une_zone = {
            'nom': zone.nom,
            'aire': zone.aire,
            'lon': zone.lon,
            'lat': zone.lat,
            'limite': zone.limite,
            # 'geometrie': geometrie
        }
        les_zones.append(une_zone)

    # Créer un GeoDataFrame à partir de la liste de dictionnaires
    gdf = gpd.GeoDataFrame(les_zones, geometry=geometrie_zone, crs='EPSG:32631')
    # Supposons que votre GeoDataFrame soit stocké dans la variable gdf
    type_index = type(gdf.index)
    print(f"Type d'index : {type_index}")
    print(gdf.index)

    # Enregistrez le GeoDataFrame au format GeoJSON
    module_directory = os.path.dirname(__file__)
    geojson_path = os.path.join(module_directory, '..', 'static', 'gis', 'zone_ul.geojson')
    gdf.to_file(geojson_path, driver='GeoJSON', index='ignore')

    response = FileResponse(open(geojson_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename=zone_ul.geojson'

    return response

def telecharger_data_gpkg(request):
    geometrie_zone = [loads(zone.geometrie.wkt) for zone in zones]
    les_zones = []
    for zone in zones:
        if zone.geometrie and zone.geometrie.geojson:
            geometrie = json.loads(zone.geometrie.geojson)
        else:
            geometrie = None
    
        une_zone = {
            'nom': zone.nom,
            'aire': zone.aire,
            'lon': zone.lon,
            'lat': zone.lat,
            'limite': zone.limite,
            # 'geometrie': geometrie
        }
        les_zones.append(une_zone)

    # Créer un GeoDataFrame à partir de la liste de dictionnaires
    gdf = gpd.GeoDataFrame(les_zones, geometry=geometrie_zone, crs='EPSG:32631')
    # Enregistrez le GeoDataFrame au format GeoJSON
    module_directory = os.path.dirname(__file__)
    gpkg_path = os.path.join(module_directory, '..', 'static', 'gis', 'zone_ul.gpkg')
    gdf.to_file(gpkg_path, driver='GPKG', index='ignore')

    response = FileResponse(open(gpkg_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename=zone_ul.gpkg'

    return response
