
import json
import geopandas as gpd
from django.shortcuts import render, redirect
from ..models import Zone_UL,Assainissement,EspaceVert, Lampadaire,Kiosque,Batiment, Limite, Loisir, Paneau, Parking, PlanEau, PointEau, Telecomminication
from django.contrib.gis.geos import GEOSGeometry
from shapely.geometry import Point
from shapely.wkt import loads
import folium
from folium import plugins
#Create your views here.

def alerte(request,*args,**kwargs):
    return render(request,"geospatial/alerte.html")

#CARTOGRAPHIE MAP
kiosques = Kiosque.objects.all()
lampadaires = Lampadaire.objects.all()
panneaux = Paneau.objects.all()
#POUR POINT EAU
points_eau = PointEau.objects.all()
geom_pt_eau=[loads(pt_eau.geometrie.wkt)for pt_eau in points_eau]
atrs_pt_eau=[]
for atr_pt_eau in points_eau:
    pt_o={
        'nom':atr_pt_eau.nom,
        'latitude':atr_pt_eau.lat,
        'longitude':atr_pt_eau.lon,
        'type':atr_pt_eau.type,
        'fonctionnel':atr_pt_eau.fonctionnel,
        'secteur':atr_pt_eau.secteur,
        'image':atr_pt_eau.image.url if atr_pt_eau.image else None,
        'date_creation':atr_pt_eau.date_creation.strftime("%Y-%m-%d") if atr_pt_eau.date_creation else None,
        'zone':atr_pt_eau.zone.nom if atr_pt_eau.zone else None,
        'zone':atr_pt_eau.zone.nom if atr_pt_eau.zone else None,
        'date_collecte':atr_pt_eau.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if atr_pt_eau.date_collecte else None,
        'agent_collecteur':atr_pt_eau.agent_collecteur,
        'situé dans':atr_pt_eau.espace_vert.nom if atr_pt_eau.espace_vert else None,
        'au environ de':atr_pt_eau.batiment.batiment if atr_pt_eau.batiment else None,
        'info_modifier_le':atr_pt_eau.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if atr_pt_eau.info_modifier_le else None,
    }
    atrs_pt_eau.append(pt_o)
gdf_pt_eau=gpd.GeoDataFrame(atrs_pt_eau,geometry=geom_pt_eau, crs='EPSG:32631')
### POUR ZONE UL
zones = Zone_UL.objects.all()
geometrie_zone=[loads(zone.geometrie.wkt) for zone in zones]
# Extraire les attributs de chaque zone
zones_attributs = []
for zone in zones:
    zone_attributs = {
        'nom': zone.nom,
        'aire en m²': zone.aire,
        'longitude': zone.lon,
        'latitude': zone.lat,
    }
    zones_attributs.append(zone_attributs)
gdf_zone=gpd.GeoDataFrame(zones_attributs,geometry=geometrie_zone, crs='EPSG:32631') 

##POUR ASSAINISSEMENT
assainissements = Assainissement.objects.all()
# Extraire les geometri de chaque assainissement
geometrie_ass = [loads(ass.geometrie.wkt) for ass in assainissements if ass.geometrie is not None]
ass_atrs = []
for ass in assainissements:
    attributs = {
        'nom':ass.nom,
        'latitude':ass.lat,
        'longitude':ass.lon,
        'type':ass.type,
        'fonctionnel':ass.fonctionnel,
        'secteur':ass.secteur,
        'image':ass.image.url if ass.image else None,
        'date_creation':ass.date_creation.strftime("%Y-%m-%d") if ass.date_creation else None,
        'zone':ass.zone.nom if ass.zone else None,
        'date_collecte':ass.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if ass.date_collecte else None,
        'agent_collecteur':ass.agent_collecteur,
        'info_modifier_le':ass.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if ass.info_modifier_le else None,
    }
    ass_atrs.append(attributs)
gdf_ass=gpd.GeoDataFrame(ass_atrs,geometry=geometrie_ass, crs='EPSG:32631')
#vue pur care d'occupation du sol
def carte(request, *args, **kwargs):
    m = gdf_zone.explore(
        column="nom",
        scheme="naturalbreaks",
        legend=True,
        k=10,
        tooltip=False,
        popup=True,
        legend_kwds=dict(colorbar=False),
        name="zonage",
    )

    # Assainissem
    gdf_ass.explore(
        m=m,
        color="black",
        marker_kwds=dict(radius=5, fill=True),
        tooltip="nom",
        tooltip_kwds=dict(labels=True),
        popup=True,
        name="assainissement",
    )
    #Point eau
    gdf_pt_eau.explore(
        m=m,
        color="green",
        marker_kwds=dict(radius=5, fill=True),
        tooltip="nom",
        tooltip_kwds=dict(labels=True),
        popup=True,
        name="robinet d'eau",
    )

    # Ajouter une couche de tuiles Google Satellite
    folium.TileLayer("CartoDB positron", show=False).add_to(m)
    folium.LayerControl().add_to(m)  # use folium to add layer control

    carte_html = m._repr_html_()
    context = {'carte_html': carte_html}
    return render(request, 'geospatial/carte.html', context)

#FAIRE DES ANALYSE SPATIAL AU COMPLET
def analyse(request,*args,**kwargs):
    m=gdf_zone.explore(
    column="nom",  
    scheme="naturalbreaks",  
    legend=True,  
    k=10,  
    tooltip=False,  
    popup=True ,
    legend_kwds=dict(colorbar=False),  
    name="zonage",  
    )
          #assainissem
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
    analyse_html = m._repr_html_()
    context={'analyse_html':analyse_html}
    return render(request,"geospatial/analyse.html",context)

path = r"C:\Users\julien\Desktop\geoinformatique\geo_data_science\geopandas_pro\donne\ASSAINIS.geojson"
assain= gpd.read_file(path)
#assain.head()
def remove_z_dimension(geometry):
     return Point(geometry.x, geometry.y)

assain['geometry'] = assain['geometry'].apply(remove_z_dimension)
# for index, row in assain.iterrows():
#     #print(row)
#     ass=Assainissement(
#        nom=row['assainissement'],
#         # lat=row['y'],
#         # lon=row['x'],
#         type=row['type'],
#         geometrie=GEOSGeometry(row['geometry'].wkt,srid=32631),  
#      )
   # ass.save()
#### Assainissement.objects.all().delete()