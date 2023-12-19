from django.shortcuts import render
from django.urls import reverse
from .formulaire import UserForm, ProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def accueil(request):
    return render(request,'utilisateurs/index.html')

def register(request, *args, **kwargs):
    enregistrer = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            enregistrer = True
            return HttpResponseRedirect('connection')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    
    context = {
        'enregistrer': enregistrer,
        'form1': user_form,
        'form2': profile_form,
    }
            
    return render(request, 'utilisateurs/register.html', context)

    
def connecter(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        #on cree une variable user
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login (request,user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("l'Utilisateur est desactivé")
        else:
            return HttpResponse("veillez ecrire correctement votre nom et votre mot de passe")
    else:
        return render(request,'utilisateurs/login.html')
    
@login_required
def deconnecter(request):
    logout(request)
    return HttpResponseRedirect('/')

