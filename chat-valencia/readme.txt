Este es un chat que funciona en un servidor asincrono y con base de datos relacional para los datos de los usuarios y base de datos de memoria para los chats.

#Versiones:
V0 - Versión tal cual viene de la web: Sin salas. Sin guardado de conversaciones. Sin frontend separado. Con usuarios en base de datos. 

#Pasos para hacer funcionar el chat:

Primero comprobar si están o no instalados los requirements.txt, en caso contrario: 'pip install -r requirements.txt'
Aconsejable hacerlo dentro de un entorno de python

-Paso-1: Averiguar si el puerto 6379 está ocupado
    sudo lsof -i -P | grep 6379

-Paso-2: Liberar puerto 6379 en caso de que lo este
    /etc/init.d/redis-server stop

-Paso-3: Lanzar servicio redis y base de datos relacional con docker-compose:
    sudo docker-compose up -d

-Paso-4: Lanzar servidor de Django
    python(3-si es necesario en tu entorno) manage.py runserver

-Paso-5: Conectarse en dos navegadores diferentes a la misma sala
    localhost:8000/chat

bibliografía:
    https://programadorwebvalencia.com/django-chat-usando-websockets-con-salas-y-async/