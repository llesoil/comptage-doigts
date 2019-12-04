sudo systemctl restart nginx
sudo systemctl restart daphne
#gunicorn --certfile=./keys/comptage.crt --keyfile=./keys/comptage.key app.wsgi:application
