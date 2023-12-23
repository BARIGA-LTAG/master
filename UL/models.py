from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.gdal.libgdal import lgdal
###################################
import geopandas as gpd
from pyproj import Proj, transform

class CodeLatLonGeom():
    def lat_lon_par_geometrie(self, *args, **kwargs):
        """Mettre à jour les coordonnées lat et lon à partir de la géométrie"""
        # Définir les systèmes de coordonnées
        utm = Proj(proj="utm", zone=31, ellps="WGS84")
        wgs84 = Proj(proj="latlong", datum="WGS84")
        if self.geometrie and self.lat is None and self.lon is None:
            #conversion par pyproj
            self.lon, self.lat = transform(utm, wgs84,self.geometrie.x, self.geometrie.y)
            super().save(*args, **kwargs) 
   
    def ajout_geometrie_par_lat_lon(self):
        """Met à jour le champ geometrie à partir des champs lat et lon."""
        if self.lat is not None and self.lon is not None:
            # Convertit les coordonnées de WGS 84 à EPSG 32631
            pnt = Point(self.lon, self.lat, srid=4326)
            self.geometrie = pnt.transform(32631, clone=True)
            super().save()  # Enregistre les modifications
 # Utilisez la méthode save pour enregistrer les modifications et appeler ajout_geometrie_par_lat_lon
   # save en fonction du cas
    def save(self, *args, **kwargs):
        if self.lat is None and self.lon is None:
            self.lat_lon_par_geometrie(*args, **kwargs)
        else:
            self.ajout_geometrie_par_lat_lon()
        super().save(*args, **kwargs)
# les deux fonctions suivant sapplique a lat et lon si necessaire
    def get_lat_as_string(self):
        return str(self.lat).replace(',', '.')

    def get_lon_as_string(self):
        return str(self.lon).replace(',', '.')

class Limite(models.Model):
    nom = models.CharField(max_length=50)
    aire = models.FloatField(default=0)
    lon = models.FloatField(blank=True,null=True)
    lat = models.FloatField(blank=True,null=True)
    geometrie = models.PolygonField(srid=32631)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom

    class Meta:
        verbose_name="Limite"

    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  # Met à jour l'aire en fonction de la géométrie
        if self.geometrie.centroid:  # Vérifie si la géométrie a un point central
            self.lon, self.lat = self.geometrie.centroid.x, self.geometrie.centroid.y
        super().save(*args, **kwargs)

class Zone_UL(models.Model):
    nom = models.CharField(max_length=50)
    aire = models.FloatField(default=0)
    lon = models.FloatField(blank=True,null=True)
    lat = models.FloatField(blank=True,null=True)
    limite=models.ForeignKey(Limite,on_delete=models.PROTECT,default=Limite,null=True) 
    geometrie = models.MultiPolygonField(srid=32631)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Zone"
        verbose_name_plural="Zones"
    
    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  # Met à jour l'aire en fonction de la géométrie
        if self.geometrie.centroid:  # Vérifie si la géométrie a un point central
            self.lon, self.lat = self.geometrie.centroid.x, self.geometrie.centroid.y
        super().save(*args, **kwargs)
    
CAMP=(
        ('NORD', ('Campus Nord')),
        ('SUD', ('Campus Sud')),
    )  
TYPES_A=(
        ('PBL', ('Poubele')),
        ('FOS', ('Fosse septique')),
    )
class Assainissement(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    lat=models.FloatField(blank=True,null=True)
    lon=models.FloatField(blank=True,null=True)
    type=models.CharField(choices=TYPES_A)
    fonctionnel=models.BooleanField(default=True)
    secteur=models.CharField(choices=CAMP,blank=True,null=True)
    precision=models.TextField(max_length=300,blank=True,null=True)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE # CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    geometrie=models.PointField(blank=True,null=True,srid=32631)
    accuracy = models.FloatField(blank=True, null=True)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False) #nouveau
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)#nouveau
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Assainissement"
        verbose_name_plural="Assainissements"

    
USAGE=(
        ('COM', ('Commercial')),
        ('SANT', ('Sanitaire')),
        ('SOS', ('Sociale')),
        ('PED', ('Pédagogique')),
        ('CUL', ('Culturelle')),
    )
class Kiosque(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    lat=models.FloatField(blank=True,null=True)
    lon=models.FloatField(blank=True,null=True)
    accuracy = models.FloatField(blank=True, null=True)
    usage=models.CharField(choices=USAGE)
    fonctionnel=models.BooleanField(default=True)
    secteur=models.CharField(choices=CAMP)
    precision=models.TextField(max_length=300,null=True,blank=True)
    date_creation=models.DateField(blank=True,null=True)
    image=models.ImageField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom

    class Meta:
        verbose_name="Kiosque"
        verbose_name_plural="Kiosques"


LAMP=(
        ('CEET', ('Energie Hydrolique')),
        ('SOLAR', ('Energie solaire')),
    ) 
PROP=(
        ('CEET', ('CEET')),
        ('SOLAR', ('Solaire')),
    ) 
class Lampadaire(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    lat=models.FloatField(blank=True)
    lon=models.FloatField(blank=True)
    accuracy = models.FloatField(blank=True, null=True)
    type=models.CharField(choices=PROP)
    fonctionnel=models.BooleanField(default=True)
    energie=models.CharField(choices=LAMP,max_length=7)
    secteur=models.CharField(choices=CAMP,max_length=11)
    precision=models.TextField(max_length=300,null=True,blank=True)
    date_creation=models.DateField(blank=True,null=True)
    loisir = models.ForeignKey('Loisir', on_delete=models.SET_NULL,blank=True,null=True,related_name="lamp_loisir")# CLEE # CLEE
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE # CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    route = models.ForeignKey('Voirie', on_delete=models.SET_NULL,blank=True,null=True,related_name="lamp_eau")# CLEE
    plan_eau = models.ForeignKey('PlanEau', on_delete=models.SET_NULL,blank=True,related_name="lamp_plan_eau",null=True)# CLEE
    espace_vert = models.ForeignKey('EspaceVert', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    batiment = models.ForeignKey('Batiment', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Lampadaire"
        verbose_name_plural="Lampadaires"

ROL=(
        ('PUB', ('Publicitaire')),
        ('DIRC', ('Directionel')),
        ('SENS', ('Sensibilisation')),
    ) 

TYPP=(
        ('ROUT', ('Routier')),
        ('INFO', ('Informationel')),
    ) 

FORM=(
        ('CRC', ('Cercle')),
        ('CAR', ('Carré')),
        ('REC', ('Rectangle')),
        ('TRI', ('Triangle')),
        ('HEX', ('Hec/Hex/gone')),
    ) 
class Paneau(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=40)
    lat=models.FloatField(blank=True)
    lon=models.FloatField(blank=True)
    accuracy = models.FloatField(blank=True, null=True)
    type=models.CharField(choices=TYPP)
    forme=models.CharField(choices=FORM)
    fonctionnel=models.BooleanField(default=True)
    role=models.CharField(choices=ROL)
    secteur=models.CharField(choices=CAMP)
    precision=models.TextField(max_length=300,null=True,blank=True)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    route=models.ForeignKey('Voirie',on_delete=models.SET_NULL,blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    patking = models.ForeignKey('Parking', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Paneau"
        verbose_name_plural="Paneaux"
EAU=(
        ('FOR', ('Forage')),
        ('TDE', ('Tde')),
    ) 
class PointEau(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=40)
    lat=models.FloatField(blank=True)
    lon=models.FloatField(blank=True)
    accuracy = models.FloatField(blank=True, null=True)
    type=models.CharField(choices=EAU)
    fonctionnel=models.BooleanField(default=True)
    precision=models.TextField(max_length=300,null=True,blank=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    espace_vert = models.ForeignKey('EspaceVert', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    batiment = models.ForeignKey('Batiment', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Point d'eau"
        verbose_name_plural="Points d'eaux"
CAT=(
        ('BAN', ('Banc')),
        ('TABBAN', ('Table banc')),
        ('BAN_C', ('Banc couvert')),
        ('TABBAN_C', ('Table banc couvert')),
    ) 
MAT=(
        ('BOI', ('Bois')),
        ('BETON', ('Béton')),
    ) 
class Reposoir(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=40)
    lat=models.FloatField(blank=True)
    lon=models.FloatField(blank=True)
    accuracy = models.FloatField(blank=True, null=True)
    type=models.CharField(choices=CAT)
    materiel=models.CharField(choices=MAT)
    place=models.IntegerField()
    fonctionnel=models.BooleanField(default=True)
    toiture=models.BooleanField(default=False)
    precision=models.TextField(max_length=300,null=True,blank=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    espace_vert = models.ForeignKey('EspaceVert', on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Reposoir"
        verbose_name_plural="Reposoirs"

PTEL=(
        ('UL', ('Université de Lomé')),
        ('MOOV', ('Moov')),
        ('BANK', ('Banque')),
        ('GOUV', ('République Togolaise')),
        ('TGCOM', ('TogoCom')),
    )
TYP_TEL=(
        ('AS', ('Antenne Securité')),
        ('AR', ('Antenne réseau')),
        ('RAD', ('Antenne Radio')),
        ('wf', ('Wifi')),
    )
class Telecomminication(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=40)
    lat=models.FloatField(blank=True)
    lon=models.FloatField(blank=True)
    accuracy = models.FloatField(blank=True, null=True)
    type=models.CharField(choices=TYP_TEL)
    fonctionnel=models.BooleanField(default=True)
    precision=models.TextField(max_length=300,blank=True,null=True)
    secteur=models.CharField(choices=CAMP)
    propriete=models.CharField(choices=PTEL)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE # CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Telecommunication"
        verbose_name_plural="Telecommunications"

METEO=(
        ('SYNOP', ('Station Synoptique')),
        ('MANUAL', ('Antenne .....')),
    )
class Meteo(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    lat=models.FloatField(blank=True)
    lon=models.FloatField(blank=True)
    accuracy = models.FloatField(blank=True, null=True)
    type=models.CharField(choices=METEO) # a faire apres
    fonctionnel=models.BooleanField(default=True)
    precision=models.TextField(max_length=300)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Station météo"
        verbose_name_plural="Stations météos"

ARBR2=(
        ('NAT', ('Arbre Fruitier')),
        ('REBOI', ('Arbre Bois')),
    )
ARBR1=(
        ('NAT', ('Arbre naturel')),
        ('REBOI', ('Arbre reboisé')),
    )
class ArbreIsole(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    espece=models.CharField(max_length=80,blank=True, null=True)
    lat=models.FloatField(blank=True)
    lon=models.FloatField(blank=True)
    accuracy = models.FloatField(blank=True, null=True)
    type=models.CharField(choices=ARBR1)
    hauteur=models.FloatField(blank=True, null=True)
    diametre=models.FloatField(blank=True, null=True)
    precision=models.TextField(max_length=300)
    secteur=models.CharField(choices=CAMP)
    nature=models.CharField(choices=ARBR2)
    image=models.ImageField(blank=True, null=True)
    annee_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Arbre isolé"
        verbose_name_plural="Arbres isolés"

    
LOIS1=(
        ('SPOR', ('Sport')),
        ('SPECTACL', ('Evenement Culturel')),
    )
LOIS2=(
        ('B1', ('Footbal')),
        ('B2', ('Bascketbaal')),
        ('B3', ('Voleyball')),
        ('B4', ('Tenis')),
        ('D', ('Dance')),
        ('AUDI', ('Auditerium')),
    )
class Loisir(models.Model):
    nom = models.CharField(max_length=50)
    categorie = models.CharField(max_length=10,choices=LOIS1)
    lat=models.FloatField(blank=True,null=True)
    lon=models.FloatField(blank=True,null=True)
    accuracy = models.FloatField(blank=True, null=True)
    type_usage=models.CharField(choices=LOIS2)
    aire= models.FloatField(default=0)
    precision=models.TextField(max_length=300,blank=True,null=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    geometrie=models.MultiPolygonField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Espace loisir"
        verbose_name_plural="Espaces loisirs"
    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  # Met à jour l'aire en fonction de la géométrie
        if self.geometrie.centroid:  # Vérifie si la géométrie a un point central
            self.lon, self.lat = self.geometrie.centroid.x, self.geometrie.centroid.y
        super().save(*args, **kwargs)

VERT=(
        ('V.NAT', ('Vegetation naturel')),
        ('V.REB', ('Vegetation reboisé')),
        ('V.AMG', ('Espace vert aménagé')),
        ('BROU/C', ('Brousaille/Champs')),
        ('V.EXPERT', ('Vegetation expérimentale')),
    )
class EspaceVert(models.Model):
    nom = models.CharField(max_length=50)
    type = models.CharField(max_length=10,choices=VERT)
    lat=models.FloatField(blank=True,null=True)
    lon=models.FloatField(blank=True,null=True)
    accuracy = models.FloatField(blank=True, null=True)
    aire= models.FloatField(default=0)
    precision=models.TextField(max_length=300,blank=True,null=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    date_creation=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    batiment = models.OneToOneField('Batiment', on_delete=models.SET_NULL,blank=True,related_name="bat_jardin",null=True)# CLEE
    lampe = models.ForeignKey(Lampadaire, on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.MultiPolygonField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Espace vert"
        verbose_name_plural="Espaces verts"

    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  # Met à jour l'aire en fonction de la géométrie
        if self.geometrie.centroid:  # Vérifie si la géométrie a un point central
            self.lon, self.lat = self.geometrie.centroid.x, self.geometrie.centroid.y
        super().save(*args, **kwargs)

class ArbreReboise(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    espece=models.CharField(max_length=80,blank=True,null=True)
    lat=models.FloatField(blank=True)
    lon=models.FloatField(blank=True)
    date_reboise= models.DateTimeField(blank=True,null=True)
    accuracy = models.FloatField(blank=True, null=True)
    type=models.CharField(default="Arbre Reboisé")
    hauteur=models.FloatField(blank=True,null=True)
    diametre=models.FloatField(blank=True,null=True)
    precision=models.TextField(max_length=300)
    secteur=models.CharField(choices=CAMP)
    nature=models.CharField(choices=ARBR2)
    image=models.ImageField()
    annee_reboise=models.DateField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    zone_plantation = models.ForeignKey(EspaceVert, on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Arbre Reboisé"
        verbose_name_plural="Arbres Reboisés"

PARK=(
        ('CYCL', ('Cycliste')),
        ('AUTO', ('Automobile')),
    )
class Parking(models.Model):
    nom = models.CharField(max_length=50)
    lat=models.FloatField(blank=True,null=True)
    lon=models.FloatField(blank=True,null=True)
    accuracy = models.FloatField(blank=True, null=True)
    type=models.CharField(choices=PARK)
    aire= models.FloatField(default=0)
    camera=models.BooleanField(default=True)
    toiture=models.BooleanField(default=False)
    agent_securite=models.BooleanField(default=True)
    lampadaire=models.BooleanField(default=True)
    date_creation=models.DateTimeField(blank=True, null=True)
    precision=models.TextField(max_length=300,blank=True,null=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,blank=True,null=True)# CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,blank=True,null=True) # CLEE
    geometrie=models.MultiPolygonField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Parking"
        verbose_name_plural="Parkings"

    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  # Met à jour l'aire en fonction de la géométrie
        if self.geometrie.centroid:  # Vérifie si la géométrie a un point central
            self.lon, self.lat = self.geometrie.centroid.x, self.geometrie.centroid.y
        super().save(*args, **kwargs)

class PlanEau(models.Model):
    nom = models.CharField(max_length=50)
    lat=models.FloatField(blank=True,null=True)
    lon=models.FloatField(blank=True,null=True)
    accuracy = models.FloatField(blank=True, null=True)
    aire= models.FloatField(default=0,null=True)
    lampadaire=models.BooleanField(default=True)
    date_creation=models.DateTimeField(blank=True, null=True)
    precision=models.TextField(max_length=300,null=True,blank=True)
    secteur=models.CharField(choices=CAMP)
    image=models.ImageField(blank=True,null=True)
    zone=models.ForeignKey(Zone_UL,on_delete=models.SET_NULL,null=True) # CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    geometrie=models.MultiPolygonField(srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Plan d'eau"
        verbose_name_plural="Plans d'eaux"

    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  # Met à jour l'aire en fonction de la géométrie
        if self.geometrie.centroid:  # Vérifie si la géométrie a un point central
            self.lon, self.lat = self.geometrie.centroid.x, self.geometrie.centroid.y
        super().save(*args, **kwargs)

NIVO=(
        ('RE', ('Rez-de-chaussé')),
        ('N1', ('Niveau 1')),
        ('N2', ('Niveau 2')),
        ('N3', ('Niveau 3')),
        ('N4', ('Niveau 4')),
        ('N5', ('Niveau 5')),
        ('N6', ('Niveau 6')),
        ('N7', ('Niveau 7')),
        ('N8', ('Niveau 8')),
    )
BATRIO=(
        ('INDUS', ('Materiaux industriels')),
        ('ECOLO', ('Materiaux ecologique')),
    )
AERA=(
        ('VENT', ('Ventilation')),
        ('CLIM', ('Climatisation')),
        ('NUL', ('NEANT/Naturel')),
    )
TOIT=(
        ('AL', ('Dallé')),
        ('TUL', ('TULLE')),
        ('TOLA', ('Tôle Aluminium')),
        ('TOLZ', ('Tôle zin 0.5')),
    )
NATBAT=(
        ('CHANT', ('En Chantier')),
        ('ACHEV1', ('Achevé fonctionnel')),
        ('ACHEV2', ('Achevé Non fonctionnel')),
    )
CATEGORIES = [
    ("administratif", "Administratif"),
    ("pedagogique", "Pédagogique"),
    ("commercial", "comercial"),
    ("residentiel", "residentiel"),
]

TYPFORMA=(
        ('PRO', ('Professionnelle')),
        ('RECH', ('Recherche')),
    )
DOFORMA=(
        ('D1_POLY', ('Hybride/Polyvalent')),
        ('D2_SAN', ('Santé')),
        ('D3_ECO', ('Economie')),
        ('D4_ENV', ('Environnement')),
        ('D5_HS', ('Homme/Societé')),
         ('D6_SPOR', ('Sport')),
        ('D7_INFO', ('Informatique')),
         ('D8_AGRO', ('Agronomie')),
        ('D9_LANG', ('Langue')),
         ('D10_COMM', ('Communication')),
        ('D11_DROI', ('Droit/Politique')),
    )

CHAIZ=(
        ('BOI', ('Chaise Bois')),
        ('PLAS', ('Chaise Plastique')),
         ('FAUT', ('Chaise Fauteil')),
    )
class Batiment(models.Model):
    nom = models.CharField(max_length=60,null=True)
    lat=models.FloatField(blank=True,null=True)
    lon=models.FloatField(blank=True,null=True)
    accuracy = models.FloatField(blank=True, null=True)
    aire= models.FloatField(default=0)
    adresse= models.CharField(max_length=200,null=True)
    camerasurvaillance=models.BooleanField(default=False)
    extinteur=models.BooleanField(default=False)
    internet=models.BooleanField(default=False)
    renove=models.BooleanField(default=False)
    nature=models.CharField(choices=NATBAT) #faire un choice ou comment
    aeration= models.CharField(max_length=10,choices=AERA,)
    date_construi=models.DateField(blank=True,null=True)
    electricite=models.BooleanField(default=True)
    secteur=models.CharField(choices=CAMP,max_length=19)
    toilette=models.BooleanField(default=False)
    toiture= models.CharField(max_length=100,choices=TOIT)
    categorie = models.CharField(max_length=50, choices=CATEGORIES, null=True) #nouveaute
    nbre_niveau= models.CharField(choices=NIVO,null=True)
    materiaux= models.CharField(max_length=10,choices=BATRIO,null=True)
    image=models.ImageField(blank=True,null=True)
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,null=True)# CLEE # CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    geometrie=models.MultiPolygonField(srid=32631,blank=True,null=True)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
#class BatimentAdministratif(Batiment):
    #batiment = models.OneToOneField(Batiment, on_delete=models.CASCADE, primary_key=True)
    nb_bureaux = models.PositiveIntegerField(default=0)
    type_service= models.CharField(max_length=70,blank=True,null=True)################
    heure_ouverture=models.TimeField(blank=True,null=True)
    heure_fermeture=models.TimeField(blank=True,null=True)
#class BatimentPedagogique(Batiment):
    nb_salle = models.PositiveIntegerField(default=0,blank=True,null=True)
    nb_chaise = models.PositiveIntegerField(default=0,blank=True,null=True)
    type_banc=models.CharField(choices=CHAIZ, max_length=30,blank=True,null=True)####
    kit_informatique=models.BooleanField(default=False)
    type_formation=models.CharField(choices=TYPFORMA,max_length=30,blank=True,null=True)#########
    domaine_formation=models.CharField(choices=DOFORMA,max_length=30,blank=True,null=True)####
#class BatimentAdminPedago(Batiment):
    nb_salle = models.PositiveIntegerField(default=0)
    nb_chaise = models.PositiveIntegerField(default=0)
#class BatimentCommercial(Batiment):
    nb_employe = models.PositiveIntegerField(default=0)
    type_commerce= models.CharField(max_length=60,blank=True,null=True)
#class BatimentResidentiel(Batiment):
    nb_appartement = models.PositiveIntegerField(blank=True,null=True)
    loyer_mensuale= models.FloatField(blank=True,null=True)
    lit=models.BooleanField(default=False)
    cuisine=models.BooleanField(default=False)
    eau=models.BooleanField(default=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Batiment"
        verbose_name_plural="Batiments"

    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  # Met à jour l'aire en fonction de la géométrie
        if self.geometrie.centroid:  # Vérifie si la géométrie a un point central
            self.lon, self.lat = self.geometrie.centroid.x, self.geometrie.centroid.y
        super().save(*args, **kwargs)


CAMERA=(
        ('RGB', ('RGB')),
        ('IR', ('InfraRouge')),
    )
class Camera(CodeLatLonGeom,models.Model):
    nom=models.CharField(max_length=50)
    lat=models.FloatField(null=True,blank=True)
    lon=models.FloatField(null=True,blank=True)
    date_instal=models.DateField(null=True,blank=True)
    secteur=models.CharField(max_length=11,choices=CAMP)
    type=models.CharField(max_length=5,choices=CAMERA)
    fonctionnel=models.BooleanField(default=True)
    batiment=models.ForeignKey(Batiment,on_delete=models.SET_NULL,null=True,related_name="camera_bat")
    parking=models.ForeignKey(Parking,on_delete=models.SET_NULL, null=True, related_name="camera_park")
    zone = models.ForeignKey(Zone_UL, on_delete=models.SET_NULL,blank=True,null=True)# CLEE # CLEE
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL,null=True) # CLEE
    geometrie=models.PointField(srid=32631)
    date_collecte=models.DateTimeField( auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nom
    class Meta:
        verbose_name="Camera"
        verbose_name_plural="Cameras"

TYP_ROUT=(
        ('B', ('Bitumé')),
        ('P', ('Pavé')),
        ('T', ('Non Révetue')),
    )
class Voirie(models.Model):
    nom = models.CharField(max_length=100)
    lat=models.FloatField(blank=True)
    lon=models.FloatField(blank=True)
    date_construc=models.DateTimeField(blank=True, null=True)
    largeur= models.FloatField(default=0)
    adresse = models.CharField(max_length=200)
    longueur= models.FloatField(default=0)
    Paneaux=models.BooleanField(default=True)
    lampadaire=models.BooleanField(default=True)
    limite=models.ForeignKey(Limite,on_delete=models.SET_NULL, null=True, related_name="voirie_limite") # CLEE
    revetement= models.CharField(max_length=10,choices=TYP_ROUT)
    geometrie = models.MultiPolygonField(null=True, srid=32631)
    date_collecte=models.DateTimeField(auto_now_add=True, editable=False)
    agent_collecteur=models.CharField(max_length=50,blank=True, null=True)
    info_modifier_le = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name="Route"
        verbose_name_plural="Routes"

    def calcul_aire(self):
        return self.geometrie.area
    
    def save(self, *args, **kwargs):
        self.aire = self.calcul_aire()  # Met à jour l'aire en fonction de la géométrie
        if self.geometrie.centroid:  # Vérifie si la géométrie a un point central
            self.lon, self.lat = self.geometrie.centroid.x, self.geometrie.centroid.y
        super().save(*args, **kwargs)
####################
##############
from multiselectfield import MultiSelectField
# LES ALERTES

CHOICES = (
        ('choix1', 'Climatisation'),
        ('choix2', 'Vitilateur'),
        ('choix3', 'Ampoule'),
        ('choix3', 'Sonorisation'),
        ('choix3', 'Table/Banc'),
    )
class AlerteBatiment(models.Model):
    disfonction=models.BooleanField(default=False)
    lesPennes= MultiSelectField(choices=CHOICES,max_length=300)
    SOSMessage=models.TextField(max_length=300)
    batiment=models.ForeignKey(Batiment,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.CharField(max_length=70)
   
class AlerteLampadaire(models.Model):
    disfonction=models.BooleanField(default=False)
    SOSMessage=models.TextField(max_length=300)
    lampadaire=models.ForeignKey(Lampadaire,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.CharField(max_length=70)

class AlertePointEau(models.Model):
    disfonction=models.BooleanField(default=False)
    SOSMessage=models.TextField(max_length=300)
    point_eau=models.ForeignKey(PointEau,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)

class AlerteWifi(models.Model):
    disfonction=models.BooleanField(default=False)
    SOSMessage=models.TextField(max_length=300)
    wifi=models.ForeignKey(Telecomminication,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.CharField(max_length=70)

class AlertePoubelleFosse(models.Model):
    disfonction=models.BooleanField(default=False)
    SOSMessage=models.TextField(max_length=300)
    poubellefosse=models.ForeignKey(Assainissement,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.CharField(max_length=70)

class AlerteJardin(models.Model):
    disfonction=models.BooleanField(default=False)
    SOSMessage=models.TextField(max_length=300)
    verdure=models.ForeignKey(EspaceVert,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.CharField(max_length=70)

class AlerteReposoir(models.Model):
    disfonction=models.BooleanField(default=False)
    SOSMessage=models.TextField(max_length=300)
    repos=models.ForeignKey(Reposoir,on_delete=models.SET_NULL,null=True)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.CharField(max_length=70)

class AlerteGenerale(models.Model):
    disfonction=models.BooleanField(default=False)
    SOSMessage=models.TextField(max_length=300)
    date_alerte=models.DateTimeField(auto_now_add=True, editable=False)
    auteur= models.CharField(max_length=70)
    #general=models.OneToOneField(Gestionaire,on_delete=models.SET_NULL)## je creer un groupe gestionaire
