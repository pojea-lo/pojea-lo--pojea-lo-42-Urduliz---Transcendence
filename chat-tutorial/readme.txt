CHAT - TUTORIAL:

Pasos para hacer funcionar el chat:

Primero comprobar si están o no instalados los requirements.txt, en caso contrario: 'pip install -r requirements.txt'
Aconsejable hacerlo dentro de un entorno de python

-Paso-1: Averiguar si el puerto 6379 está ocupado
    sudo lsof -i -P | grep 6379

-Paso-2: Liberar puerto 6379 en caso de que lo este
    /etc/init.d/redis-server stop

-Paso-3: Lanzar servicio redis con docker:
    sudo docker run --rm -p 6379:6379 redis:7

-Paso-4: Lanzar servidor de Django
    python(3-si es necesario en tu entorno) manage.py runserver

-Paso-5: Conectarse en dos navegadores diferentes a la misma sala
    localhost:8000/chat

bibliografía:
    https://channels.readthedocs.io/en/latest/tutorial/part_1.html
