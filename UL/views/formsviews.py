from json import loads
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from UL.formulaire import AlerteGeneraleForm, AlerteJardinForm, AlerteLampadaireForm, AlertePointEauForm, AlertePoubelleFosseForm, AlerteReposoirForm, AlerteWifiForm, AssainissementForm, BatimentForm,AlerteBatimentForm
from django.contrib.gis.geos import GEOSGeometry
from shapely.geometry import Point
import geopandas as gpd
from ..models import Zone

## POUR LES ALERTE
@login_required(login_url='connection')
def faire_alerte(request, *args, **kwargs):
    if request.method == 'POST':
        if 'submit_form1' in request.POST:
            form1 = AlerteBatimentForm(request.POST)
            if form1.is_valid():
                form1.instance.auteur = request.user.profile 
                form1.save()
                form1 = AlerteBatimentForm()
        else:
            form1 = AlerteBatimentForm()

        #formulaires alerlamp
        if 'submit_form2' in request.POST:
            form2 = AlerteLampadaireForm(request.POST)
            if form2.is_valid():
                form2.instance.auteur = request.user.profile 
                form2.save()
                form2 = AlerteLampadaireForm()
        else:
            form2 = AlerteLampadaireForm()
        #  formulaires point eau
        if 'submit_form3' in request.POST:
            form3 = AlertePointEauForm(request.POST)
            if form3.is_valid():
                form3.instance.auteur = request.user.profile 
                form3.save()
                form3 = AlertePointEauForm()
        else:
            form3 = AlertePointEauForm()
        
        #formulaires alerWIFI
        if 'submit_form4' in request.POST:
            form4 = AlerteWifiForm(request.POST)
            if form4.is_valid():
                form4.instance.auteur = request.user.profile 
                form4.save()
                form4 = AlerteWifiForm()
        else:
            form4 = AlerteWifiForm()
        #formulaires alerPUISARD
        if 'submit_form5' in request.POST:
            form5 = AlertePoubelleFosseForm(request.POST or None)
            if form5.is_valid():
                form5.instance.auteur = request.user.profile 
                form5.save()
                form5 = AlertePoubelleFosseForm()
        else:
            form5 = AlertePoubelleFosseForm()
        #formulaires alerREPOS
        if 'submit_form6' in request.POST:
            form6 = AlerteReposoirForm(request.POST)
            if form6.is_valid():
                form6.instance.auteur = request.user.profile 
                form6.save()
                form6 = AlerteReposoirForm()
        else:
            form6 = AlerteReposoirForm()
        #formulaires alerJARDIN
        if 'submit_form7' in request.POST:
            form7 = AlerteJardinForm(request.POST)
            if form7.is_valid():
                form7.instance.auteur = request.user.profile 
                form7.save()
                form7 = AlerteJardinForm()
        else:
            form7 = AlerteJardinForm()
        #formulaires alerGENERAL
        if 'submit_form8' in request.POST:
            form8 = AlerteGeneraleForm(request.POST)
            if form8.is_valid():
                form8.instance.auteur = request.user.profile 
                form8.save()
                form8 = AlerteGeneraleForm()
        else:
            form8 = AlerteGeneraleForm()

    else:
        # Initialisation A zero
        form1 = AlerteBatimentForm()
        form2 = AlerteLampadaireForm()
        form3 = AlertePointEauForm()
        form4 = AlerteWifiForm()
        form5 = AlertePoubelleFosseForm()
        form6 = AlerteReposoirForm()
        form7 = AlerteJardinForm()
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
@login_required(login_url='connection')
def collecteur(request,*args,**kwargs):
    return render(request, 'geospatial/collecte.html')

zones = Zone.objects.all()
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

    context={'form': form}
    return render(request, 'infra/assainis.html', context)


def formbatiment(request,*args,**kwargs):
    if request.method == 'POST':
        form = BatimentForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = BatimentForm()
    return render(request, 'infra/batiment.html',{'form':form})


