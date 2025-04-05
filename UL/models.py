from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.gdal.libgdal import lgdal
from django.contrib.auth.models import User
from utilisateurs.models import Profile
import geopandas as gpd
from pyproj import Proj, transform

class Polyg_Lat_Lon():
    def get_lat_as_str(self):
        return str(self.latitude).replace(',', '.')
    def get_lon_as_str(self):
        return str(self.longitude).replace(',', '.')
    
class CodeLatLonGeom():
    def lat_lon_par_geometrie(self, *args, **kwargs):
        """Mettre à jour les coordonnées latitude et longitude à partir de la géométrie"""
        # Définir les systèmes de coordonnées
        utm = Proj(proj="utm", zone=31, ellps="WGS84")
        wgs84 = Proj(proj="latlong", datum="WGS84")
        if self.geometrie and self.latitude is None and self.longitude is None:
            #conversion par pyproj
            self.longitude, self.latitude = transform(utm, wgs84,self.geometrie.x, self.geometrie.y)
            super().save(*args, **kwargs) 

    def ajout_geometrie_par_lat_lon(self):
        """Met à jour le champ geometrie à partir des champs latitude et longitude."""
        if self.latitude is not None and self.longitude is not None and self.geometrie is None:
            # Convertit les coordonnées de WGS 84 à EPSG 32631
            pnt = Point(float(self.longitude), float(self.latitude), srid=4326)
            self.geometrie = pnt.transform(32631, clone=True)
            super().save()  # Enregistre les modifications
 # Utilisez la méthode save pour enregistrer les modifications et appeler ajout_geometrie_par_lat_lon
   # save en fonction du cas
    def save(self, *args, **kwargs):
        if self.latitude is None and self.longitude is None:
            self.lat_lon_par_geometrie(*args, **kwargs)
        else:
            self.ajout_geometrie_par_lat_lon()
        super().save(*args, **kwargs)
# les deux fonctions suivant sapplique a latitude et longitude si necessaire
    def get_lat_as_string(self):
        return str(self.latitude).replace(',', '.')

    def get_lon_as_string(self):
        return str(self.longitude).replace(',', '.')

class LimiteGeographique(models.Model):
    nom = models.CharField(max_length=50)
    aire = models.FloatField(default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    geometrie = models.MultiPolygonField(srid=32631)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom

    class Meta:
        verbose_name="Limite"

    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)

class Cloture(models.Model):
    nom = models.CharField(max_length=30)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    longueur= models.DecimalField(max_digits=15, decimal_places=2,null=True)
    hauteur= models.DecimalField(max_digits=15, decimal_places=2,null=True)
    geometrie = models.MultiLineStringField(srid=32631)
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)

class Zone(models.Model):
    nom = models.CharField(max_length=50)
    theme = models.CharField(max_length=60,null=True)
    aire = models.FloatField(default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True,blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True) 
    geometrie = models.MultiPolygonField(srid=32631)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Zone"
        verbose_name_plural="Zones"
    
    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)
    
CAMP=(
        ('Campus Nord', ('Campus Nord')),
        ('Campus Sud', ('Campus Sud')),
    )  

class Fosseseptique(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    fonctionnel=models.BooleanField(default=True)
    secteur=models.CharField(choices=CAMP,blank=True)
    commentaire=models.TextField(max_length=300,blank=True,null=True)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE 
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.PointField(blank=True,null=True,srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False) #nouveau
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)#nouveau
    info_modifier_le = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Fosse septique"
        verbose_name_plural="Fosses septiques"

class Poubelle(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=7,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7,null=True)
    fonctionnel=models.BooleanField(default=True)
    secteur=models.CharField(choices=CAMP,blank=True)
    commentaire=models.TextField(max_length=300,blank=True,null=True)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE # CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.PointField(blank=True,null=True,srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False) #nouveau
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)#nouveau
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Poubelle"
        verbose_name_plural="Poubelles"    

class Passerelle(models.Model):
    nom = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    geometrie = models.LineStringField(srid=32631)
    fonctionnel=models.BooleanField(default=True)
    secteur=models.CharField(choices=CAMP,blank=True,null=True)
    commentaire=models.TextField(max_length=300,blank=True,null=True)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name="Passerelle"
        verbose_name_plural="Passerelles"
USAGE=(
        ('Commercial', ('Commercial')),
        ('Sanitaire', ('Sanitaire')),
        ('Sociale', ('Sociale')),
        ('Pédagogique', ('Pédagogique')),
        ('Culturelle', ('Culturelle')),
    )

class Kiosque(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    usage=models.CharField(choices=USAGE)
    fonctionnel=models.BooleanField(default=True)
    secteur=models.CharField(choices=CAMP)
    commentaire=models.TextField(max_length=300,null=True,blank=True)
    date_creation=models.DateField(blank=True,null=True)
    image=models.ImageField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Kiosque"
        verbose_name_plural="Kiosques"

LAMP=(
        ('Energie Hydrolique', ('Energie Hydrolique')),
        ('Energie solaire', ('Energie solaire')),
    ) 

class ToiletteIsole(CodeLatLonGeom,models.Model):
    nom = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    geometrie = models.PointField(srid=32631)
    fonctionnel=models.BooleanField(default=True)
    secteur=models.CharField(choices=CAMP,blank=True,null=True)
    commentaire=models.TextField(max_length=300,blank=True,null=True)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,default=1,null=True)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False, null=True)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom
     
    class Meta:
        verbose_name="Toilette Isole"
        verbose_name_plural="Toilette Isoles"
 
class Eclairage(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    fonctionnel=models.BooleanField(default=True)
    energie=models.CharField(choices=LAMP,max_length=30)
    secteur=models.CharField(choices=CAMP,max_length=18)
    commentaire=models.TextField(max_length=300,null=True,blank=True)
    date_creation=models.DateField(blank=True,null=True)
    loisir = models.ForeignKey('AireLoisir', on_delete=models.SET_NULL,blank=True,null=True,related_name="lamp_loisir")# CLEE # CLEE
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE # CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    route = models.ForeignKey('Voirie', on_delete=models.SET_NULL,blank=True,null=True,related_name="lamp_route")# CLEE
    plan_eau = models.ForeignKey('BassinEau', on_delete=models.SET_NULL,blank=True,related_name="lamp_plan_eau",null=True)# CLEE
    espace_vert = models.ForeignKey('TrameVerte', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    batiment = models.ForeignKey('Batis', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Eclairage"
        verbose_name_plural="Eclairages"

PTYPE=(
        ('Danger', ('Danger')),
        ('Obligation', ('Obligation')),
        ('Interdiction', ('Interdiction')),
        ('indication', ('indication')),
    ) 

PCAT=(
        ('Routier', ('Routier')),
        ('Informationel', ('Informationel')),
    ) 

FORM=(
        ('Cercle', ('Cercle')),
        ('Carré', ('Carré')),
        ('Rectangle', ('Rectangle')),
        ('Triangle', ('Triangle')),
        ('Hec/Hex/gone', ('Hec/Hex/gone')),
    ) 
class Panneau(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=40)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    categorie=models.CharField(choices=PCAT)
    type=models.CharField(choices=PTYPE)
    forme=models.CharField(choices=FORM)
    couleur=models.CharField(max_length=40,null=True,blank=True)
    fonctionnel=models.BooleanField(default=True)
    secteur=models.CharField(choices=CAMP)
    commentaire=models.TextField(max_length=300,null=True,blank=True)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    route=models.ForeignKey('Voirie',on_delete=models.SET_NULL,blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    patking = models.ForeignKey('AireStationnement', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Panneau"
        verbose_name_plural="Panneaux"
EAU=(
        ('Forage', ('Forage')),
        ('Tde', ('Tde')),
    ) 
class PointEau(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=40)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    source=models.CharField(choices=EAU)
    fonctionnel=models.BooleanField(default=True)
    commentaire=models.TextField(max_length=300,null=True,blank=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    espace_vert = models.ForeignKey('TrameVerte', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    batiment = models.ForeignKey('Batis', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom

    class Meta:
        verbose_name="Point d'eau"
        verbose_name_plural="Points d'eaux"
CAT=(
        ('Banc', ('Banc')),
        ('Table banc', ('Table banc')),
        ('Banc couvert', ('Banc couvert')),
        ('Table banc couvert', ('Table banc couvert')),
    ) 
MAT=(
        ('Bois', ('Bois')),
        ('Béton', ('Béton')),
    ) 
class Reposoir(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=40)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    type=models.CharField(choices=CAT)
    materiel=models.CharField(choices=MAT)
    nombe_place=models.IntegerField()
    fonctionnel=models.BooleanField(default=True)
    toiture=models.BooleanField(default=False)
    commentaire=models.TextField(max_length=300,null=True,blank=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    aire_repos = models.ForeignKey('AireRepos', on_delete=models.SET_NULL,null=True)# CLEE
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    espace_vert = models.ForeignKey('TrameVerte', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Reposoir"
        verbose_name_plural="Reposoirs"

PTEL=(
        ('Université de Lomé', ('Université de Lomé')),
        ('Moov', ('Moov')),
        ('Banque', ('Banque')),
        ('République Togolaise', ('République Togolaise')),
        ('TogoCom', ('TogoCom')),
    )
TYP_TEL=(
        ('Antenne Securité', ('Antenne Securité')),
        ('Antenne réseau', ('Antenne réseau')),
        ('Antenne Radio', ('Antenne Radio' )),
        ('Antenne Wifi', ('Antenne Wifi')),
    )  
class Telecommunication(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=40)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    type=models.CharField(choices=TYP_TEL)
    fonctionnel=models.BooleanField(default=True)
    commentaire=models.TextField(max_length=300,blank=True,null=True)
    secteur=models.CharField(choices=CAMP)
    proprietaire=models.CharField(choices=PTEL)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE # CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Telecommunication"
        verbose_name_plural="Telecommunications"

METEO=(
        ('Station Synoptique', ('Station Synoptique')),
        ('Antenne Manuelle', ('Antenne Manuelle')),
    )
class StationMeteo(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    type=models.CharField(choices=METEO) # a faire apres
    fonctionnel=models.BooleanField(default=True)
    commentaire=models.TextField(max_length=300,null=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Station météo"
        verbose_name_plural="Stations météos"

ARBR2=(
        ('Arbre Fruitier', ('Arbre Fruitier')),
        ('Arbre Bois', ('Arbre Bois')),
    )
ARBR1=(
        ('Arbre naturel', ('Arbre naturel')),
        ('Arbre reboisé', ('Arbre reboisé')),
    )
class ArbreIsole(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    espece=models.CharField(max_length=80,blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    type=models.CharField(choices=ARBR1)
    hauteur=models.FloatField(blank=True, null=True)
    diametre=models.FloatField(blank=True, null=True)
    commentaire=models.TextField(max_length=300,null=True)
    secteur=models.CharField(choices=CAMP)
    nature=models.CharField(choices=ARBR2)
    image=models.ImageField(blank=True, null=True)
    annee_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Arbre isolé"
        verbose_name_plural="Arbres isolés"

LOIS1=(
        ('Sport', ('Sport')),
        ('Evenement Culturel', ('Evenement Culturel')),
    )
LOIS2=(
        ('Footbal', ('Footbal')),
        ('Bascketball', ('Bascketball')),
        ('Voleyball', ('Voleyball')),
        ('Tenis', ('Tenis')),
        ('Dance', ('Dance')),
        ('Auditerium', ('Auditerium')),
    )
class AireLoisir(models.Model):
    nom = models.CharField(max_length=50)
    categorie = models.CharField(max_length=50,choices=LOIS1)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    type_usage=models.CharField(choices=LOIS2)
    aire= models.FloatField(default=0)
    commentaire=models.TextField(max_length=300,blank=True,null=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.MultiPolygonField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.nom
    
    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)

    class Meta:
        verbose_name=" Aire de Loisir"
        verbose_name_plural="Aires de loisirs"
VERT=(
        ('Aire Forestiére Naturelles Existante', ('Aire Forestiére Naturelles Existante')),
        ('Aire Forestiére Naturelles Reboisé', ('Aire Forestiére Naturelles Reboisé')),
        ('Aire Forestiére de Redéployement Reboisé', ('Aire Forestiére de Redéployement Reboisé')),
        ('Aire Forestiére de Redéployement Non reboisée', ('Aire Forestiére de Redéployement Non Reboisée')),
        ('Espace vert aménagé', ('Espace vert Aménagé')),
        ('Espace vert Non aménagé', ('Espace vert Non aménagé')),
        ('Ceinture Verte Non Aménagée', ('Ceinture Verte Non Aménagée')),
        ('Parc Forestier Reboisé', ('Parc Forestier Reboisé')),
        ('Parc Forestier Non Reboisé', ('Parc Forestier Non Reboisé')),
        ("Stricture d'Acueil Non Amenagée", ("Stricture d'Acueil Non Amenagée")),
        ('Jardin Botanique', ('Jardin Botanique (Végétation Experimentale)')),
        ('Autre Aire de Redéployement', ('Autre Aire de Redéployement')),
    )
class TrameVerte(models.Model):
    nom = models.CharField(max_length=50)
    categorie = models.CharField(max_length=60,choices=VERT)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    aire= models.FloatField(default=0)
    commentaire=models.TextField(max_length=300,blank=True,null=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    batiment = models.OneToOneField('Batis', on_delete=models.SET_NULL,blank=True,related_name="bat_jardin",null=True)# CLEE
    lampe = models.ForeignKey(Eclairage, on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.MultiPolygonField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.nom
    
    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)
    
    
    class Meta:
        verbose_name="Trame Verte"

class ArbreReboise(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    espece=models.CharField(max_length=80,blank=True,null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    type=models.CharField(default="Arbre Reboisé")
    hauteur=models.FloatField(blank=True,null=True)
    diametre=models.FloatField(blank=True,null=True)
    commentaire=models.TextField(max_length=300,null=True)
    secteur=models.CharField(choices=CAMP)
    nature=models.CharField(choices=ARBR2)
    annee_reboise=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    zone_plantation = models.ForeignKey(TrameVerte, on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Arbre Reboisé"
        verbose_name_plural="Arbres Reboisés"

PARK=(
        ('Moto/Cyclo', ('Moto/Cyclo')),
        ('Automobile', ('Automobile')),
    )
class AireStationnement(Polyg_Lat_Lon,models.Model):
    nom = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    type=models.CharField(choices=PARK)
    aire= models.FloatField(default=0)
    camera=models.BooleanField(default=True)
    toiture=models.BooleanField(default=False)
    agent_securite=models.BooleanField(default=True)
    lampadaire=models.BooleanField(default=True)
    date_creation=models.DateTimeField(blank=True, null=True)
    commentaire=models.TextField(max_length=300,blank=True,null=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.MultiPolygonField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True,null=True)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom

    class Meta:
        verbose_name="Aire de stationnement"
        #verbose_name_plural="Parkings"

    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)

class AireRepos(Polyg_Lat_Lon,models.Model):
    nom = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    aire= models.FloatField(default=0)
    commentaire=models.TextField(max_length=300,blank=True,null=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.MultiPolygonField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Aire de Repos"
        verbose_name_plural="Aires de Repos"
    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)

class BassinEau(models.Model):
    nom = models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    aire= models.FloatField(default=0,null=True)
    lampadaire=models.BooleanField(default=True)
    date_creation=models.DateTimeField(blank=True, null=True)
    commentaire=models.TextField(max_length=300,null=True,blank=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    zone=models.ForeignKey(Zone,on_delete=models.SET_NULL,null=True) # CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.MultiPolygonField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Bassin d'Eau"
        verbose_name_plural="Bassin d'Eaux"

    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)

NIVO=(
        ('Rez-de-chaussé', ('Rez-de-chaussé')),
        ('Niveau 1', ('Niveau 1')),
        ('Niveau 2', ('Niveau 2')),
        ('Niveau 3', ('Niveau 3')),
        ('Niveau 4', ('Niveau 4')),
        ('Niveau 5', ('Niveau 5')),
        ('Niveau 6', ('Niveau 6')),
        ('Niveau 7', ('Niveau 7')),
        ('Niveau 8', ('Niveau 8')),
    )
BATRIO=(
        ('Materiaux industriels', ('Materiaux industriels')),
        ('Materiaux ecologique', ('Materiaux ecologique')),
    )
AERA=(
        ('Ventilation', ('Ventilation')),
        ('Climatisation', ('Climatisation')),
        ('NEANT/Naturel', ('NEANT/Naturel')),
    )
TOIT=(
        ('Dallé', ('Dallé')),
        ('TULLE', ('TULLE')),
        ('Tôle Aluminium', ('Tôle Aluminium')),
    )
NATBAT=(
        ('En Chantier', ('En Chantier')),
        ('Achevé fonctionnel', ('Achevé fonctionnel')),
        ('Achevé Non fonctionnel', ('Achevé Non fonctionnel')),
    )
CATEGORIES = [
    ("administratif", "Administratif"),
    ("pedagogique", "Pédagogique"),
    ("commercial", "comercial"),
    ("residentiel", "residentiel"),
]

TYPFORMA=(
        ('Professionnelle', ('Professionnelle')),
        ('Recherche', ('Recherche')),
        ('Mixte', ('Mixte')),
    )
DOFORMA=(
        ('Hybride/Polyvalent', ('Hybride/Polyvalent')),
        ('Santé', ('Santé')),
        ('Economie', ('Economie')),
        ('Homme/Societé', ('Homme/Societé')),
         ('Sport', ('Sport')),
        ('Informatique', ('Informatique')),
         ('Agronomie', ('Agronomie')),
        ('Langue et Art', ('Langue et Art')),
         ('Communication', ('Communication')),
        ('Droit/Politique', ('Droit/Politique')),
    )

CHAIZ=(
        ('Chaise Bois', ('Chaise Bois')),
        ('Chaise Plastique', ('Chaise Plastique')),
         ('Chaise Fauteil', ('Chaise Fauteil')),
    )
class Batis(Polyg_Lat_Lon,models.Model):
    nom= models.CharField(max_length=60,null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    aire= models.FloatField(default=0)
    commentaire= models.CharField(max_length=200,null=True)
    camerasurvaillance=models.BooleanField(default=False)
    extinteur=models.BooleanField(default=False)
    internet=models.BooleanField(default=False)
    renove=models.BooleanField(default=False)
    nature=models.CharField(choices=NATBAT) #faire un choice ou comment
    aeration= models.CharField(max_length=30,choices=AERA,)
    date_construi=models.DateField(blank=True,null=True)
    electricite=models.BooleanField(default=True)
    secteur=models.CharField(choices=CAMP,max_length=19)
    toilette=models.BooleanField(default=False)
    toiture= models.CharField(max_length=60,choices=TOIT)
    categorie = models.CharField(max_length=50, choices=CATEGORIES, null=True) #nouveaute
    nbre_niveau= models.CharField(choices=NIVO,null=True)
    materiaux= models.CharField(max_length=30,choices=BATRIO,null=True)
    image=models.ImageField(blank=True,null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,null=True)# CLEE # CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.MultiPolygonField(srid=32631,blank=True,null=True)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
#class BatimentAdministratif(Batis):
    nb_bureaux = models.PositiveIntegerField(default=0)
    type_service= models.CharField(max_length=50,blank=True,null=True)################
    heure_ouverture=models.TimeField(blank=True,null=True)
    heure_fermeture=models.TimeField(blank=True,null=True)
#class BatimentPedagogique(Batis):
    nb_salle = models.PositiveIntegerField(default=0,blank=True,null=True)
    nb_chaise = models.PositiveIntegerField(default=0,blank=True,null=True)
    type_banc=models.CharField(choices=CHAIZ, max_length=30,blank=True,null=True)####
    kit_informatique=models.BooleanField(default=False)
    type_formation=models.CharField(choices=TYPFORMA,max_length=30,blank=True,null=True)#########
    domaine_formation=models.CharField(choices=DOFORMA,max_length=30,blank=True,null=True)####
#class BatimentAdminPedago(Batis):
    nb_employe = models.PositiveIntegerField(default=0)
    #type_commerce= models.CharField(max_length=60,blank=True,null=True)
#class BatimentResidentiel(Batis):
    nb_appartement = models.PositiveIntegerField(blank=True,null=True)
    loyer_mensuel= models.FloatField(blank=True,null=True)
    lit=models.BooleanField(default=False)
    cuisine=models.BooleanField(default=False)
    eau=models.BooleanField(default=True)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Batis"
        verbose_name_plural="Batiments"

    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)

CAMERA=(
        ('RGB', ('RGB')),
        ('InfraRouge', ('InfraRouge')),
    )
class Camera(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    date_instal=models.DateField(null=True,blank=True)
    secteur=models.CharField(max_length=11,choices=CAMP)
    type=models.CharField(max_length=30,choices=CAMERA)
    fonctionnel=models.BooleanField(default=True)
    batiment=models.ForeignKey(Batis,on_delete=models.SET_NULL,null=True,related_name="camera_bat")
    parking=models.ForeignKey(AireStationnement,on_delete=models.SET_NULL, null=True, related_name="camera_park")
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL,blank=True,null=True)# CLEE # CLEE
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,null=True)
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField( auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.nom
    class Meta:
        verbose_name="Camera"
        verbose_name_plural="Cameras"

class Caniveau(models.Model):
    nom = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    aire=models.DecimalField(max_digits=15, decimal_places=2,null=True)
    rue=models.ForeignKey('Voirie',on_delete=models.SET_NULL,related_name="caniveau_rue", null=True)
    largeur= models.FloatField(default=0)
    longueur= models.FloatField(default=0)
    profondueur= models.FloatField(default=0)
    geometrie = models.MultiPolygonField(srid=32631)

    def calcul_aire(self):
        return self.geometrie.area

    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)
TYP_ROUT=(
        ('Bitumé', ('Bitumé')),
        ('Pavé et ciment', ('Pavé et ciment')),
        ('Non Révetue', ('Non Révetue')),
    )
CAT_ROUT=(
        ('circulation Petonne', ('circulation pietonne')),
        ('circulation automobile', ('circulation automobile')),
       
    )
class Voirie(models.Model):
    nom = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6,null=True)
    date_constru=models.DateTimeField(blank=True, null=True)
    largeur= models.FloatField(default=0)
    adresse = models.CharField(max_length=200)
    aire=models.DecimalField(max_digits=15, decimal_places=2,null=True)
    longueur= models.FloatField(default=0)
    Panneau=models.BooleanField(default=True)
    lampe=models.BooleanField(default=True)
    caniveau=models.BooleanField(default=True)
    nature= models.CharField(max_length=30,choices=TYP_ROUT)
    categorie= models.CharField(max_length=30,choices=CAT_ROUT)
    limite=models.ForeignKey(LimiteGeographique,on_delete=models.PROTECT,default=1,null=True, related_name="voirie_limite") # CLEE
    geometrie = models.MultiPolygonField(null=True, srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True,null=True)
    info_modifier_le = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.nom
    
    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  
        if self.geometrie.centroid: 
            centre=self.geometrie.transform(4326, clone=True).centroid
            self.longitude, self.latitude = centre.x, centre.y
        super().save(*args, **kwargs)

    class Meta:
        verbose_name="Route"
        verbose_name_plural="Routes"

####################
##############
from multiselectfield import MultiSelectField
# LES ALERTES
CHOICES = (
        ('Climatisation', 'Climatisation'),
        ('Ventilateur', 'Ventilateur'),
        ('Ampoule', 'Ampoule'),
        ('Sonorisation', 'Sonorisation'),
        ('Table/Banc', 'Table/Banc'),
    )

class AlerteBatiment(models.Model):
    disfonction=models.BooleanField(default=True)
    lesPennes= MultiSelectField(choices=CHOICES,max_length=300)
    SOSMessage=models.TextField(max_length=150)
    batiment=models.ForeignKey(Batis,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.ForeignKey(Profile,on_delete=models.SET_NULL,editable=False,null=True,default=1)
    def __str__(self):
        return 'alerte_'+ str(self.id)+ '_Batis'
   
class AlerteLampadaire(models.Model):
    disfonction=models.BooleanField(default=True)
    SOSMessage=models.TextField(max_length=150)
    lampadaire=models.ForeignKey(Eclairage,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.ForeignKey(Profile,on_delete=models.SET_NULL,editable=False,null=True,default=1)
    def __str__(self):
        return 'alerte_'+ str(self.id)+ '_Lampe'
class AlertePointEau(models.Model):
    disfonction=models.BooleanField(default=True)
    SOSMessage=models.TextField(max_length=150)
    point_eau=models.ForeignKey(PointEau,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.ForeignKey(Profile,on_delete=models.SET_NULL,editable=False,null=True,default=1)
    def __str__(self):
        return 'alerte_'+ str(self.id)+ '_Robinet'

class AlerteWifi(models.Model):
    disfonction=models.BooleanField(default=True)
    SOSMessage=models.TextField(max_length=150)
    wifi=models.ForeignKey(Telecommunication,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.ForeignKey(Profile,on_delete=models.SET_NULL,editable=False,null=True,default=1)
    def __str__(self):
        return 'alerte_'+ str(self.id)+ '_Wifi'
class AlertePoubelle(models.Model):
    disfonction=models.BooleanField(default=True)
    SOSMessage=models.TextField(max_length=150)
    poubelle=models.ForeignKey('Poubelle',on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.ForeignKey(Profile,on_delete=models.SET_NULL,editable=False,null=True,default=1)
    def __str__(self):
        return 'alerte_'+ str(self.id)+ '_Poubelle'

class AlerteJardin(models.Model):
    disfonction=models.BooleanField(default=True)
    SOSMessage=models.TextField(max_length=150)
    verdure=models.ForeignKey(TrameVerte,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.ForeignKey(Profile,on_delete=models.SET_NULL,editable=False,null=True,default=1)
    def __str__(self):
        return 'alerte_'+ str(self.id)+ '_Vert'

class AlerteReposoir(models.Model):
    disfonction=models.BooleanField(default=True)
    SOSMessage=models.TextField(max_length=150)
    repos=models.ForeignKey(Reposoir,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.ForeignKey(Profile,on_delete=models.SET_NULL,editable=False,null=True,default=1)
    def __str__(self):
        return 'alerte_'+ str(self.id)+ '_Repos'

class AlerteGenerale(models.Model):
    disfonction=models.BooleanField(default=True)
    SOSMessage=models.TextField(max_length=150)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.ForeignKey(Profile,on_delete=models.SET_NULL,editable=False,null=True,default=1)
    def __str__(self):
        return 'alerte_'+ str(self.id)+ '_Campus'
