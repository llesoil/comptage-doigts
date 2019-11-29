sudo systemctl restart nginx
sudo systemctl restart daphne
#gunicorn --certfile=./keys/comptage.crt --keyfile=./keys/comptage.key --bind 131.254.101.229 app.wsgi:application
