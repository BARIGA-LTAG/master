
import json
import geopandas as gpd
from django.shortcuts import render, redirect
from ..models import ArbreIsole, ArbreReboise, Camera, Caniveau, Fosseseptique, Passerelle, Reposoir, StationMeteo, ToiletteIsole, Voirie, Zone,Poubelle,TrameVerte,PointEau,Eclairage,Kiosque,Batis,AireRepos, LimiteGeographique, AireLoisir, Panneau, AireStationnement, BassinEau, Telecommunication,LimiteGeographique,Cloture
from django.contrib.gis.geos import GEOSGeometry
from shapely.geometry import Polygon,LineString,MultiPolygon
from django.contrib.auth.decorators import login_required
from shapely.wkt import loads
import folium
from folium import plugins
from folium.plugins import FloatImage,MiniMap,HeatMap,MarkerCluster,FastMarkerCluster,SideBySideLayers
#Create your views here.
#@login_required(login_url='connection')
def analyse(request,*args,**kwargs):
    return render(request,"geospatial/analyse.html")
######################################### PRE¨PARATION DES DONNES ##############################################

#APPEL DES CLASS
zones = Zone.objects.all()
cloture=Cloture.objects.all()
limite=LimiteGeographique.objects.all()
fosse=Fosseseptique.objects.all()
poube=Poubelle.objects.all()
passe=Passerelle.objects.all()
kiosq=Kiosque.objects.all()
toilete=ToiletteIsole.objects.all()
eclaire=Eclairage.objects.all()
pann=Panneau.objects.all()
eau=PointEau.objects.all()
repo=Reposoir.objects.all()
telecom=Telecommunication.objects.all()
meteo=StationMeteo.objects.all()
arbreiso=ArbreIsole.objects.all()
loisir=AireLoisir.objects.all()
vert=TrameVerte.objects.all()
arbrereb=ArbreReboise.objects.all()
parck=AireStationnement.objects.all()
airrepo=AireRepos.objects.all()
planeau=BassinEau.objects.all()
batis=Batis.objects.all()
camera=Camera.objects.all()
canivo=Caniveau.objects.all()
voie=Voirie.objects.all()
##################################################################################################
geometrie_zone = [loads(zone.geometrie.wkt) for zone in zones]
les_zones = []

for zone in zones:
    if zone.geometrie and zone.geometrie.geojson:
        geometrie = json.loads(zone.geometrie.geojson)
    else:
        geometrie = None
    une_zone = {
        'nom': zone.nom,
        'theme':zone.theme,
        'aire': zone.aire,
    }
    les_zones.append(une_zone)
geo_zone = gpd.GeoDataFrame(les_zones, geometry=geometrie_zone, crs='EPSG:32631')


#########################################  POUR CLOTUTRE  #########################################################
geom_cloture = [loads(cl.geometrie.wkt) for cl in cloture]
la_clo = []
for cl in cloture:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'longueur':float(cl.longueur) if cl.longueur else None,
        'hauteur':float(cl.hauteur) if cl.hauteur else None,
    }
    la_clo.append(clot)

geo_cloture = gpd.GeoDataFrame(la_clo, geometry=geom_cloture, crs='EPSG:32631')
#########################################  POUR Limite  #########################################################
geom_limite = [loads(cl.geometrie.wkt) for cl in limite]
limul = []
for cl in limite:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'aire':cl.aire,
    }
    limul.append(clot)
geo_limite = gpd.GeoDataFrame(limul, geometry=geom_limite, crs='EPSG:32631')
#########################################  POUR FOSSE #########################################################
geom_fosse = [loads(cl.geometrie.wkt) for cl in fosse]
les_foss = []
for cl in fosse:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_foss.append(clot)
geo_fosse = gpd.GeoDataFrame(les_foss, geometry=geom_fosse, crs='EPSG:32631')
#########################################  POUR POUBELLE  #########################################################
geom_poub = [loads(cl.geometrie.wkt) for cl in poube]
les_poub = []
for cl in poube:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_poub.append(clot)
geo_poubel = gpd.GeoDataFrame(les_poub, geometry=geom_poub, crs='EPSG:32631')
#########################################  POUR PASSERELLE  #########################################################
geom_pass = [loads(cl.geometrie.wkt) for cl in passe]
les_pass = []
for cl in passe:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom if cl.nom else None,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_pass.append(clot)

geo_passerel = gpd.GeoDataFrame(les_pass, geometry=geom_pass, crs='EPSG:32631')
#########################################  POUR KIOSQUES  #########################################################
geom_kios = [loads(cl.geometrie.wkt) for cl in kiosq]
les_kios = []
for cl in kiosq:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur if cl.secteur else None,
        'usage':cl.usage if cl.usage else None,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_kios.append(clot)

geo_kiosq = gpd.GeoDataFrame(les_kios, geometry=geom_kios, crs='EPSG:32631')
#########################################  POUR OILETTE ISOLE  #########################################################
geom_toil = [loads(cl.geometrie.wkt) for cl in toilete]
les_toil = []
for cl in toilete:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_toil.append(clot)
geo_toilet = gpd.GeoDataFrame(les_toil, geometry=geom_toil, crs='EPSG:32631')

#########################################  POUR ECLAIRAGE  #########################################################
geom_eclair = [loads(cl.geometrie.wkt) for cl in eclaire]
les_eclair = []
for cl in eclaire:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur if cl.secteur else None,
        'energie':cl.energie if cl.energie else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
        'loisir':cl.loisir.nom if cl.loisir else None,
        'route':cl.route.nom if cl.route else None,
        'retenu_eau':cl.plan_eau.nom if cl.plan_eau else None,
        'trame_verte':cl.espace_vert.nom if cl.espace_vert else None,
        'batiment':cl.batiment.nom if cl.batiment else None,
    }
    les_eclair.append(clot)

geo_eclair = gpd.GeoDataFrame(les_eclair, geometry=geom_eclair, crs='EPSG:32631')
#########################################  POUR CLOTUTRE  #########################################################
geom_pan = [loads(cl.geometrie.wkt) for cl in pann]
les_pan = []
for cl in pann:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur if cl.secteur else None,
        'forme':cl.forme if cl.forme else None,
        'categorie':cl.categorie if cl.categorie else None,
        'type':cl.type if cl.type else None,
        'couleur':cl.couleur if cl.couleur else None,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
        'route':cl.route.nom if cl.route else None,
        'parking':cl.patking.nom if cl.patking else None,
    }
    les_pan.append(clot)
geo_pano = gpd.GeoDataFrame(les_pan, geometry=geom_pan, crs='EPSG:32631')

#########################################  POUR POINT  EAU  #########################################################
geom_pteau = [loads(cl.geometrie.wkt) for cl in eau]
les_pteau = []
for cl in eau:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur if cl.secteur else None,
        'source':cl.source if cl.source else None,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
        'trame_verte':cl.espace_vert.nom if cl.espace_vert else None,
        'batiment':cl.batiment.nom if cl.batiment else None,
    }
    les_pteau.append(clot)

geo_eau = gpd.GeoDataFrame(les_pteau, geometry=geom_pteau, crs='EPSG:32631')
#########################################  POUR REPOSOIR  #########################################################
geom_repos = [loads(cl.geometrie.wkt) for cl in repo]
les_repos = []
for cl in repo:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur if cl.secteur else None,
        'type':cl.type if cl.type else None,
        'materiel':cl.materiel if cl.materiel else None,
        'nombe_place':cl.nombe_place if cl.nombe_place else None,
        'toiture':cl.toiture if cl.toiture else None,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
        'trame_verte':cl.espace_vert.nom if cl.espace_vert else None,
        'aire_repos':cl.aire_repos.nom if cl.aire_repos else None,
    }
    les_repos.append(clot)

geo_repos = gpd.GeoDataFrame(les_repos, geometry=geom_repos, crs='EPSG:32631')

#########################################  POUR TELECOM  #########################################################
geom_tele = [loads(cl.geometrie.wkt) for cl in telecom]
les_tele = []
for cl in telecom:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur if cl.secteur else None,
        'type':cl.type if cl.type else None,
        'proprietaire':cl.proprietaire if cl.proprietaire else None,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_tele.append(clot)

geo_telecom = gpd.GeoDataFrame(les_tele, geometry=geom_tele, crs='EPSG:32631')

#########################################  POUR METEO  #########################################################
geom_meteo = [loads(cl.geometrie.wkt) for cl in meteo]
les_meteo = []
for cl in meteo:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur if cl.secteur else None,
        'type':cl.type if cl.type else None,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_meteo.append(clot)

geo_meteo = gpd.GeoDataFrame(les_meteo, geometry=geom_meteo, crs='EPSG:32631')

#########################################  POUR ARBRE ISOLE  #########################################################
geom_arbri = [loads(cl.geometrie.wkt) for cl in arbreiso]
les_arbri = []
for cl in arbreiso:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'espece':cl.espece,
        'secteur':cl.secteur if cl.secteur else None,
        'type':cl.type if cl.type else None,
        'nature':cl.nature if cl.nature else None,
        'diametre':cl.diametre if cl.diametre else None,
        'hauteur':cl.hauteur if cl.hauteur else None,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.annee_creation.strftime("%Y-%m-%d") if cl.annee_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_arbri.append(clot)

geo_arbri = gpd.GeoDataFrame(les_arbri, geometry=geom_arbri, crs='EPSG:32631')

#########################################  POUR AIRE LOISIR  #########################################################
geom_airls = [loads(cl.geometrie.wkt) for cl in loisir]
les_airls = []
for cl in loisir:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'categorie':cl.categorie if cl.categorie else None,
        'secteur':cl.secteur if cl.secteur else None,
        'type_usage':cl.type_usage if cl.type_usage else None,
        'aire':cl.aire if cl.aire else None,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_airls.append(clot)

geo_loisir = gpd.GeoDataFrame(les_airls, geometry=geom_airls, crs='EPSG:32631')
#########################################  POUR TRAME VERTE  #########################################################
geom_vert = [loads(cl.geometrie.wkt) for cl in vert]
les_vert = []
for cl in vert:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'categorie':cl.categorie if cl.categorie else None,
        'secteur':cl.secteur if cl.secteur else None,
        'aire':cl.aire if cl.aire else None,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
        'batiment':cl.batiment.nom if cl.batiment else None,
        'lampadaire':cl.lampe.nom if cl.lampe else None,
    }
    les_vert.append(clot)

geo_vert = gpd.GeoDataFrame(les_vert, geometry=geom_vert, crs='EPSG:32631')

#########################################  POUR ARBRE REBOISE  #####################################################
geom_arbrre = [loads(cl.geometrie.wkt) for cl in arbrereb]
les_arbrre = []
for cl in arbrereb:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'espece':cl.espece,
        'secteur':cl.secteur if cl.secteur else None,
        'type':cl.type if cl.type else None,
        'nature':cl.nature if cl.nature else None,
        'diametre':cl.diametre if cl.diametre else None,
        'hauteur':cl.hauteur if cl.hauteur else None,
        'image':cl.image.url if cl.image else None,
        'annee_reboise':cl.annee_reboise.strftime("%Y-%m-%d") if cl.annee_reboise else None,
        'zone':cl.zone.nom if cl.zone else None,
        'aire_reboisement':cl.zone_plantation.nom if cl.zone_plantation else None,
    }
    les_arbrre.append(clot)

geo_arbrereb = gpd.GeoDataFrame(les_arbrre, geometry=geom_arbrre, crs='EPSG:32631')

#########################################  POUR Aire stationnement  ##############################################
geom_station = [loads(cl.geometrie.wkt) for cl in parck]
les_station = []
for cl in parck:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'aire':cl.aire,
        'secteur':cl.secteur if cl.secteur else None,
        'type':cl.type if cl.type else None,
        'camera':cl.camera if cl.camera else None,
        'toiture':cl.toiture if cl.toiture else None,
        'agent_securite':cl.agent_securite if cl.agent_securite else None,
        'eclairage':cl.lampadaire if cl.lampadaire else None,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime('%Y-%m-%d %H:%M:%S') if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_station.append(clot)

geo_park = gpd.GeoDataFrame(les_station, geometry=geom_station, crs='EPSG:32631')

#########################################  POUR AIRE DE REPOS  ####################################################
geom_airrep = [loads(cl.geometrie.wkt) for cl in airrepo]
les_airrep = []
for cl in airrepo:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'aire':cl.aire,
        'secteur':cl.secteur if cl.secteur else None,
        'image':cl.image.url if cl.image else None,
        'date_creation':cl.date_creation.strftime('%Y-%m-%d %H:%M:%S') if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_airrep.append(clot)

geo_airepo = gpd.GeoDataFrame(les_airrep, geometry=geom_airrep, crs='EPSG:32631')

#########################################  POUR BASSIN EAU  #######################################################
geom_bassin = [loads(cl.geometrie.wkt) for cl in planeau]
les_bassin = []
for cl in planeau:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'aire':cl.aire,
        'secteur':cl.secteur if cl.secteur else None,
        'image':cl.image.url if cl.image else None,
        'aire':cl.aire if cl.aire else None,
        'eclairage':cl.lampadaire if cl.lampadaire else None,
        'date_creation':cl.date_creation.strftime('%Y-%m-%d %H:%M:%S') if cl.date_creation else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_bassin.append(clot)

geo_bassin = gpd.GeoDataFrame(les_bassin, geometry=geom_bassin, crs='EPSG:32631')
#########################################  POUR CAMERA  #########################################################
geom_cam = [loads(cl.geometrie.wkt) for cl in camera]
les_cam = []
for cl in camera:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'fonctionnel':cl.fonctionnel,
        'secteur':cl.secteur if cl.secteur else None,
        'type':cl.type if cl.type else None,
        'batiment':cl.batiment.nom if cl.batiment else None,
        'parking':cl.parking.nom if cl.parking else None,
        'date_instal':cl.date_instal.strftime('%Y-%m-%d %H:%M:%S') if cl.date_instal else None,
        'zone':cl.zone.nom if cl.zone else None,
    }
    les_cam.append(clot)

geo_cam = gpd.GeoDataFrame(les_cam, geometry=geom_cam, crs='EPSG:32631')

#########################################  POUR CANIVEAU  #########################################################
geom_caniv = [loads(cl.geometrie.wkt) for cl in canivo]
les_canv = []
for cl in canivo:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'largeur':cl.largeur if cl.largeur else None,
        'longueur':cl.longueur if cl.longueur else None,
        'profondeur':cl.profondueur if cl.profondueur else None,
        'aire':float(cl.aire) if cl.aire else None,
        'rue':cl.rue.nom if cl.rue else None,
    }
    les_canv.append(clot)

geo_caniv = gpd.GeoDataFrame(les_canv, geometry=geom_caniv, crs='EPSG:32631')

#########################################  POUR VOIRIE  #########################################################
geom_voi = [loads(cl.geometrie.wkt) for cl in voie]
les_voi = []
for cl in voie:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'largeur':cl.largeur if cl.largeur else None,
        'longueur':cl.longueur if cl.longueur else None,
        'adresse':cl.adresse if cl.adresse else None,
        'categorie':cl.categorie if cl.categorie else None,
        'aire':float(cl.aire) if cl.aire else None,
        'Panneau':cl.Panneau if cl.Panneau else None,
        'lampe':cl.lampe if cl.lampe else None,
        'caniveau':cl.caniveau if cl.caniveau else None,
        'nature':cl.nature if cl.nature else None,
        'date_constru':cl.date_constru.strftime("%Y-%m-%d") if cl.date_constru else None,
    }
    les_voi.append(clot)

geo_voie = gpd.GeoDataFrame(les_voi, geometry=geom_voi, crs='EPSG:32631')

#########################################  POUR BATIMENT  #######################################################
geom_batis = [loads(cl.geometrie.wkt) for cl in batis]
les_batis = []
for cl in batis:
    if cl.geometrie and cl.geometrie.geojson:
        geometrie = json.loads(cl.geometrie.geojson)
    else:
        geometrie = None

    clot = {
        'nom': cl.nom,
        'secteur':cl.secteur if cl.secteur else None,
        'aire':cl.aire if cl.aire else None,
        'toiture':cl.toiture if cl.toiture else None,
        'categorie':cl.categorie if cl.categorie else None,
        'aeration':cl.aeration if cl.aeration else None,
        'nature':cl.nature if cl.nature else None,
        'materiaux':cl.materiaux if cl.materiaux else None,
        'nbre_niveau':cl.nbre_niveau if cl.nbre_niveau else None,
        'camera':cl.camerasurvaillance if cl.camerasurvaillance else None,
        'extinteur':cl.extinteur if cl.extinteur else None,
        'internet':cl.internet if cl.internet else None,
        'renove':cl.renove if cl.renove else None,
        'image':cl.image.url if cl.image else None,
        'electricite':cl.electricite if cl.electricite else None,
        'toilette':cl.toilette if cl.toilette else None,
        'date_constru':cl.date_construi.strftime("%Y-%m-%d") if cl.date_construi else None,
        'zone':cl.zone.nom if cl.zone else None,
        'nb_bureaux':cl.nb_bureaux if cl.nb_bureaux else None,
        'type_service':cl.type_service if cl.type_service else None,
        'heure_ouverture':cl.heure_ouverture.strftime('%H:%M:%S') if cl.heure_ouverture else None,
        'heure_fermeture':cl.heure_fermeture.strftime('%H:%M:%S') if cl.heure_fermeture else None,##
        'kit_informatique':cl.kit_informatique if cl.kit_informatique else None,
        'type_formation':cl.type_formation if cl.type_formation else None,
        'domaine_formation':cl.domaine_formation if cl.domaine_formation else None,
    }
    les_batis.append(clot)
geo_batis = gpd.GeoDataFrame(les_batis, geometry=geom_batis, crs='EPSG:32631')

#########################################  FIN  #######################################################

############################################ CATRE OCUPATION SOL###################################################

def carte(request, *args, **kwargs):
    m = folium.Map(location=[6.175831, 1.213420], zoom_start=14.5,max_zoom=18,min_zoom=13,
                   max_lat=6.178137,min_lat=6.178658,max_lon=1.181888,min_lon=1.229314,control_scale=True,
                   )
        
    geo_limite.explore(m=m,color="#812815",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Limite",)
    geo_cloture.explore(m=m,color="#7E3F29",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Cloture",)
    geo_zone.explore(m=m,column="nom",scheme="naturalbreaks",legend=False,k=10,tooltip=False,popup=True,legend_kwds=dict(colorbar=False),name="pôle thématique",)
    geo_vert.explore(m=m,color="green",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Trame Verte",)
    geo_airepo.explore(m=m,color="#7B2B9D",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Aire de Repos",)
    geo_loisir.explore(m=m,color="#FEFB81",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Aire de Loisir",)
    geo_park.explore(m=m,color="#F214A1",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Aire de Stationnement",)
    geo_bassin.explore(m=m,color="#120EF1",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Retenue d'Eau",)
    geo_batis.explore(m=m,color="white",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Bâtis",)
    #geo_cam.explore(m=m,color="green",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Caméra",)
    geo_caniv.explore(m=m,color="#0EE4F1 ",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Caniveau",)
    geo_voie.explore(m=m,color="black",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Voirie",)
    geo_eau.explore(m=m,color="#2164D8",marker_kwds=dict(radius=7, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Point d'Eau",)
    geo_eclair.explore(m=m,color="#F13E0E",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Eclairage",)  
    geo_kiosq.explore(m=m,color="#DA1364",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Kiosques",)
    #geo_arbrereb.explore(m=m,color="green",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Arbre Reboisé",)
    #geo_arbri.explore(m=m,color="green",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Arbre Isolé",)
    geo_meteo.explore(m=m,color="#20599E",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Station Méteo",)
    geo_fosse.explore(m=m,color="#011106",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Fosse/Puisard",) 
    geo_pano.explore(m=m,color="#F07910",marker_kwds=dict(radius=7, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Panneau",)
    #geo_toilet.explore(m=m,color="green",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Toilette Isolé",)
    geo_telecom.explore(m=m,color="#85852E",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Télécommunication",)
    geo_passerel.explore(m=m,color="#707370 ",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Passerelle",)
    #geo_repos.explore(m=m,color="green",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Reposoir",)
    geo_poubel.explore(m=m,color="#13DA13",marker_kwds=dict(radius=5, fill=True),tooltip="nom",tooltip_kwds=dict(labels=True),popup=True,name="Poubelle",)
    
    folium.plugins.Fullscreen(
    position="topleft",title="Plein écran",title_cancel="Réduire",force_separate_button=True,).add_to(m)
    #carte reduite
    MiniMap(toggle_display=True,tile_layer="Cartodb dark_matter").add_to(m)
    #ajouter le NORD
    url = (
    "https://raw.githubusercontent.com/ocefpaf/secoora_assets_map/"
    "a250729bbcf2ddd12f46912d36c33f7539131bec/secoora_icons/rose.png"
    )
    FloatImage(url, bottom=60, left=5).add_to(m)
    # Ajouter une couche de tuiles Google Satellite
    folium.TileLayer("CartoDB positron", show=False).add_to(m)
    folium.LayerControl().add_to(m)  # use folium to add layer control
    carte_html = m._repr_html_()
    context = {'carte_html': carte_html}

    return render(request, 'geospatial/carte.html', context)

#############################################FAIRE DES ANALYSE SPATIAL AU COMPLET###################################

def analyse_1(request, *args, **kwargs):
    m = folium.Map(location=[6.175831, 1.213420], tiles="Cartodb Positron",zoom_start=14.5, max_zoom=18, min_zoom=13, control_scale=True)
    geo_limite.explore(name="limite UL", m=m,color="light")
    geo_zone.explore(column="nom", scheme="naturalbreaks", name="zonage", legend=False,show=False, m=m)
    folium.plugins.Fullscreen(position="topleft", title="Plein écran", title_cancel="Réduire", force_separate_button=True).add_to(m)
    geo_eau.explore(m=m, color="black", name="point d'eau")
##### densité
    dataO = [[float(y.latitude), float(y.longitude)] for y in eau]
    HeatMap(dataO, name="Densite point d'eau").add_to(m)

    # folium.TileLayer("CartoDB positron", show=False).add_to(m)
    folium.LayerControl().add_to(m)
    
    analyse_html = m._repr_html_()
    context = {'analyse_html': analyse_html}

    return render(request, "geospatial/analyse1.html", context)

def analyse_2(request,*args,**kwargs):
    m = folium.Map(location=[6.175831, 1.213420], tiles="Cartodb Positron",zoom_start=14.5, max_zoom=20, min_zoom=9, control_scale=True)
    geo_limite.explore(name="limite UL", m=m,color="")
    geo_zone.explore(column="nom", scheme="naturalbreaks", name="zonage", legend=False,show=False, m=m)
    folium.plugins.Fullscreen(position="topleft", title="Plein écran", title_cancel="Réduire", force_separate_button=True).add_to(m)
    geo_poubel.explore(m=m, color="green", name="poubelle")
##### densité
    datap = [[float(y.latitude), float(y.longitude)] for y in poube]
    HeatMap(datap, name="Densite poubelle").add_to(m)
    # folium.TileLayer("CartoDB positron", show=False).add_to(m)
    ################
    icon_create_function = """\
    function(cluster) {
        return L.divIcon({
        html: '<b>' + cluster.getChildCount() + '</b>',
        className: 'marker-cluster marker-cluster-large',
        iconSize: new L.Point(20, 20)
        });
    }"""
    ################
    marker_cluster = MarkerCluster(
        locations=[[float(y.latitude), float(y.longitude)] for y in poube],
        popups=les_poub,
        name=" poubelle cluster",
        overlay=True,
        control=True,
        icon_create_function=icon_create_function,
    )

    marker_cluster.add_to(m)

    folium.LayerControl().add_to(m)
    
    analyse_html2 = m._repr_html_()
    context = {'analyse_html2': analyse_html2}
    return render(request, "geospatial/analyse2.html", context)
###############
def tampon_color(color):
    """Retourne une fonction de style pour la couleur donnée."""
    return lambda obj: {
        'fillColor': color,'color': color, 'weight': 2,  'fillOpacity': 0.25,
    }
def analyse_3(request, *args, **kwargs):
    m = folium.Map(location=[6.175831, 1.213420],zoom_start=14.5, max_zoom=22, min_zoom=13, control_scale=True,tiles="CartoDB positron")
    geo_zone.explore(column="nom", scheme="naturalbreaks", name="zonage", legend=False,show=False, m=m)
    folium.plugins.Fullscreen(position="topleft", title="Plein écran", title_cancel="Réduire", force_separate_button=True).add_to(m)
    wifi_geo = geo_telecom[geo_telecom["type"] == "Antenne Wifi"]
    tampon_wifi1=wifi_geo.geometry.buffer(5)
    tampon_wifi2=wifi_geo.geometry.buffer(10)
    tampon_wifi3=wifi_geo.geometry.buffer(15)
    folium.GeoJson(tampon_wifi1,style_function=tampon_color('#00ff00'), name="Wifi Tampon 5m").add_to(m)
    folium.GeoJson(tampon_wifi2,style_function=tampon_color('#ffbf00'), name="Wifi Tampon 10m").add_to(m)
    folium.GeoJson(tampon_wifi3,style_function=tampon_color('#ff0000'), name="Wifi Tampon 15m").add_to(m)
    geo_telecom.explore(name="Télécommunication",marker_kwds=dict(radius=5, fill=True) ,legend=False,m=m)
    folium.LayerControl().add_to(m)
    analyse_html3 = m._repr_html_()
    context = {'analyse_html3': analyse_html3}
    return render(request, "geospatial/analyse3.html", context)
################################################

def analyse_4(request, *args, **kwargs):
    m = folium.Map(location=[6.175831, 1.213420], zoom_start=14.5, max_zoom=18, min_zoom=13, control_scale=True)
    folium.plugins.Fullscreen(position="topleft", title="Plein écran", title_cancel="Réduire", force_separate_button=True).add_to(m)
    
    # Crée et ajoute le chemin AntPath à la carte
    # folium.plugins.AntPath(
    #     locations=folium_coords,
    #     reverse=True,  # True comme booléen sans guillemets
    #     dash_array=[20, 30]
    # ).add_to(m)
    
    analyse_html4 = m._repr_html_()
    context = {'analyse_html4': analyse_html4}
    return render(request, "geospatial/analyse4.html", context)



# path = r"C:\Users\julien\Desktop\geoinformatique\geoapp_project\master\GISUL\pano.gpkg"
# donne= gpd.read_file(path)
# donne.head()
# def remove_z_dimension(geometry):
#      return Point(geometry.x, geometry.y)
# donne['geometry'] = donne['geometry'].apply(remove_z_dimension)

# for index, row in donne.iterrows():
#     d=Panneau(
#     #    categorie=row['cat'],
#     #     adresse=row['adress'],
#         commentaire=row['POINT'],
#         nom=  'panneau ' + str(row['Id_pan']),
#         geometrie=GEOSGeometry(row['geometry'].wkt,srid=32631),  
#      )
#     d.save()
# #AireRepos.objects.all().delete()