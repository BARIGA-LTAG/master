from django.contrib.gis.db import models
from django.contrib.gis.gdal.libgdal import lgdal
from django.contrib.gis import forms
#from django import forms
from .models import *

# RECHERCHE POLYVALENT A DISTANCE
class geomaprechercheForm(forms.Form):
    query = forms.CharField(label='Recherche', max_length=100)
    lat=forms.FloatField()
    lon=forms.FloatField()


class KiosqueForm(forms.ModelForm):
    class Meta:
        model = Kiosque
        fields = '__all__'  


class Zone_ULForm(forms.ModelForm):
   class Meta:
        model = Zone_UL
        fields = '__all__'  
   
    
class AssainissementForm(forms.ModelForm):
    class Meta:
        model = Assainissement
        fields = ['nom','lat','lon','type', 'fonctionnel', 'secteur', 'precision', 'image', 'zone', 'limite', 'geometrie']
      
   

class LampadaireForm(forms.ModelForm):
     class Meta:
        model = Lampadaire
        fields = '__all__'  
   

class PaneauForm(forms.ModelForm):
     class Meta:
        model = Paneau
        fields = '__all__'  
   
class PointEauForm(forms.ModelForm):
     class Meta:
        model = PointEau
        fields = '__all__'  
   
class ReposoirForm(forms.ModelForm):
    class Meta:
        model = Reposoir
        fields = '__all__'  

class TelecomminicationForm(forms.ModelForm):
    class Meta:
        model = Telecomminication
        fields = '__all__'  
   

class MeteoForm(forms.ModelForm):
     class Meta:
        model = Meteo
        fields = '__all__'  
   
class ArbreIsole(forms.ModelForm):
    class Meta:
        model = ArbreIsole
        fields = '__all__'  
   


class LoisirForm(forms.ModelForm):
    class Meta:
        model = Loisir
        fields = '__all__'  
   
class EspaceVertForm(forms.ModelForm):
     class Meta:
        model = EspaceVert
        fields = '__all__'  
   
class ParkingForm(forms.ModelForm):
   class Meta:
        model = Parking
        fields = '__all__'  
   

class PlanEauForm(forms.ModelForm):
    class Meta:
        model = PlanEau
        fields = '__all__'  
   

class BatimentForm(forms.ModelForm):
    class Meta:
        model = Batiment
        fields = '__all__'  
        widgets = {
            'geometrie': forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}),
        }
 
   
class VoirieForm(forms.ModelForm):
     class Meta:
        model = Voirie
        fields = '__all__'  
   
####################
##############
# LES ALERTES
class AlerteBatimentForm(forms.ModelForm):
    class Meta:
        model=AlerteBatiment
        fields = '__all__'  
class AlerteLampadaireForm(forms.ModelForm):
    class Meta:
        model=AlerteLampadaire
        fields = '__all__'  
class AlertePointEauForm(forms.ModelForm):
    class Meta:
        model=AlertePointEau
        fields = '__all__'  
class AlerteWifiForm(forms.ModelForm):
    class Meta:
        model=AlerteWifi
        fields = '__all__'  
class AlertePoubelleFosseForm(forms.ModelForm):
    class Meta:
        model=AlertePoubelleFosse
        fields = '__all__'   
class AlerteReposoirForm(forms.ModelForm):
    class Meta:
        model=AlerteReposoir
        fields = '__all__'  

class AlerteJardinForm(forms.ModelForm):
    class Meta:
        model=AlerteJardin
        fields = '__all__' 
       
class AlerteGeneraleForm(forms.ModelForm):
    class Meta:
        model=AlerteGenerale
        fields = '__all__'  
##########################

