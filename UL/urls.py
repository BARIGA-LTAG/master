from UL.views.geoviews import  analyse_3, analyse_4, carte, analyse,analyse_1,analyse_2
from UL.views.formsviews import formassainisement,collecteur, formbatiment,faire_alerte
from UL.views.basicviews import statistique,geomaprecherche, telecharger_aire_repos_csv, telecharger_aire_repos_geojson, telecharger_aire_repos_gpkg, telecharger_aire_sation_csv, telecharger_aire_sation_geojson, telecharger_aire_sation_gpkg, telecharger_airloisir_csv, telecharger_airloisir_geojson, telecharger_airloisir_gpkg, telecharger_arbre_i_csv, telecharger_arbre_i_geojson, telecharger_arbre_i_gpkg, telecharger_arbre_reb_geojson, telecharger_arbre_reb_gpkg, telecharger_arbre_reb_csv, telecharger_bassin_csv, telecharger_bassin_geojson, telecharger_bassin_gpkg, telecharger_batis_csv, telecharger_batis_geojson, telecharger_batis_gpkg, telecharger_camera_csv, telecharger_camera_geojson, telecharger_camera_gpkg, telecharger_caniveau_csv, telecharger_caniveau_geojson, telecharger_caniveau_gpkg, telecharger_cloture_csv, telecharger_cloture_geojson, telecharger_cloture_gpkg,telecharger_donnees, telecharger_eclairage_csv, telecharger_eclairage_geojson, telecharger_eclairage_gpkg, telecharger_fosse_csv, telecharger_fosse_geojson, telecharger_fosse_gpkg, telecharger_kiosque_csv, telecharger_kiosque_geojson, telecharger_kiosque_gpkg, telecharger_limite_csv, telecharger_limite_geojson, telecharger_limite_gpkg, telecharger_meteo_csv, telecharger_meteo_geojson, telecharger_meteo_gpkg, telecharger_panneau_csv, telecharger_panneau_geojson, telecharger_panneau_gpkg, telecharger_passe_csv, telecharger_passe_geojson, telecharger_passe_gpkg, telecharger_point_eau_csv, telecharger_point_eau_geojson, telecharger_point_eau_gpkg, telecharger_poub_csv, telecharger_poub_geojson, telecharger_poub_gpkg, telecharger_reposoir_csv, telecharger_reposoir_geojson, telecharger_reposoir_gpkg, telecharger_telecom_csv, telecharger_telecom_geojson, telecharger_telecom_gpkg, telecharger_toilette_csv, telecharger_toilette_geojson, telecharger_toilette_gpkg, telecharger_vert_csv, telecharger_vert_geojson, telecharger_vert_gpkg, telecharger_voirie_csv, telecharger_voirie_geojson, telecharger_voirie_gpkg,telecharger_zone_csv,telecharger_zone_geojson,telecharger_zone_gpkg
from django.contrib import admin
from django.urls import path
app_name='UL'
urlpatterns = [
    path('georecherche/', geomaprecherche, name='map'),
    path('alerte/', faire_alerte, name="alerte"), 
    path('analyse/', analyse, name="analyse"), 
    path('analyse_py/', analyse_1, name="analyse1"), 
    path('analyse_js/', analyse_2, name="analyse2"), 
    path('analyse3_py/', analyse_3, name="analyse3"), 
    path('analyse4_py/', analyse_4, name="analyse4"), 
    path('statistique/', statistique, name="statistique"), 
    path('carte/', carte, name="carte"),  
    path('collecte/',collecteur, name="collecte"),
    path('collecte_assainis/',formassainisement, name="assainis"),
    path('collecte_bat/',formbatiment, name="batiment"),
    path('telecharger/',telecharger_donnees, name='telecharger'),
#  TELECHARGEMENT
    path('telecharger_csv1/', telecharger_zone_csv, name='telecharger_csv1'),
    path('telecharger_json1/', telecharger_zone_geojson, name='telecharger_json1'),
    path('telecharger_gpkg1/', telecharger_zone_gpkg, name='telecharger_gpkg1'),

    path('telecharger_csv2/', telecharger_cloture_csv, name='telecharger_csv2'),
    path('telecharger_json2/', telecharger_cloture_geojson, name='telecharger_json2'),
    path('telecharger_gpkg2/', telecharger_cloture_gpkg, name='telecharger_gpkg2'),

    path('telecharger_csv3/', telecharger_limite_csv, name='telecharger_csv3'),
    path('telecharger_json3/', telecharger_limite_geojson, name='telecharger_json3'),
    path('telecharger_gpkg3/', telecharger_limite_gpkg, name='telecharger_gpkg3'),

    path('telecharger_csv4/', telecharger_fosse_csv, name='telecharger_csv4'),
    path('telecharger_json4/', telecharger_fosse_geojson, name='telecharger_json4'),
    path('telecharger_gpkg4/', telecharger_fosse_gpkg, name='telecharger_gpkg4'),

    path('telecharger_csv5/', telecharger_poub_csv, name='telecharger_csv5'),
    path('telecharger_json5/', telecharger_poub_geojson, name='telecharger_json5'),
    path('telecharger_gpkg5/', telecharger_poub_gpkg, name='telecharger_gpkg5'),

    path('telecharger_csv6/', telecharger_passe_csv, name='telecharger_csv6'),
    path('telecharger_json6/', telecharger_passe_geojson, name='telecharger_json6'),
    path('telecharger_gpkg6/', telecharger_passe_gpkg, name='telecharger_gpkg6'),

    path('telecharger_csv7/', telecharger_kiosque_csv, name='telecharger_csv7'),
    path('telecharger_json7/', telecharger_kiosque_geojson, name='telecharger_json7'),
    path('telecharger_gpkg7/', telecharger_kiosque_gpkg, name='telecharger_gpkg7'),

    path('telecharger_csv8/', telecharger_toilette_csv, name='telecharger_csv8'),
    path('telecharger_json8/', telecharger_toilette_geojson, name='telecharger_json8'),
    path('telecharger_gpkg8/', telecharger_toilette_gpkg, name='telecharger_gpkg8'),

    path('telecharger_csv9/', telecharger_eclairage_csv, name='telecharger_csv9'),
    path('telecharger_json9/', telecharger_eclairage_geojson, name='telecharger_json9'),
    path('telecharger_gpkg9/', telecharger_eclairage_gpkg, name='telecharger_gpkg9'),

    path('telecharger_csv10/', telecharger_panneau_csv, name='telecharger_csv10'),
    path('telecharger_json10/', telecharger_panneau_geojson, name='telecharger_json10'),
    path('telecharger_gpkg10/', telecharger_panneau_gpkg, name='telecharger_gpkg10'),

    path('telecharger_csv11/', telecharger_point_eau_csv, name='telecharger_csv11'),
    path('telecharger_json11/', telecharger_point_eau_geojson, name='telecharger_json11'),
    path('telecharger_gpkg11/', telecharger_point_eau_gpkg, name='telecharger_gpkg11'),

    path('telecharger_csv12/', telecharger_reposoir_csv, name='telecharger_csv12'),
    path('telecharger_json12/', telecharger_reposoir_geojson, name='telecharger_json12'),
    path('telecharger_gpkg12/', telecharger_reposoir_gpkg, name='telecharger_gpkg12'),

    path('telecharger_csv13/', telecharger_telecom_csv, name='telecharger_csv13'),
    path('telecharger_json13/', telecharger_telecom_geojson, name='telecharger_json13'),
    path('telecharger_gpkg13/', telecharger_telecom_gpkg, name='telecharger_gpkg13'),

    path('telecharger_csv14/', telecharger_meteo_csv, name='telecharger_csv14'),
    path('telecharger_json14/', telecharger_meteo_geojson, name='telecharger_json14'),
    path('telecharger_gpkg14/', telecharger_meteo_gpkg, name='telecharger_gpkg14'),

    path('telecharger_csv15/', telecharger_arbre_i_csv, name='telecharger_csv15'),
    path('telecharger_json15/', telecharger_arbre_i_geojson, name='telecharger_json15'),
    path('telecharger_gpkg15/', telecharger_arbre_i_gpkg, name='telecharger_gpkg15'),

    path('telecharger_csv16/', telecharger_airloisir_csv, name='telecharger_csv16'),
    path('telecharger_json16/', telecharger_airloisir_geojson, name='telecharger_json16'),
    path('telecharger_gpkg16/', telecharger_airloisir_gpkg, name='telecharger_gpkg16'),

    path('telecharger_csv17/', telecharger_vert_csv, name='telecharger_csv17'),
    path('telecharger_json17/', telecharger_vert_geojson, name='telecharger_json17'),
    path('telecharger_gpkg17/', telecharger_vert_gpkg, name='telecharger_gpkg17'),

    path('telecharger_csv18/', telecharger_arbre_reb_csv, name='telecharger_csv18'),
    path('telecharger_json18/', telecharger_arbre_reb_geojson, name='telecharger_json18'),
    path('telecharger_gpkg18/', telecharger_arbre_reb_gpkg, name='telecharger_gpkg18'),

    path('telecharger_csv19/', telecharger_aire_sation_csv, name='telecharger_csv19'),
    path('telecharger_json19/', telecharger_aire_sation_geojson, name='telecharger_json19'),
    path('telecharger_gpkg19/', telecharger_aire_sation_gpkg, name='telecharger_gpkg19'),

    path('telecharger_csv20/', telecharger_aire_repos_csv, name='telecharger_csv20'),
    path('telecharger_json20/',telecharger_aire_repos_geojson, name='telecharger_json20'),
    path('telecharger_gpkg20/',telecharger_aire_repos_gpkg, name='telecharger_gpkg20'),

    path('telecharger_csv21/', telecharger_bassin_csv, name='telecharger_csv21'),
    path('telecharger_json21/',telecharger_bassin_geojson, name='telecharger_json21'),
    path('telecharger_gpkg21/',telecharger_bassin_gpkg, name='telecharger_gpkg21'),

    path('telecharger_csv22/', telecharger_camera_csv, name='telecharger_csv22'),
    path('telecharger_json22/',telecharger_camera_geojson, name='telecharger_json22'),
    path('telecharger_gpkg22/',telecharger_camera_gpkg, name='telecharger_gpkg22'),

    path('telecharger_csv23/', telecharger_caniveau_csv, name='telecharger_csv23'),
    path('telecharger_json23/',telecharger_caniveau_geojson, name='telecharger_json23'),
    path('telecharger_gpkg23/',telecharger_caniveau_gpkg, name='telecharger_gpkg23'),

    path('telecharger_csv24', telecharger_voirie_csv, name='telecharger_csv24'),
    path('telecharger_json24/',telecharger_voirie_geojson, name='telecharger_json24'),
    path('telecharger_gpkg24/',telecharger_voirie_gpkg, name='telecharger_gpkg24'),

    path('telecharger_csv25', telecharger_batis_csv, name='telecharger_csv25'),
    path('telecharger_json25/',telecharger_batis_geojson, name='telecharger_json25'),
    path('telecharger_gpkg25/',telecharger_batis_gpkg, name='telecharger_gpkg25'),
    ###############################FIN TELECHARGER##########################################



  ]

