from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    """ Exemple de page non valide au niveau HTML pour que l'exemple soit concis """
    return HttpResponse("""
        <html>
	<head>
		<title>Accueil audio</title>	
	 	<meta http-equiv="Content-Type" content="text/plain;text/javascript;text/css;charset=utf-8" />
	</head>
	<body>
		<h2>
			Bienvenue sur la page reconnaissance de dessin!
			<p>
				<a href='one_hand'>Dessiner!</a>
			</p>
		</h2>	
	</body>
        </html>
    """)

def simple(request):
    return render(request, 'draw/simple.html')

