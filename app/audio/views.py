from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <h1>Bienvenue, vous êtes sur l'accueil de la détection audio!</h1>
        <p>Merci de visiter note page!</p>
    """)

def one_hand(request):
    return render(request, 'audio/one_hand.html')