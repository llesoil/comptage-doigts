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
			Bienvenue sur la page reconnaissance d'images!
			<p>
				<a href='one_hand'>Reconnaissance à une main!</a>
			</p>			
                        <p>
				<a href='two_hands'>Reconnaissance à deux mains!</a>
			</p>
		</h2>	
	</body>
</html>
    """)

def one_hand(request):
    return render(request, 'picture/one_hand.html')

def two_hands(request):
    return render(request, 'picture/two_hands.html')

