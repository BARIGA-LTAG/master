from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.

def renommer_image(instance,nom_image):
    """methode pour renommer le nom de la photo de prophile de chaque utilisateurs"""
    upload_to='images/'
    ext =nom_image.split('.')[-1]
    if instance.user.username:
        nom_image=f"photo/{instance.user.username}.{ext}"
    return os.path.join(upload_to,nom_image)

Etudiant,Enseignant,Autorite_UL='Etudiant','Enseignant','Autorite UL'
TYPE_USER=[
        (Etudiant,'Etudiant'),(Enseignant,'Enseignant'),(Autorite_UL,'Autorité UL')
    ]
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio=models.CharField(max_length=100,blank=True)
    photo=models.ImageField(upload_to=renommer_image,blank=True,null=True)
    type_profile=models.CharField(max_length=111,choices=TYPE_USER,default=Etudiant)
    def __str__(self):
        return self.user.username 
    
    # evenement et chat
    #culturel
    # cool ul
    #ect