# from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.contrib.gis import admin
from .models import *
#########################################
admin.site.site_title = ("MON-CAMPUS")
admin.site.site_header = ("MON-CAMPUS")
admin.site.index_title = ("MON-CAMPUS")
class AdminZoneGis(GISModelAdmin):
    list_display =('nom','aire','lat','lon','geometrie')
admin.site.register(Zone_UL, AdminZoneGis)

class LimiteGis(GISModelAdmin):
    list_display =('nom','aire','lat','lon','geometrie')
admin.site.register(Limite, LimiteGis)

class AssainissementGIS(GISModelAdmin):
    list_display=('nom','lat','lon','type','fonctionnel','secteur','date_creation','geometrie')
admin.site.register(Assainissement,AssainissementGIS)

class KiosqueGIS(GISModelAdmin):
    list_display=('nom','lat','lon','usage','fonctionnel','secteur','date_creation','geometrie')
admin.site.register(Kiosque,KiosqueGIS)

class LampadaireGIS(GISModelAdmin):
    list_display=('nom','lat','lon','type','energie','fonctionnel','secteur','date_creation','geometrie')
admin.site.register(Lampadaire,LampadaireGIS)

class PaneauGIS(GISModelAdmin):
    list_display=('nom','lat','lon','type','forme','role','fonctionnel','secteur','date_creation','geometrie')
admin.site.register(Paneau,PaneauGIS)

class PointEauGIS(GISModelAdmin):
    list_display=('nom','lat','lon','type','fonctionnel','secteur','date_creation','geometrie')
admin.site.register(PointEau,PointEauGIS)

class ReposoirGIS(GISModelAdmin):
    list_display=('nom','lat','lon','type','materiel','toiture','place','fonctionnel','secteur','date_creation','geometrie')
admin.site.register(Reposoir,ReposoirGIS)

class TelecomminicationGIS(GISModelAdmin):
    list_display=('nom','lat','lon','propriete','fonctionnel','secteur','date_creation','geometrie')
admin.site.register(Telecomminication,TelecomminicationGIS)

class MeteoGIS(GISModelAdmin):
    list_display=('nom','lat','lon','type','fonctionnel','secteur','date_creation','geometrie')
admin.site.register(Meteo,MeteoGIS)

class ArbreIsoleGIS(GISModelAdmin):
    list_display=('nom','lat','lon','type','espece','nature','hauteur','diametre','secteur','annee_creation','geometrie')
admin.site.register(ArbreIsole,ArbreIsoleGIS)

class LoisirGIS(GISModelAdmin):
    list_display=('nom','lat','lon','type_usage','categorie','aire','secteur','date_creation','geometrie')
admin.site.register(Loisir,LoisirGIS)

class EspaceVertGIS(GISModelAdmin):
    list_display=('nom','lat','lon','type','aire','secteur','date_creation','geometrie')
admin.site.register(EspaceVert,EspaceVertGIS)

class ParkingGIS(GISModelAdmin):
    list_display=('nom','lat','lon','type','aire','camera','toiture','agent_securite','lampadaire','secteur','date_creation','geometrie')
admin.site.register(Parking,ParkingGIS)

class PlanEauGIS(GISModelAdmin):
    list_display=('nom','lat','lon','aire','secteur','lampadaire','date_creation','geometrie')
admin.site.register(PlanEau,PlanEauGIS)

class BatimentGIS(GISModelAdmin):
    list_display=('nom','lat','lon','nature','electricite','aeration','adresse','extinteur','renove','internet','materiaux','nbre_niveau','toiture','toilette','camerasurvaillance','secteur','aire','date_construi','categorie','geometrie')
admin.site.register(Batiment,BatimentGIS)

class CameraGIS(GISModelAdmin):
    list_display=('nom','lat','lon','secteur','type','fonctionnel','date_instal','geometrie')
admin.site.register(Camera,CameraGIS)

class VoirieGIS(GISModelAdmin):
    list_display=('nom','lat','lon','largeur','longueur','adresse','lampadaire','Paneaux','geometrie')
admin.site.register(Voirie,VoirieGIS)

class AlerteBatimentGIS(admin.ModelAdmin):
    list_display=('batiment','disfonction','lesPennes','SOSMessage','date_alerte')
admin.site.register(AlerteBatiment,AlerteBatimentGIS)

class AlerteLampadaireGIS(admin.ModelAdmin):
    list_display=("lampadaire",'disfonction','SOSMessage','date_alerte')
admin.site.register(AlerteLampadaire,AlerteLampadaireGIS)

class AlertePointEauGIS(admin.ModelAdmin):
    list_display=('disfonction','SOSMessage','date_alerte')
admin.site.register(AlertePointEau,AlertePointEauGIS)

class AlerteWifiGIS(admin.ModelAdmin):
    list_display=('disfonction','SOSMessage','date_alerte')
admin.site.register(AlerteWifi,AlerteWifiGIS)

class AlertePoubelleFosseGIS(admin.ModelAdmin):
    list_display=('disfonction','poubellefosse','SOSMessage','date_alerte')
admin.site.register(AlertePoubelleFosse,AlertePoubelleFosseGIS)

class AlerteJardinGIS(admin.ModelAdmin):
    list_display=('disfonction','SOSMessage','date_alerte')
admin.site.register(AlerteJardin,AlerteJardinGIS)

class AlerteReposoirGIS(admin.ModelAdmin):
    list_display=('disfonction','SOSMessage','date_alerte')
admin.site.register(AlerteReposoir,AlerteReposoirGIS)

class AlerteGeneraleGIS(admin.ModelAdmin):
    list_display=('disfonction','SOSMessage','date_alerte')
admin.site.register(AlerteGenerale,AlerteGeneraleGIS)