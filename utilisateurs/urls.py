from django.urls import path
from .views import accueil,register,connecter,deconnecter
urlpatterns = [
    path('',accueil,name="accueil"),
    path('register',register,name="register"),
    path('connection',connecter,name="connection"),
    path('deconnection',deconnecter,name="deconnection"),

]