from django.http import HttpResponse

def start_page(request):
    html = "<html><body>Bienvenue sur le site!</body></html>"
    return HttpResponse(html)
