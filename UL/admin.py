# from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.contrib.gis import admin
from .models import *

#########################################
admin.site.site_title = ("MON-CAMPUS")
admin.site.site_header = ("MON-CAMPUS")
admin.site.index_title = ("MON-CAMPUS")

class AdminZoneGis(GISModelAdmin):
    list_display =('nom','theme','aire','latitude','longitude')
admin.site.register(Zone, AdminZoneGis)

class LimiteGis(GISModelAdmin):
    list_display =('nom','aire','latitude','longitude')
admin.site.register(LimiteGeographique, LimiteGis)

class PoubelleGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','fonctionnel','secteur','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(Poubelle,PoubelleGIS)

class FosseseptiqueGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','fonctionnel','secteur','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(Fosseseptique,FosseseptiqueGIS)

class PasserelleGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','fonctionnel','secteur','zone','date_creation','image')
admin.site.register(Passerelle,PasserelleGIS)


class KiosqueGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','usage','fonctionnel','secteur','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(Kiosque,KiosqueGIS)

class ToiletteGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','fonctionnel','secteur','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(ToiletteIsole,ToiletteGIS)

class LampadaireGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','energie','fonctionnel','secteur','route','zone','date_creation','date_collecte','info_modifier_le','plan_eau','loisir')
admin.site.register(Eclairage,LampadaireGIS)

class PanneauGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','type','forme','categorie','couleur','fonctionnel','secteur','route','patking','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(Panneau,PanneauGIS)

class PointEauGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','source','fonctionnel','secteur','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(PointEau,PointEauGIS)

class ReposoirGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','type','materiel','toiture','nombe_place','fonctionnel','secteur','aire_repos','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(Reposoir,ReposoirGIS)

class TelecomminicationGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','proprietaire','fonctionnel','secteur','type','proprietaire','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(Telecommunication,TelecomminicationGIS)

class MeteoGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','type','fonctionnel','secteur','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(StationMeteo,MeteoGIS)

class ArbreIsoleGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','type','espece','nature','hauteur','diametre','secteur','zone','annee_creation','date_collecte','info_modifier_le')
admin.site.register(ArbreIsole,ArbreIsoleGIS)

class ArbreReboiseGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','type','espece','nature','hauteur','diametre','secteur','zone','zone_plantation','annee_reboise','date_collecte','info_modifier_le')
admin.site.register(ArbreReboise,ArbreReboiseGIS)

class LoisirGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','type_usage','categorie','aire','secteur','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(AireLoisir,LoisirGIS)

class EspaceVertGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','categorie','aire','secteur','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(TrameVerte,EspaceVertGIS)

class ParkingGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','type','aire','camera','toiture','agent_securite','lampadaire','secteur','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(AireStationnement,ParkingGIS)

class PlanEauGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','aire','lampadaire','secteur','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(BassinEau,PlanEauGIS)

class AireReposGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','aire','secteur','zone','date_creation','date_collecte','info_modifier_le','image')
admin.site.register(AireRepos,AireReposGIS)

class BatimentGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','nature','secteur','zone','aire','date_construi','categorie','domaine_formation','type_formation','electricite','aeration','kit_informatique','extinteur','renove','internet','materiaux','nbre_niveau','toiture','toilette','camerasurvaillance')
admin.site.register(Batis,BatimentGIS)

class CameraGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','type','fonctionnel','secteur','zone','parking','batiment','date_instal','date_collecte','info_modifier_le')
admin.site.register(Camera,CameraGIS)

class CaniveauGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','aire','largeur','longueur','profondueur')
admin.site.register(Caniveau,CaniveauGIS)

class VoirieGIS(GISModelAdmin):
    list_display=('nom','latitude','longitude','categorie','largeur','longueur','adresse','lampe','Panneau','caniveau','nature','date_constru','date_collecte','info_modifier_le')
admin.site.register(Voirie,VoirieGIS)
##############################################################################
#alerte
class AlerteBatimentGIS(admin.ModelAdmin):
    list_display=('batiment','disfonction','lesPennes','SOSMessage','date_alerte','auteur')
admin.site.register(AlerteBatiment,AlerteBatimentGIS)

class AlerteLampadaireGIS(admin.ModelAdmin):
    list_display=("lampadaire",'disfonction','SOSMessage','date_alerte','auteur')
admin.site.register(AlerteLampadaire,AlerteLampadaireGIS)

class AlertePointEauGIS(admin.ModelAdmin):
    list_display=('point_eau','disfonction','SOSMessage','date_alerte')
admin.site.register(AlertePointEau,AlertePointEauGIS)

class AlerteWifiGIS(admin.ModelAdmin):
    list_display=('wifi','disfonction','SOSMessage','date_alerte','auteur')
admin.site.register(AlerteWifi,AlerteWifiGIS)

class AlertePoubelleFosseGIS(admin.ModelAdmin):
    list_display=('poubelle','disfonction','SOSMessage','date_alerte','auteur')
admin.site.register(AlertePoubelle,AlertePoubelleFosseGIS)

class AlerteJardinGIS(admin.ModelAdmin):
    list_display=('verdure','disfonction','SOSMessage','date_alerte','auteur')
admin.site.register(AlerteJardin,AlerteJardinGIS)

class AlerteReposoirGIS(admin.ModelAdmin):
    list_display=('repos','disfonction','SOSMessage','date_alerte','auteur')
admin.site.register(AlerteReposoir,AlerteReposoirGIS)

class AlerteGeneraleGIS(admin.ModelAdmin):
    list_display=('disfonction','SOSMessage','date_alerte','auteur')
admin.site.register(AlerteGenerale,AlerteGeneraleGIS)