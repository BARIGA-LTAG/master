from shapely.wkt import loads
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from django.shortcuts import render
from ..formulaire import geomaprechercheForm
from ..models import *  
from geopy.distance import geodesic
from django.http import FileResponse
import geopandas as gpd
import csv
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


def telecharger_donnees(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="zones.csv"'

    writer = csv.writer(response)
    writer.writerow(['nom', 'aire', 'superficie', 'lon', 'lat', 'limite'])

    zones = Zone_UL.objects.all()
    for zone in zones:
        writer.writerow([zone.nom, zone.aire, zone.superficie, zone.lon, zone.lat, zone.limite])

    return response


#STATISTIQUE
### statistique
def statistique(request,*args,**kwargs):
    df_zones = pd.DataFrame(list(zones.values()))
    sns.scatterplot(data=df_zones, x='nom', y='aire')
    plt.show()
    return render(request,"geospatial/statistique.html")

#TELECHARGER MULTIFORMA
# Créer une liste de dictionnaires avec les attributs et la géométrie au format GeoJSON
zones = Zone_UL.objects.all()
# 
def telecharger_excel(request): ################# VALIDE
    # Créez un DataFrame avec les attributs
    df = pd.DataFrame(list(zones.values()))

    # Créez un fichier Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="zones.xlsx"'
    df.to_excel(response, index=False)

    return response

# def telecharger_geopackage(request):
#     zones = Zone_UL.objects.all()
#     gdf = gpd.GeoDataFrame(zones, geometry=geometrie, crs='EPSG:32631')

#     response = HttpResponse(content_type='application/geopackage')
#     response['Content-Disposition'] = 'attachment; filename="zones.gpkg"'
#     gdf.to_file(response, layer='zones', driver='GPKG')

#     return response

def telecharger_geopackage(request):
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
            'superficie': zone.superficie,
            'lon': zone.lon,
            'lat': zone.lat,
            'limite': zone.limite,
            'geometrie': geometrie
        }
        les_zones.append(une_zone)

    # Créer un GeoDataFrame à partir de la liste de dictionnaires
    gdf = gpd.GeoDataFrame(les_zones, geometry=geometrie_zone, crs='EPSG:32631')

    # Enregistrez le GeoDataFrame au format GeoPackage
    gdf.to_file('zone_ul.gpkg', driver='GPKG')

    # Servez le fichier comme réponse
    with open('zone_ul.gpkg', 'rb') as file:
        response = FileResponse(file)
        response['Content-Disposition'] = 'attachment; filename=zone_ul.gpkg'
        print(response.content)
        return response
