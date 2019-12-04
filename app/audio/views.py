from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
         <html>
	<head>
		<title>Accueil audio</title>	
	 	<meta http-equiv="Content-Type" content="text/plain;text/javascript;text/css;charset=utf-8" />
	  	{% load staticfiles %}
		<link type="text/css" rel="stylesheet" href="{% static 'css/home.css' %}" media="all"/>
	</head>
	<body>
		<h2>
			Bienvenue sur la page reconnaissance audio!
			<p>
				<a href='simple'>Débuter la reconnaissance audio!</a>
			</p>
		</h2>	
	</body>
        </html>
   """)

def one_hand(request):
    return render(request, 'audio/one_hand.html')
