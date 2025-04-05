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
        model = Zone
        fields = '__all__'  
   
    
class AssainissementForm(forms.ModelForm):
    class Meta:
        model = Poubelle
        fields = ['nom','latitude','longitude', 'fonctionnel', 'secteur', 'image', 'zone', 'limite']
      
   

class LampadaireForm(forms.ModelForm):
     class Meta:
        model = Eclairage
        fields = '__all__'  
   

class PaneauForm(forms.ModelForm):
     class Meta:
        model = Panneau
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
        model = Telecommunication
        fields = '__all__'  
   

class MeteoForm(forms.ModelForm):
     class Meta:
        model = StationMeteo
        fields = '__all__'  
   
class ArbreIsole(forms.ModelForm):
    class Meta:
        model = ArbreIsole
        fields = '__all__'  
   
class LoisirForm(forms.ModelForm):
    class Meta:
        model = AireLoisir
        fields = '__all__'  
   
class EspaceVertForm(forms.ModelForm):
     class Meta:
        model = TrameVerte
        fields = '__all__'  
   
class ParkingForm(forms.ModelForm):
   class Meta:
        model = AireStationnement
        fields = '__all__'  
   

class PlanEauForm(forms.ModelForm):
    class Meta:
        model = BassinEau
        fields = '__all__'  
   

class BatimentForm(forms.ModelForm):
    class Meta:
        model = Batis
        fields = '__all__'  
       # exclude =['geometrie','aire']
        
   
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
        fields = ['disfonction','lesPennes' , 'SOSMessage', 'batiment']
class AlerteLampadaireForm(forms.ModelForm):
    class Meta:
        model=AlerteLampadaire
        fields = ['disfonction', 'SOSMessage', 'lampadaire'] 
class AlertePointEauForm(forms.ModelForm):
    class Meta:
        model=AlertePointEau
        fields = ['disfonction', 'SOSMessage', 'point_eau'] 
class AlerteWifiForm(forms.ModelForm):
    class Meta:
        model=AlerteWifi
        fields = ['disfonction', 'SOSMessage', 'wifi']
class AlertePoubelleFosseForm(forms.ModelForm):
    class Meta:
        model=AlertePoubelle
        fields = ['disfonction', 'SOSMessage', 'poubelle']
class AlerteReposoirForm(forms.ModelForm):
    class Meta:
        model=AlerteReposoir
        fields = ['disfonction', 'SOSMessage', 'repos']

class AlerteJardinForm(forms.ModelForm):
    class Meta:
        model=AlerteJardin
        fields = ['disfonction', 'SOSMessage', 'verdure']
       
class AlerteGeneraleForm(forms.ModelForm):
    class Meta:
        model=AlerteGenerale
        fields = ['disfonction', 'SOSMessage']
##########################

