# MELI Challenge

# Requisitos
1. Python 3.10.5 y pip
2. PostgreSQL 14.4 con su configuración inicial (poseer una contraseña y tener la base de datos por default)
3. A la aplicación se le implemento Docker, y se encuentra en un contenedor de DockerHub, sin embargo Google pide manualmente aceptar permisos de acceso y privilegio para envio de correos, por lo tanto, no se encuentra disponible para hacerle el run (https://hub.docker.com/repository/docker/ee106as45d68514f1/meli-challenge) Así que si se desea bajarlo por docker y hacer pull, se debe de tener en cuenta de contar con Docker en la maquina/ambiente virtual


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
![image](https://user-images.githubusercontent.com/32200374/176282401-dc0ab5d5-2dd0-49ab-a0a9-483fc4101722.png)

7. En caso de que la base de datos o las tablas ya existan, el programa nos avisará por consola
![image](https://user-images.githubusercontent.com/32200374/176282804-4859ce3b-9699-43cd-872b-355acfd6a0af.png)

8. En cada insert que haga a la base de datos, nos va a mostrar por cada registro el nombre de archivo, su tipo y fecha de ultima modificación por consola de la siguiente manera:
![image](https://user-images.githubusercontent.com/32200374/176284167-de6a16a5-0e5c-4549-8440-026d834b97a0.png)

9. En caso de que algún archivo este con visibilidad pública, se realiza el servicio de notificación vía correo electronico (Gmail service). La consola tambien nos proporciona información de la siguiente manera:
![image](https://user-images.githubusercontent.com/32200374/176284425-9f2aa6ad-f957-4bf7-affe-9a085a6c6169.png)

10. El correo electronico nos llega de la siguiente manera:
![image](https://user-images.githubusercontent.com/32200374/176284579-acd0ad47-cc61-4693-b903-59c5f12b1d54.png)

11. La base de datos desde el programa pgAdmin4 antes de ejecutar nuestro script se visualiza de la siguiente manera:
![image](https://user-images.githubusercontent.com/32200374/176285120-a9d1216d-92d0-406d-bac1-41e1195df107.png)
Podemos ver que existe ya una base de datos llamada postgres y es la que crea PostgreSQL por defecto cuando se descarga, instala e inicializa.


12. Podemos verificar despues de correr nuestro script, la creación de la base de datos nueva llamada (melichallenge) junto con sus dos tablas (principal: que recolecta toda la información sin registrros repetidos porque tiene una key la cual es su nombre_archivo) y la de (historicos: que guarda todos los registros de los archivos que en alguna corrida fueron públicos, tambien con el control de no ingresar repetidos con el mismo key que la tabla anterior)
Aqui vemos los registros de la tabla principal
![image](https://user-images.githubusercontent.com/32200374/176285713-aee3cddc-60f9-473c-984d-27d0c73ebd3f.png)

Aqui vemos los registros de la tabla historicos (Que fueron publicos y se setearon a privados y se le notifico al owner vía gmail del cambio)
![image](https://user-images.githubusercontent.com/32200374/176285876-87784c64-b5e9-4b1d-84af-8f241055a31c.png)


# Explicación del funcionamiento en codigo
- [x] Los modulos/librerias utilizadas fueron: "PyDrive2" (es una biblioteca contenedora de google-api-python-client que simplifica muchas tareas comunes de Google Drive API V2 y la autenticación como tal para Google y GoogleDrive), "Create_Service" es un metodo implementado en el script Google.py y utilizado por nuestrro script principal GoogleDrive.py (Es utilizado para crear un servicio de google dado un cliente, api_name, api_version y scopes. En nuestrro caso, como tenemos nuestras propias credenciales brindadas por Google en el archivo client_secrets.json que descargamos de https://console.cloud.google.com/apis/credentials?project=meli-challenge-354322 se las proporcionamos al servicio junto con el alcance https://mail.google.com/ para poder enviar correos electronicos con el API de gmail), "base64" (Utilizado para poder codificar todo el contenido del correo que vamos a enviar), "MIMEMultipart" y "MIMEText" (MIMEMultipart es un estándar de Internet que se utiliza para admitir la transferencia de uno o varios archivos adjuntos de texto y que no son de texto. Los archivos adjuntos que no son de texto pueden incluir archivos de gráficos, audio y video. MIMEText se utiliza para enviar correos electrónicos de texto.), "psycopg2" (Psycopg es el adaptador de base de datos PostgreSQL más popular para el lenguaje de programación Python. desarrollado principalmente en C como un envoltorio de libpq, lo que resulta en que sea eficiente y seguro. Cuenta con cursores del lado del cliente y del lado del servidor.), "getpass" (es una forma segura de solicitar la contraseña sin que se visualice en consola ), "cryptography" (por medio del modulo fernet podemos encriptar mediante una llave y un objeto cualquier texto)
 
