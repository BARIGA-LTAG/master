import os
from shapely.wkt import loads
import json
from django.shortcuts import redirect, render
from ..formulaire import geomaprechercheForm
from ..models import *  
from geopy.distance import geodesic
from django.http import FileResponse
import geopandas as gpd
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
#A.objects.all().update(lat=None, lon=None)

# fonction pour la rechere de tous les infrastricture
@login_required(login_url='connection')
def geomaprecherche(request):
    # Initialiser les résultats en cas de non-requête
    results1 = results2 = results3 =results4 = results5=[]
    if 'query' in request.GET:
        query = request.GET['query']
        # Récupérer la position de l'utilisateur s'ils l'ont partagée
        user_lat = float(request.GET['lat']) if 'lat' in request.GET else None
        user_lon = float(request.GET['lon']) if 'lon' in request.GET else None

        if user_lat is not None and user_lon is not None:
            # Obtenir les résultats de la recherche
            results1 = Batis.objects.filter(nom__icontains=query)
            results2 = AireRepos.objects.filter(nom__icontains=query)
            results3 = PointEau.objects.filter(nom__icontains=query)
            results4 = ToiletteIsole.objects.filter(nom__icontains=query)
            results5 = Poubelle.objects.filter(nom__icontains=query)

            # Trier les résultats par la distance par rapport à l'utilisateur
            results1 = sorted(results1, key=lambda x: geodesic((user_lat, user_lon), (x.latitude, x.longitude)).m)[:5]
            results2 = sorted(results2, key=lambda x: geodesic((user_lat, user_lon), (x.latitude, x.longitude)).m)[:5]
            results3 = sorted(results3, key=lambda x: geodesic((user_lat, user_lon), (x.latitude, x.longitude)).m)[:5]
            results4 = sorted(results4, key=lambda x: geodesic((user_lat, user_lon), (x.latitude, x.longitude)).m)[:5]
            results5 = sorted(results5, key=lambda x: geodesic((user_lat, user_lon), (x.latitude, x.longitude)).m)[:5]
        else:
            # Si les coordonnées ne sont pas fournies, les résultats restent vides ou par défaut
            results1 = Batis.objects.filter(nom__icontains=query)[:5]
            results2 = AireRepos.objects.filter(nom__icontains=query)[:5]
            results3 = PointEau.objects.filter(nom__icontains=query)[:5]
            results4 = ToiletteIsole.objects.filter(nom__icontains=query)[:5]
            results5 = Poubelle.objects.filter(nom__icontains=query)[:5]

    # Préparation du formulaire de recherche
    form = geomaprechercheForm()
    
    # Préparer le contexte à envoyer au template
    context = {
        'form': form,
        'results1': results1,
        'results2': results2,
        'results3': results3,
        'results4': results4,
        'results5': results5,
    }
    return render(request, 'geospatial/map.html', context)

### telecharger les donneees
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

################################STATISTIQUE########################################
### statistique

def statistique(request,*args,**kwargs):
    return render(request,"geospatial/statistique.html")
                ############# TELECHARGEMENT##############


def admin_only(lavue):
    def verifier_acces(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/connection')  # Assurez-vous que l'URL est correcte
        if not request.user.is_staff:
            return HttpResponse("""
                <body style="height: 100vh; margin: 0; display: flex; justify-content: center; align-items: center; font-family: Roboto, sans-serif; background-color: #f4f4f4; color: #333; text-align: center;">
                <div style="padding: 20px; border: 1px solid #ccc; box-shadow: 0 2px 5px rgba(0,5,0,0.1); max-width: 600px; background-color: #5f4;">
                    Vous n'avez pas les droits d'accès à cette page.<br> Vous devez être un administrateur.
                </div>
                </body>
            """)
        return lavue(request, *args, **kwargs)
    return verifier_acces
@login_required(login_url='connection')
@admin_only 
def telecharger_donnees(request,*args,**kwargs):
   
    les_links = [
                [{'nom': 'telecharger_zone_csv', 'nom_url': 'UL:telecharger_csv1'},
                {'nom': 'telecharger_zone_geojson', 'nom_url': 'UL:telecharger_json1'},
                {'nom': 'telecharger_zone_gpkg', 'nom_url': 'UL:telecharger_gpkg1'}],
            
                [{'nom':'telecharger_cloture_csv', 'nom_url':'UL:telecharger_csv2'},
                {'nom':'telecharger_cloture_geojson', 'nom_url':'UL:telecharger_json2'},
                {'nom':'telecharger_cloture_gpkg', 'nom_url':'UL:telecharger_gpkg2'}],

                [{'nom':'telecharger_limite_csv', 'nom_url': 'UL:telecharger_csv3'},
                {'nom':'telecharger_limite_geojson', 'nom_url':'UL:telecharger_json3'},
                {'nom':'telecharger_limite_gpkg', 'nom_url': 'UL:telecharger_gpkg3'}],

                [{'nom': 'telecharger_fosse_csv', 'nom_url': 'UL:telecharger_csv4'},
                {'nom':  'telecharger_fosse_geojson', 'nom_url':'UL:telecharger_json4'},
                {'nom': 'telecharger_fosse_gpkg', 'nom_url':'UL:telecharger_gpkg4'}],

                [ {'nom': 'telecharger_poub_csv', 'nom_url':'UL:telecharger_csv5'},
                {'nom':  'telecharger_poub_geojson', 'nom_url':'UL:telecharger_json5'},
                {'nom':'telecharger_poub_gpkg', 'nom_url':'UL:telecharger_gpkg5'}],

                [{'nom':'telecharger_passe_csv', 'nom_url': 'UL:telecharger_csv6'},
                {'nom':'telecharger_passe_geojson', 'nom_url': 'UL:telecharger_json6'},
                {'nom':  'telecharger_passe_gpkg', 'nom_url': 'UL:telecharger_gpkg6'}],

                [{'nom': 'telecharger_kiosque_csv', 'nom_url': 'UL:telecharger_csv7'},
                {'nom': 'telecharger_kiosque_geojson', 'nom_url': 'UL:telecharger_json7'},
                {'nom': 'telecharger_kiosque_gpkg', 'nom_url': 'UL:telecharger_gpkg7'}],

                [{'nom':'telecharger_toilette_csv', 'nom_url': 'UL:telecharger_csv8'},
                {'nom': 'telecharger_toilette_geojson', 'nom_url': 'UL:telecharger_json8'},
                {'nom': 'telecharger_toilette_gpkg', 'nom_url': 'UL:telecharger_gpkg8'}],

                [{'nom': 'telecharger_eclairage_csv', 'nom_url': 'UL:telecharger_csv9'},
                {'nom':'telecharger_eclairage_geojson', 'nom_url': 'UL:telecharger_json9'},
                {'nom': 'telecharger_eclairage_gpkg', 'nom_url': 'UL:telecharger_gpkg9'}],

                [{'nom':'telecharger_panneau_csv', 'nom_url': 'UL:telecharger_csv10'},
                {'nom':  'telecharger_panneau_geojson', 'nom_url': 'UL:telecharger_json10'},
                {'nom': 'telecharger_panneau_gpkg', 'nom_url': 'UL:telecharger_gpkg10'}],
                
                [{'nom':'telecharger_point_eau_csv', 'nom_url': 'UL:telecharger_csv11'},
                {'nom':'telecharger_point_eau_geojson', 'nom_url': 'UL:telecharger_json11'},
                {'nom': 'telecharger_point_eau_gpkg', 'nom_url': 'UL:telecharger_gpkg11'}],

                [{'nom': 'telecharger_reposoir_csv', 'nom_url': 'UL:telecharger_csv12'},
                {'nom': 'telecharger_reposoir_geojson', 'nom_url': 'UL:telecharger_json12'},
                {'nom': 'telecharger_reposoir_gpkg', 'nom_url': 'UL:telecharger_gpkg12'}],

                [ {'nom': 'telecharger_telecom_csv', 'nom_url': 'UL:telecharger_csv13'},
                {'nom': 'telecharger_telecom_geojson', 'nom_url': 'UL:telecharger_json13'},
                {'nom':   'telecharger_telecom_gpkg', 'nom_url': 'UL:telecharger_gpkg13'}],

                [{'nom': 'telecharger_meteo_csv', 'nom_url': 'UL:telecharger_csv14'},
                {'nom':   'telecharger_meteo_geojson', 'nom_url': 'UL:telecharger_json14'},
                {'nom': 'telecharger_meteo_gpkg', 'nom_url': 'UL:telecharger_gpkg14'}],

                [{'nom':  'telecharger_arbre_i_csv', 'nom_url': 'UL:telecharger_csv15'},
                {'nom': 'telecharger_arbre_i_geojson', 'nom_url': 'UL:telecharger_json15'},
                {'nom':   'telecharger_arbre_i_gpkg', 'nom_url': 'UL:telecharger_gpkg15'}],

                [{'nom': 'telecharger_airloisir_csv', 'nom_url': 'UL:telecharger_csv16'},
                {'nom': 'telecharger_airloisir_geojson', 'nom_url': 'UL:telecharger_json16'},
                {'nom': 'telecharger_airloisir_gpkg', 'nom_url': 'UL:telecharger_gpkg16'}],

                [{'nom':'telecharger_vert_csv', 'nom_url': 'UL:telecharger_csv17'},
                {'nom': 'telecharger_vert_geojson', 'nom_url': 'UL:telecharger_json17'},
                {'nom': 'telecharger_vert_gpkg', 'nom_url': 'UL:telecharger_gpkg17'}],

                [{'nom':'telecharger_arbre_reb_csv', 'nom_url': 'UL:telecharger_csv18'},
                {'nom':  'telecharger_arbre_reb_geojson', 'nom_url': 'UL:telecharger_json18'},
                {'nom':'telecharger_arbre_reb_gpkg', 'nom_url': 'UL:telecharger_gpkg18'}],

                [  {'nom': 'telecharger_aire_sation_csv', 'nom_url': 'UL:telecharger_csv19'},
                {'nom':'telecharger_aire_sation_geojson', 'nom_url': 'UL:telecharger_json19'},
                {'nom':  'telecharger_aire_sation_gpkg', 'nom_url': 'UL:telecharger_gpkg19'}],

                [{'nom':'telecharger_aire_repos_csv', 'nom_url': 'UL:telecharger_csv20'},
                {'nom': 'telecharger_aire_repos_geojson', 'nom_url': 'UL:telecharger_json20'},
                {'nom':'telecharger_aire_repos_gpkg', 'nom_url': 'UL:telecharger_gpkg20'}],

                [{'nom': 'telecharger_bassin_csv', 'nom_url': 'UL:telecharger_csv21'},
                {'nom':'telecharger_bassin_geojson', 'nom_url': 'UL:telecharger_json21'},
                {'nom': 'telecharger_bassin_gpkg', 'nom_url': 'UL:telecharger_gpkg21'}],

                [ {'nom': 'telecharger_camera_csv', 'nom_url': 'UL:telecharger_csv22'},
                {'nom':'telecharger_camera_geojson', 'nom_url': 'UL:telecharger_json22'},
                {'nom': 'telecharger_camera_gpkg', 'nom_url': 'UL:telecharger_gpkg22'}],

                [   {'nom': 'telecharger_caniveau_csv', 'nom_url': 'UL:telecharger_csv23'},
                {'nom':'telecharger_caniveau_geojson', 'nom_url': 'UL:telecharger_json23'},
                {'nom': 'telecharger_caniveau_gpkg', 'nom_url': 'UL:telecharger_gpkg23'}],

                [{'nom': 'telecharger_voirie_csv', 'nom_url': 'UL:telecharger_csv24'},
                {'nom':'telecharger_voirie_geojson', 'nom_url': 'UL:telecharger_json24'},
                {'nom': 'telecharger_voirie_gpkg', 'nom_url': 'UL:telecharger_gpkg24'}],

                [ {'nom':'telecharger_batis_csv', 'nom_url': 'UL:telecharger_csv25'},
                {'nom':'telecharger_batis_geojson', 'nom_url': 'UL:telecharger_json25'},
                {'nom':'telecharger_batis_gpkg', 'nom_url': 'UL:telecharger_gpkg25'}]
                ]

    # Récupérer le numéro de la page demandée
    page_number = request.GET.get('page', 1)  # par défaut à la page 1 si 'page' n'est pas fourni
    # Créer un objet Paginator avec 9 éléments par page
    paginator = Paginator(les_links, 6)
    # Récupérer la page actuelle
    page_obj = paginator.get_page(page_number)
    # Passer la page_obj à votre template
    return render(request, "geospatial/donnee.html", {'page_obj': page_obj})

#########################################  POUR ZONE  #########################################################
def telecharger_zone(request, format):
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
            'longitude': float(zone.longitude),
            'latitude': float(zone.latitude),
            'limite': zone.limite.nom if zone.limite else None,
        }
        les_zones.append(une_zone)

    gdf = gpd.GeoDataFrame(les_zones, geometry=geometrie_zone, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'zone_ul.csv')
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'zone_ul.geojson')
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'zone_ul.gpkg')
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)
    
    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=zone_ul.{format}'
    return response

# execution
def telecharger_zone_csv(request):
    return telecharger_zone(request, 'csv')

def telecharger_zone_geojson(request):
    return telecharger_zone(request, 'geojson')

def telecharger_zone_gpkg(request):
    return telecharger_zone(request, 'gpkg')

#########################################  POUR CLOTUTRE  #########################################################
def telecharger_cloture(request,format):
    geom_cloture = [loads(cl.geometrie.wkt) for cl in cloture]
    la_clo = []
    for cl in cloture:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'longueur':float(cl.longueur) if cl.longueur else None,
            'hauteur':float(cl.hauteur) if cl.hauteur else None,
        }
        la_clo.append(clot)

    gdf = gpd.GeoDataFrame(la_clo, geometry=geom_cloture, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'cloture_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'cloture_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'cloture_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=cloture_ul.{format}'
    return response

# execution
def telecharger_cloture_csv(request):
    return telecharger_cloture(request, 'csv')

def telecharger_cloture_geojson(request):
    return telecharger_cloture(request, 'geojson')

def telecharger_cloture_gpkg(request):
    return telecharger_cloture(request, 'gpkg')

#########################################  POUR Limite  #########################################################

def telecharger_limite(request,format):
    geom_limite = [loads(cl.geometrie.wkt) for cl in limite]
    limul = []
    for cl in limite:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'aire':cl.aire,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        limul.append(clot)

    gdf = gpd.GeoDataFrame(limul, geometry=geom_limite, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'limite_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'limite_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'limite_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=limite_ul.{format}'
    return response

# execution
def telecharger_limite_csv(request):
    return telecharger_limite(request, 'csv')

def telecharger_limite_geojson(request):
    return telecharger_limite(request, 'geojson')

def telecharger_limite_gpkg(request):
    return telecharger_limite(request, 'gpkg')

#########################################  POUR FOSSE #########################################################

def telecharger_fosse(request,format):
    geom_fosse = [loads(cl.geometrie.wkt) for cl in fosse]
    les_foss = []
    for cl in fosse:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'fonctionnel':cl.fonctionnel,
            'secteur':cl.secteur,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_foss.append(clot)

    gdf = gpd.GeoDataFrame(les_foss, geometry=geom_fosse, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'fosse_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'fosse_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'fosse_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=fosse_septique_ul.{format}'
    return response

# execution
def telecharger_fosse_csv(request):
    return telecharger_fosse(request, 'csv')

def telecharger_fosse_geojson(request):
    return telecharger_fosse(request, 'geojson')

def telecharger_fosse_gpkg(request):
    return telecharger_fosse(request, 'gpkg')
#########################################  POUR POUBELLE  #########################################################
def telecharger_poubelle(request,format):
    geom_poub = [loads(cl.geometrie.wkt) for cl in poube]
    les_poub = []
    for cl in poube:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'fonctionnel':cl.fonctionnel,
            'secteur':cl.secteur,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_poub.append(clot)

    gdf = gpd.GeoDataFrame(les_poub, geometry=geom_poub, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'poubelle_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'poubelle_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'poubelle_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=poubelle_ul.{format}'
    return response

# execution
def telecharger_poub_csv(request):
    return telecharger_poubelle(request, 'csv')

def telecharger_poub_geojson(request):
    return telecharger_poubelle(request, 'geojson')

def telecharger_poub_gpkg(request):
    return telecharger_poubelle(request, 'gpkg')
#########################################  POUR PASSERELLE  #########################################################
def telecharger_passerelle(request,format):
    geom_pass = [loads(cl.geometrie.wkt) for cl in passe]
    les_pass = []
    for cl in passe:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom if cl.nom else None,
            'longitude':float(cl.longitude) if cl.longitude else None,
            'latitude':float(cl.latitude)if cl.latitude else None,
            'fonctionnel':cl.fonctionnel,
            'secteur':cl.secteur,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
        }
        les_pass.append(clot)

    gdf = gpd.GeoDataFrame(les_pass, geometry=geom_pass, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'passerelle.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'passerelle.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'passerelle.ulgpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=passerelle_ul.{format}'
    return response

# execution   
def telecharger_passe_csv(request):
    return telecharger_passerelle(request, 'csv')

def telecharger_passe_geojson(request):
    return telecharger_passerelle(request, 'geojson')

def telecharger_passe_gpkg(request):
    return telecharger_passerelle(request, 'gpkg')
#########################################  POUR KIOSQUES  #########################################################
def telecharger_kiosque(request,format):
    geom_kios = [loads(cl.geometrie.wkt) for cl in kiosq]
    les_kios = []
    for cl in kiosq:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'fonctionnel':cl.fonctionnel,
            'secteur':cl.secteur if cl.secteur else None,
            'usage':cl.usage if cl.usage else None,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_kios.append(clot)

    gdf = gpd.GeoDataFrame(les_kios, geometry=geom_kios, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'kiosque_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'kiosque_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'kiosque_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=kiosque_ul.{format}'
    return response

# execution
def telecharger_kiosque_csv(request):
    return telecharger_kiosque(request, 'csv')

def telecharger_kiosque_geojson(request):
    return telecharger_kiosque(request, 'geojson')

def telecharger_kiosque_gpkg(request):
    return telecharger_kiosque(request, 'gpkg')
#########################################  POUR OILETTE ISOLE  #########################################################
def telecharger_toilette(request,format):
    geom_toil = [loads(cl.geometrie.wkt) for cl in toilete]
    les_toil = []
    for cl in toilete:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'fonctionnel':cl.fonctionnel,
            'secteur':cl.secteur,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_toil.append(clot)

    gdf = gpd.GeoDataFrame(les_toil, geometry=geom_toil, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'toilette_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'toilette_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'toilette_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=toilette_ul.{format}'
    return response

# execution
def telecharger_toilette_csv(request):
    return telecharger_toilette(request, 'csv')

def telecharger_toilette_geojson(request):
    return telecharger_toilette(request, 'geojson')

def telecharger_toilette_gpkg(request):
    return telecharger_toilette(request, 'gpkg')
#########################################  POUR ECLAIRAGE  #########################################################
def telecharger_eclairage(request,format):
    geom_eclair = [loads(cl.geometrie.wkt) for cl in eclaire]
    les_eclair = []
    for cl in eclaire:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
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
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_eclair.append(clot)

    gdf = gpd.GeoDataFrame(les_eclair, geometry=geom_eclair, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'eclairage_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'eclairage_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'eclairage_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=eclairage_ul.{format}'
    return response

# execution
def telecharger_eclairage_csv(request):
    return telecharger_eclairage(request, 'csv')

def telecharger_eclairage_geojson(request):
    return telecharger_eclairage(request, 'geojson')

def telecharger_eclairage_gpkg(request):
    return telecharger_eclairage(request, 'gpkg')
#########################################  POUR CLOTUTRE  #########################################################
def telecharger_panneau(request,format):
    geom_pan = [loads(cl.geometrie.wkt) for cl in pann]
    les_pan = []
    for cl in pann:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
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
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_pan.append(clot)

    gdf = gpd.GeoDataFrame(les_pan, geometry=geom_pan, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'panneau_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'panneau_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'panneau_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=panneau_ul.{format}'
    return response

# execution
def telecharger_panneau_csv(request):
    return telecharger_panneau(request, 'csv')

def telecharger_panneau_geojson(request):
    return telecharger_panneau(request, 'geojson')

def telecharger_panneau_gpkg(request):
    return telecharger_panneau(request, 'gpkg')
#########################################  POUR POINT  EAU  #########################################################
def telecharger_pointeau(request,format):
    geom_pteau = [loads(cl.geometrie.wkt) for cl in eau]
    les_pteau = []
    for cl in eau:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'fonctionnel':cl.fonctionnel,
            'secteur':cl.secteur if cl.secteur else None,
            'source':cl.source if cl.source else None,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'trame_verte':cl.espace_vert.nom if cl.espace_vert else None,
            'batiment':cl.batiment.nom if cl.batiment else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_pteau.append(clot)

    gdf = gpd.GeoDataFrame(les_pteau, geometry=geom_pteau, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'point_eau_UL.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'point_eau_UL.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'point_eau_UL.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=point_eau_UL.{format}'
    return response

# execution
def telecharger_point_eau_csv(request):
    return telecharger_pointeau(request, 'csv')

def telecharger_point_eau_geojson(request):
    return telecharger_pointeau(request, 'geojson')

def telecharger_point_eau_gpkg(request):
    return telecharger_pointeau(request, 'gpkg')
#########################################  POUR REPOSOIR  #########################################################
def telecharger_reposoir(request,format):
    geom_repos = [loads(cl.geometrie.wkt) for cl in repo]
    les_repos = []
    for cl in repo:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
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
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_repos.append(clot)

    gdf = gpd.GeoDataFrame(les_repos, geometry=geom_repos, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'reposoir_UL.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'reposoir_UL.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'reposoir_UL.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=reposoir_UL.{format}'
    return response

# execution
def telecharger_reposoir_csv(request):
    return telecharger_reposoir(request, 'csv')

def telecharger_reposoir_geojson(request):
    return telecharger_reposoir(request, 'geojson')

def telecharger_reposoir_gpkg(request):
    return telecharger_reposoir(request, 'gpkg')
#########################################  POUR TELECOM  #########################################################
def telecharger_telecom(request,format):
    geom_tele = [loads(cl.geometrie.wkt) for cl in telecom]
    les_tele = []
    for cl in telecom:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'fonctionnel':cl.fonctionnel,
            'secteur':cl.secteur if cl.secteur else None,
            'type':cl.type if cl.type else None,
            'proprietaire':cl.proprietaire if cl.proprietaire else None,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_tele.append(clot)

    gdf = gpd.GeoDataFrame(les_tele, geometry=geom_tele, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'telecom_UL.csv') 
        gdf.to_csv(output_path, index=False, encoding='utf-8')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'telecom_UL.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'telecom_UL.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=telecom_UL.{format}'
    return response

# execution
def telecharger_telecom_csv(request):
    return telecharger_telecom(request, 'csv')

def telecharger_telecom_geojson(request):
    return telecharger_telecom(request, 'geojson')

def telecharger_telecom_gpkg(request):
    return telecharger_telecom(request, 'gpkg')
#########################################  POUR METEO  #########################################################
def telecharger_meteo(request,format):
    geom_meteo = [loads(cl.geometrie.wkt) for cl in meteo]
    les_meteo = []
    for cl in meteo:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'fonctionnel':cl.fonctionnel,
            'secteur':cl.secteur if cl.secteur else None,
            'type':cl.type if cl.type else None,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_meteo.append(clot)

    gdf = gpd.GeoDataFrame(les_meteo, geometry=geom_meteo, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'meteo_UL.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'meteo_UL.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'meteo_UL.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=stat_meteo_UL.{format}'
    return response

# execution
def telecharger_meteo_csv(request):
    return telecharger_meteo(request, 'csv')

def telecharger_meteo_geojson(request):
    return telecharger_meteo(request, 'geojson')

def telecharger_meteo_gpkg(request):
    return telecharger_meteo(request, 'gpkg')
#########################################  POUR ARBRE ISOLE  #########################################################
def telecharger_arbre_i(request,format):
    geom_arbri = [loads(cl.geometrie.wkt) for cl in arbreiso]
    les_arbri = []
    for cl in arbreiso:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'espece':cl.espece,
            'secteur':cl.secteur if cl.secteur else None,
            'type':cl.type if cl.type else None,
            'nature':cl.nature if cl.nature else None,
            'diametre':cl.diametre if cl.diametre else None,
            'hauteur':cl.hauteur if cl.hauteur else None,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.annee_creation.strftime("%Y-%m-%d") if cl.annee_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_arbri.append(clot)

    gdf = gpd.GeoDataFrame(les_arbri, geometry=geom_arbri, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'arbre_isole_UL.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'arbre_isole_UL.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'arbre_isole_UL.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=arbre_isole_UL.{format}'
    return response

# execution
def telecharger_arbre_i_csv(request):
    return telecharger_arbre_i(request, 'csv')

def telecharger_arbre_i_geojson(request):
    return telecharger_arbre_i(request, 'geojson')

def telecharger_arbre_i_gpkg(request):
    return telecharger_arbre_i(request, 'gpkg')
#########################################  POUR AIRE LOISIR  #########################################################
def telecharger_aireloisir(request,format):
    geom_airls = [loads(cl.geometrie.wkt) for cl in loisir]
    les_airls = []
    for cl in loisir:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'categorie':cl.categorie if cl.categorie else None,
            'secteur':cl.secteur if cl.secteur else None,
            'type_usage':cl.type_usage if cl.type_usage else None,
            'aire':cl.aire if cl.aire else None,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_airls.append(clot)

    gdf = gpd.GeoDataFrame(les_airls, geometry=geom_airls, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'aire_loisir_UL.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'aire_loisir_UL.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'aire_loisir_UL.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=aire_loisir_UL.{format}'
    return response

# execution
def telecharger_airloisir_csv(request):
    return telecharger_aireloisir(request, 'csv')

def telecharger_airloisir_geojson(request):
    return telecharger_aireloisir(request, 'geojson')

def telecharger_airloisir_gpkg(request):
    return telecharger_aireloisir(request, 'gpkg')
#########################################  POUR TRAME VERTE  #########################################################
def telecharger_trameverte(request,format):
    geom_vert = [loads(cl.geometrie.wkt) for cl in vert]
    les_vert = []
    for cl in vert:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'categorie':cl.categorie if cl.categorie else None,
            'secteur':cl.secteur if cl.secteur else None,
            'aire':cl.aire if cl.aire else None,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.date_creation.strftime("%Y-%m-%d") if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'batiment':cl.batiment.nom if cl.batiment else None,
            'lampadaire':cl.lampe.nom if cl.lampe else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_vert.append(clot)

    gdf = gpd.GeoDataFrame(les_vert, geometry=geom_vert, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'trame_verte_UL.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'trame_verte_UL.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'trame_verte_UL.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=trame_verte_UL.{format}'
    return response

# execution
def telecharger_vert_csv(request):
    return telecharger_trameverte(request, 'csv')

def telecharger_vert_geojson(request):
    return telecharger_trameverte(request, 'geojson')

def telecharger_vert_gpkg(request):
    return telecharger_trameverte(request, 'gpkg')
#########################################  POUR ARBRE REBOISE  #####################################################
def telecharger_arbre_r(request,format):
    geom_arbrre = [loads(cl.geometrie.wkt) for cl in arbrereb]
    les_arbrre = []
    for cl in arbrereb:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
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
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_arbrre.append(clot)

    gdf = gpd.GeoDataFrame(les_arbrre, geometry=geom_arbrre, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'arbre_reboise_UL.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'arbre_reboise_UL.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'arbre_reboise_UL.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=arbre_reboise_UL.{format}'
    return response

# execution
def telecharger_arbre_reb_csv(request):
    return telecharger_arbre_r(request, 'csv')

def telecharger_arbre_reb_geojson(request):
    return telecharger_arbre_r(request, 'geojson')

def telecharger_arbre_reb_gpkg(request):
    return telecharger_arbre_r(request, 'gpkg')
#########################################  POUR Aire stationnement  ##############################################
def telecharger_aire_sation(request,format):
    geom_station = [loads(cl.geometrie.wkt) for cl in parck]
    les_station = []
    for cl in parck:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
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
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_station.append(clot)

    gdf = gpd.GeoDataFrame(les_station, geometry=geom_station, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'aire_station_UL.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'aire_station_UL.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'aire_station_UL.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=aire_station_UL.{format}'
    return response

# execution
def telecharger_aire_sation_csv(request):
    return telecharger_aire_sation(request, 'csv')

def telecharger_aire_sation_geojson(request):
    return telecharger_aire_sation(request, 'geojson')

def telecharger_aire_sation_gpkg(request):
    return telecharger_aire_sation(request, 'gpkg')
#########################################  POUR AIRE DE REPOS  ####################################################
def telecharger_aire_repos(request,format):
    geom_airrep = [loads(cl.geometrie.wkt) for cl in airrepo]
    les_airrep = []
    for cl in airrepo:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'aire':cl.aire,
            'secteur':cl.secteur if cl.secteur else None,
            'image':cl.image.url if cl.image else None,
            'date_creation':cl.date_creation.strftime('%Y-%m-%d %H:%M:%S') if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_airrep.append(clot)

    gdf = gpd.GeoDataFrame(les_airrep, geometry=geom_airrep, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'aire_repos_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'aire_repos_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'aire_repos_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=aire_repos_ul.{format}'
    return response

# execution
def telecharger_aire_repos_csv(request):
    return telecharger_aire_repos(request, 'csv')

def telecharger_aire_repos_geojson(request):
    return telecharger_aire_repos(request, 'geojson')

def telecharger_aire_repos_gpkg(request):
    return telecharger_aire_repos(request, 'gpkg')
#########################################  POUR BASSIN EAU  #######################################################
def telecharger_bassin(request,format):
    geom_bassin = [loads(cl.geometrie.wkt) for cl in planeau]
    les_bassin = []
    for cl in planeau:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'aire':cl.aire,
            'secteur':cl.secteur if cl.secteur else None,
            'image':cl.image.url if cl.image else None,
            'aire':cl.aire if cl.aire else None,
            'eclairage':cl.lampadaire if cl.lampadaire else None,
            'date_creation':cl.date_creation.strftime('%Y-%m-%d %H:%M:%S') if cl.date_creation else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_bassin.append(clot)

    gdf = gpd.GeoDataFrame(les_bassin, geometry=geom_bassin, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'bassin_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'bassin_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'bassin_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=bassin_ul.{format}'
    return response

# execution
def telecharger_bassin_csv(request):
    return telecharger_bassin(request, 'csv')

def telecharger_bassin_geojson(request):
    return telecharger_bassin(request, 'geojson')

def telecharger_bassin_gpkg(request):
    return telecharger_bassin(request, 'gpkg')
#########################################  POUR CAMERA  #########################################################
def telecharger_camera(request,format):
    geom_cam = [loads(cl.geometrie.wkt) for cl in camera]
    les_cam = []
    for cl in camera:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'fonctionnel':cl.fonctionnel,
            'secteur':cl.secteur if cl.secteur else None,
            'type':cl.type if cl.type else None,
            'batiment':cl.batiment.nom if cl.batiment else None,
            'parking':cl.parking.nom if cl.parking else None,
            'date_instal':cl.date_instal.strftime('%Y-%m-%d %H:%M:%S') if cl.date_instal else None,
            'zone':cl.zone.nom if cl.zone else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
        }
        les_cam.append(clot)

    gdf = gpd.GeoDataFrame(les_cam, geometry=geom_cam, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'camera_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'camera_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'camera_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=camera_ul.{format}'
    return response

# execution
def telecharger_camera_csv(request):
    return telecharger_camera(request, 'csv')

def telecharger_camera_geojson(request):
    return telecharger_camera(request, 'geojson')

def telecharger_camera_gpkg(request):
    return telecharger_camera(request, 'gpkg')
#########################################  POUR CANIVEAU  #########################################################
def telecharger_caniveau(request,format):
    geom_caniv= [loads(cl.geometrie.wkt) for cl in canivo]
    les_canv = []
    for cl in canivo:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'largeur':cl.largeur if cl.largeur else None,
            'longueur':cl.longueur if cl.longueur else None,
            'profondeur':cl.profondueur if cl.profondueur else None,
            'aire':float(cl.aire) if cl.aire else None,
            'rue':cl.rue.nom if cl.rue else None,
            
        }
        les_canv.append(clot)

    gdf = gpd.GeoDataFrame(les_canv, geometry=geom_caniv, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'caniveau_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'caniveau_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'caniveau_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=caniveau_ul.{format}'
    return response

# execution
def telecharger_caniveau_csv(request):
    return telecharger_caniveau(request, 'csv')

def telecharger_caniveau_geojson(request):
    return telecharger_caniveau(request, 'geojson')

def telecharger_caniveau_gpkg(request):
    return telecharger_caniveau(request, 'gpkg')
#########################################  POUR VOIRIE  #########################################################
def telecharger_voirie(request,format):
    geom_voi = [loads(cl.geometrie.wkt) for cl in voie]
    les_voi = []
    for cl in voie:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
            'largeur':cl.largeur if cl.largeur else None,
            'longueur':cl.longueur if cl.longueur else None,
            'adresse':cl.adresse if cl.adresse else None,
            'aire':float(cl.aire) if cl.aire else None,
            'Panneau':cl.Panneau if cl.Panneau else None,
            'lampe':cl.lampe if cl.lampe else None,
            'caniveau':cl.caniveau if cl.caniveau else None,
            'nature':cl.nature if cl.nature else None,
            'categorie':cl.categorie if cl.categorie else None,
            'date_constru':cl.date_constru.strftime("%Y-%m-%d") if cl.date_constru else None,
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,

        }
        les_voi.append(clot)

    gdf = gpd.GeoDataFrame(les_voi, geometry=geom_voi, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'voirie_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'voirie_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'voirie_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=voirie_ul.{format}'
    return response

# execution
def telecharger_voirie_csv(request):
    return telecharger_voirie(request, 'csv')

def telecharger_voirie_geojson(request):
    return telecharger_voirie(request, 'geojson')

def telecharger_voirie_gpkg(request):
    return telecharger_voirie(request, 'gpkg')
#########################################  POUR BATIMENT  #######################################################
def telecharger_batis(request,format):
    geom_batis = [loads(cl.geometrie.wkt) for cl in batis]
    les_batis = []
    for cl in batis:
        if cl.geometrie and cl.geometrie.geojson:
            geometrie = json.loads(cl.geometrie.geojson)
        else:
            geometrie = None
    
        clot = {
            'nom': cl.nom,
            'longitude':float(cl.longitude),
            'latitude':float(cl.latitude),
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
            'limite':cl.limite.nom if cl.limite else None,
            'date_collecte':cl.date_collecte.strftime('%Y-%m-%d %H:%M:%S') if cl.date_collecte else None,
            'agent_collecteur':cl.agent_collecteur if cl.agent_collecteur else None,
            'info_modifier_le':cl.info_modifier_le.strftime('%Y-%m-%d %H:%M:%S') if cl.info_modifier_le else None,
            'nb_bureaux':cl.nb_bureaux if cl.nb_bureaux else None,
            'type_service':cl.type_service if cl.type_service else None,
            'heure_ouverture':cl.heure_ouverture.strftime('%H:%M:%S') if cl.heure_ouverture else None,
            'heure_fermeture':cl.heure_fermeture.strftime('%H:%M:%S') if cl.heure_fermeture else None,##
            'nb_salle':cl.nb_salle if cl.nb_salle else None,
            'nb_chaise':cl.nb_chaise if cl.nb_chaise else None,
            'type_banc':cl.type_banc if cl.type_banc else None,
            'kit_informatique':cl.kit_informatique if cl.kit_informatique else None,
            'type_formation':cl.type_formation if cl.type_formation else None,
            'domaine_formation':cl.domaine_formation if cl.domaine_formation else None,
            'nb_employe':cl.nb_employe if cl.nb_employe else None,
            'nb_appartement':cl.nb_appartement if cl.nb_appartement else None,
            'loyer_mensuel':cl.loyer_mensuel if cl.loyer_mensuel else None,
            'lit':cl.lit if cl.lit else None,
            'cuisine':cl.cuisine if cl.cuisine else None,
            'eau':cl.eau if cl.eau else None,
            ###########################################################################

        }
        les_batis.append(clot)

    gdf = gpd.GeoDataFrame(les_batis, geometry=geom_batis, crs='EPSG:32631')
    module_directory = os.path.dirname(__file__)
    if format == 'csv':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'batis_ul.csv') 
        gdf.to_csv(output_path, index=False, encoding='latin')
    elif format == 'geojson':
        output_path = os.path.join(module_directory, '..', 'static', 'gis', 'batis_ul.geojson') 
        gdf.to_file(output_path, driver='GeoJSON', index=False)
    elif format == 'gpkg':
        output_path =os.path.join(module_directory, '..', 'static', 'gis', 'batis_ul.gpkg') 
        gdf.to_file(output_path, driver='GPKG', index=False)
    else:
        # Gérer un format non pris en charge 
        return HttpResponse("Format non pris en charge", status=400)

    response = FileResponse(open(output_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename=batis_ul.{format}'
    return response

# execution
def telecharger_batis_csv(request):
    return telecharger_batis(request, 'csv')

def telecharger_batis_geojson(request):
    return telecharger_batis(request, 'geojson')

def telecharger_batis_gpkg(request):
    return telecharger_batis(request, 'gpkg')
#########################################  FIN  #######################################################