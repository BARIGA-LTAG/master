
import json
import geopandas as gpd
from django.shortcuts import render, redirect
from ..models import Zone_UL,Assainissement,EspaceVert, Lampadaire,Kiosque,Batiment, Limite, Loisir, Paneau, Parking, PlanEau, PointEau, Telecomminication
from pathlib import Path
from django.contrib.gis.geos import GEOSGeometry
from shapely.geometry import Point
from shapely.wkt import loads
import folium
from folium import plugins
import pyproj
from UL.formulaire import AssainissementForm
#Create your views here.

def alerte(request,*args,**kwargs):
    return render(request,"geospatial/alerte.html")
def analyse(request,*args,**kwargs):
    context={}
    return render(request,"geospatial/analyse.html",context)


#CARTOGRAPHIE MAP

kiosques = Kiosque.objects.all()
lampadaires = Lampadaire.objects.all()
panneaux = Paneau.objects.all()
points_eau = PointEau.objects.all()

zones = Zone_UL.objects.all()
geometrie_zone=[loads(zone.geometrie.wkt) for zone in zones]
# Extraire les attributs de chaque zone
zones_attributs = []
for zone in zones:
    zone_attributs = {
        'nom': zone.nom,
        'aire': zone.aire,
        'lon': zone.lon,
        'lat': zone.lat,
        'limite': zone.limite,
        #'geometrie': json.loads(zone.geometrie.geojson)
    }
    zones_attributs.append(zone_attributs)
    
assainissements = Assainissement.objects.all()
# Extraire les geometri de chaque assainissement
geometrie_ass = [loads(ass.geometrie.wkt) for ass in assainissements if ass.geometrie is not None]
ass_atrs = []
for ass in assainissements:
    attributs = {
        'nom': ass.nom,
        'type': ass.type,
        'fonctionnel': ass.fonctionnel,
        'lon': ass.lon,
        'lat': ass.lat,
        'limite': ass.limite,
        'secteur': ass.secteur,
        #'geometrie': json.loads(ass.geometrie.geojson),
    }
    ass_atrs.append(attributs)

def carte(request,*args,**kwargs):
    gdf_zone=gpd.GeoDataFrame(zones_attributs,geometry=geometrie_zone, crs='EPSG:32631')

    
    
    m=gdf_zone.explore(
    column="nom",  # make choropleth based on "POP2010" column
    scheme="naturalbreaks",  # use mapclassify's natural breaks scheme
    legend=True,  # show legend
    k=10,  # use 10 bins
    tooltip=False,  # hide tooltip
    popup=True ,#["POP2010", "POP2000"],  # show popup (on-click)
    legend_kwds=dict(colorbar=False),  # do not use colorbar
    name="zonage",  # name of the layer in the map
    )
          #assainissem
    # gdf_ass=gpd.GeoDataFrame(ass_atrs,geometry=geometrie_ass, crs='EPSG:32631')
    # gdf_ass.explore(
    # m=m,
    # color="black",  # use red color on all points
    # marker_kwds=dict(radius=5, fill=True),  # make marker radius 10px with fill
    # tooltip="nom",  # show "name" column in the tooltip
    # tooltip_kwds=dict(labels=True),  # do not show column label in the tooltip
    # name="assainissement",  # name of the layer in the map
    # )
    # Ajouter une couche de tuiles Google Satellite
 
    folium.TileLayer("CartoDB positron", show=False).add_to(m) 
    
    folium.LayerControl().add_to(m)  # use folium to add layer control

    m  # show map
    carte_html = m._repr_html_()
    context={'carte_html':carte_html}
    return render(request, 'geospatial/carte.html',context)



# path = r"C:\Users\julien\Desktop\geoinformatique\geo_data_science\geopandas_pro\donne\zonage.geojson"
# assain=gpd.read_file(path)
# assain.head()
# def remove_z_dimension(geometry):
#      return Point(geometry.x, geometry.y)

#assain['geometry'] = assain['geometry'].apply(remove_z_dimension)
# for index, row in assain.iterrows():
#     #print(index)
#     ass=Zone_UL(
#        nom=row['Domaines_U'],
#     #     # lat=row['y'],
#     #     # lon=row['x'],
#     #     type=row['type'],
#         geometrie=GEOSGeometry(row['geometry'].wkt,srid=32631),  
#      )
#     ass.save()
# Assainissement.objects.all().delete()