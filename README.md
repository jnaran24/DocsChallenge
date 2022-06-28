# MELI Challenge

# Requisitos
1. Python 3.10.5 y pip
2. PostgreSQL 14.4 con su configuración inicial (poseer una contraseña y tener la base de datos por default)
3. A la aplicación se le implemento Docker, y se encuentra en un contenedor de DockerHub, sin embargo por compatibilidad con servicio de autenticación de Google, no se encuentra disponible para hacerle el run (https://hub.docker.com/repository/docker/ee106as45d68514f1/meli-challenge) Así que si se desea hacer pull, se debe de tener en cuenta de contar con Docker en la maquina/ambiente virtual


# Funcionamiento
Para poder ejecutar localmente el programa se requiere:
1. Al no correrla en docker sino local, instalamos modulos y librerias con el siguiente comando : "pip install pydrive2 psycopg2 google-auth-oauthlib cryptography requests"
2. Ejecutar el programa QuickStart, con el comando "python QuickStart.py" Este programa ejecutará un serivio de Google para poder obtener un token necesario de permiso a la anterior Unidad/Carpeta. por lo tanto se abrira una pestaña en su navegador predeterminado, pidiendole iniciar sesión de Google y luego aceptar las 2 condiciones siguientes

![image](https://user-images.githubusercontent.com/32200374/176259664-e1379d30-fbcf-4f7f-84e0-9063b77667f8.png)

![image](https://user-images.githubusercontent.com/32200374/176259734-7675925a-9487-4567-937a-39b6da580438.png)

En la consola nos aparece el mensaje "Authentication successful."

3. En este punto podemos ejecutar el programa principal con el comando "python GoogleDrive.py" el cual hará toda la logica.
4. Nos pedira inicialmente colocar el id de la carpeta o unidad Drive que se quiere obtener toda la información de los archivos que se encuentren allí.  (Este id se puede ver cuando estamos en el navegador, mediante la URL de la unidad/carpeta). Al ingresarlo damos enter

Seguidamente nos va a pedir el Password de la base de datos que colocamos en la configuración inicial del Postgresql. Al ingresarlo damos enter

![image](https://user-images.githubusercontent.com/32200374/176264568-e1f539a0-4bc7-4378-8b5c-1c62f025e312.png)

5. Empezará a correr todo el programa principal
6. Si se abre una ventana en el navegador pidiendo permisos de Google en el proceso es porque hay archivo(s) publico(s) y se requiere permiso para poder mandar los correos con las notificaciones, los aceptamos y nos aparecerá este mensaje 


 
