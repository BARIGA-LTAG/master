from json import loads
import json
from django.http import JsonResponse
from django.shortcuts import render
import pyproj
from UL.formulaire import AlerteGeneraleForm, AlerteJardinForm, AlerteLampadaireForm, AlertePointEauForm, AlertePoubelleFosseForm, AlerteReposoirForm, AlerteWifiForm, AssainissementForm, BatimentForm,AlerteBatimentForm
from django.contrib.gis.geos import GEOSGeometry
from shapely.geometry import Point
import geopandas as gpd
from ..models import Zone_UL

## POUR LES ALERTE 
def faire_alerte(request, *args, **kwargs):
    form1 = AlerteBatimentForm(request.POST or None)
    form2 = AlerteLampadaireForm(request.POST or None)
    form3 = AlertePointEauForm(request.POST or None)
    form4 = AlerteWifiForm(request.POST or None)
    form5 = AlertePoubelleFosseForm(request.POST or None)
    form6 = AlerteReposoirForm(request.POST or None)
    form7 = AlerteJardinForm(request.POST or None)
    form8 = AlerteGeneraleForm(request.POST or None)
    
    if request.method == 'POST':
        if 'submit_form1' in request.POST and form1.is_valid():
            form1.save()
            form1 = AlerteBatimentForm()
        elif 'submit_form2' in request.POST and form2.is_valid():
            form2.save()
            form2 = AlerteLampadaireForm()
        elif 'submit_form3' in request.POST and form3.is_valid():
            form3.save()
            form3 = AlertePointEauForm()
        elif 'submit_form4' in request.POST and form4.is_valid():
            form4.save()
            form4 = AlerteWifiForm()
        elif 'submit_form5' in request.POST and form5.is_valid():
            form5.save()
            form5 = AlertePoubelleFosseForm()
        elif 'submit_form6' in request.POST and form6.is_valid():
            form6.save()
            form6 = AlerteReposoirForm()
        elif 'submit_form7' in request.POST and form7.is_valid():
            form7.save()
            form7 = AlerteJardinForm()
        elif 'submit_form8' in request.POST and form8.is_valid():
            form8.save()
            form8 = AlerteGeneraleForm()

    context = {
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        'form5': form5,
        'form6': form6,
        'form7': form7,
        'form8': form8,
    }
    return render(request, 'geospatial/alerte.html', context)


## collerter
def collecteur(request,*args,**kwargs):
    return render(request, 'geospatial/collecte.html')

zones = Zone_UL.objects.all()
def convert_geometry_to_4326(geometry):
    # Convertir la géométrie en EPSG:4326
    geometry.transform(4326)
    return geometry

def formassainisement(request,*args,**kwargs):
    form=AssainissementForm()
    if request.method=='POST':
        form = AssainissementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = AssainissementForm()
    else:
        form = AssainissementForm()
 
    zones_geojson = []

    for zone in zones:
        # Convertir la géométrie en EPSG:4326
        geometry_4326 = convert_geometry_to_4326(zone.geometrie)
        #geom_4326 = zone.geometrie.transform(4326, clone=True)
        # Convertir la géométrie en GeoJSON
        champs = {
            "geometrie": json.loads(geometry_4326.geojson),
            "nom": zone.nom,
            "aire": zone.aire,}
        zones_geojson.append(champs)

    zones_geojson = json.dumps(zones_geojson)

    context={'form': form,'zones_geojson':zones_geojson}
    return render(request, 'infra/assainis.html', context)


def formbatiment(request,*args,**kwargs):
    if request.method == 'POST':
        form = BatimentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = BatimentForm()
    return render(request, 'infra/batiment.html',{'form':form})

