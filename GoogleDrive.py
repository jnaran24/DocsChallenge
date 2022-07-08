from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from getpass import getpass
from cryptography.fernet import Fernet

directorio_credenciales = 'credentials_module.json'

# INICIAR SESION
def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credenciales)
    else:
        gauth.Authorize()
    
    return GoogleDrive(gauth)

# METODO EJECUTOR 
def insertDataBase():
    # Se pide al usuario ingresar el id de la unidad/carpeta del Drive
    idUnidad = input('id de unidad/carpeta: ')
    # Genera una clave en formato de secuencia de bytes:
    key = Fernet.generate_key()
    objeto_cifrado = Fernet(key)
    dbAccess = objeto_cifrado.encrypt(str.encode(getpass())) # Encriptamos la pass de las Bases de datos

    # ----------------------CONEXIÓN A LA BASE DE DATOS SQL--------------------------------
    try:        
        connection=psycopg2.connect(
            user ='postgres', 
            host = 'localhost', 
            password = objeto_cifrado.decrypt(dbAccess).decode(), # Desencriptamos y decodificamos la pass
            port=5432) # Datos basicos para conexión con la BD
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # Autocommit a las sentencias ejecutadas
        cursor = connection.cursor() # Cursor de la BD principal

        try:
            cursor.execute('CREATE DATABASE melichallenge') # Creamos la BD
        except:
            print("La base de datos ya se encuentra creada")
            pass
        
        cursor.execute('SELECT current_database()') # Brindamos información de la base de datos principal
        for row in cursor.fetchall():
            print('the main database is: ',row)
        print('')
        cursor.close() # Cerramos cursos y conexión de la base de datos principal
        connection.close()
        
        connection2=psycopg2.connect( # Nos conectamos a la BD que creamos
            user ='postgres', 
            database='melichallenge', 
            host = 'localhost', 
            password = objeto_cifrado.decrypt(dbAccess).decode(), # Desencriptamos y decodificamos la pass
            port=5432)
        cursor2 = connection2.cursor() # Cursor de la nueva BD
        connection2.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # Autocommit a las sentencias ejecutadas

        try: # Intentamos crear las tablas, principal y historicos
            cursor2.execute('''CREATE TABLE principal(
                nombre_archivo VARCHAR,
                extension_archivo VARCHAR(5),
                propietario VARCHAR,
                visibilidad VARCHAR(8),
                fecha_modificacion DATE
            );
            ALTER TABLE principal ADD UNIQUE (nombre_archivo)''')
            cursor2.execute('''CREATE TABLE historicos(
                nombre_archivo VARCHAR,
                extension_archivo VARCHAR(5),
                propietario VARCHAR,
                visibilidad VARCHAR(8),
                fecha_modificacion DATE
            );
            ALTER TABLE principal ADD UNIQUE (nombre_archivo)''')
        except:
            print("las tablas que intenta crear ya existen")
            pass

        resultado = []
        credenciales = login() #Nos autenticamos
        # Se realiza el query para obtener los archivos de la carpeta contenedora
        lista_archivos = credenciales.ListFile({'q': "'{0}' in parents and trashed=false".format(idUnidad)}).GetList()
        for f in lista_archivos:
            nombre = f['title'] # Nombre del archivo
            extension = nombre.split(".",1)[1] # Extension del archivo
            visibilidad = f['shared']
            fechaUltimaMod = f['modifiedDate']
            
            print('Nombre deel archivo:', nombre) #Nombre del archivo            
            print('Tipo archivo:', extension)
            print('ultima modificación:', fechaUltimaMod) #Fecha de modificación    
            atributos = f.metadata # Asignamos la metadata a una variable
            infoPropietario = atributos["owners"] # Asignamos la info del owner a una variable
            for variable in infoPropietario: # Recorremos esa info del owner
                try: # Archivo por archivo intentamos ingresar su información
                    cursor2.execute('''INSERT INTO principal (nombre_archivo,
                    extension_archivo,
                    propietario,
                    visibilidad,
                    fecha_modificacion)
                    VALUES('{0}','{1}','{2}','{3}','{4}');'''.format(
                        nombre,
                        extension,
                        variable["displayName"],
                        visibilidad,
                        fechaUltimaMod
                    ))
                except Exception as ex:
                    print(ex)
                    
                    cursor2.execute('''UPDATE principal 
                    SET extension_archivo='{0}',
                    propietario='{1}',
                    visibilidad='{2}',
                    fecha_modificacion='{3}' 
                    WHERE nombre_archivo = '{4}' '''.format(
                        extension,
                        variable["displayName"],
                        visibilidad,
                        fechaUltimaMod,
                        nombre
                    ))
                    pass            

            if(visibilidad == True): #True si visibilidad es publica, False si es privada
                #-----------SE ALMACENA EL REGISTRO EN TABLA HISTORICOS--------------------
                try:
                    cursor2.execute('''INSERT INTO historicos (nombre_archivo,
                    extension_archivo,
                    propietario,
                    visibilidad,
                    fecha_modificacion)
                    VALUES('{0}','{1}','{2}','{3}','{4}');'''.format(
                        nombre,
                        extension,
                        variable["displayName"],
                        visibilidad,
                        fechaUltimaMod
                    ))
                except Exception as ex:
                    print(ex)
                    pass

                #----------------SERVICIO DE EMAIL PARA NOTIFICACION-----------------------
                CLIENTE = "client_secrets.json"
                API_NAME = "gmail"
                API_VERSION = "v1"
                SCOPES = ["https://mail.google.com/"]

                service = Create_Service(CLIENTE, API_NAME, API_VERSION, SCOPES)
                mimeMessage = MIMEMultipart()
                mimeMessage["subject"] = "Notificación cambio de privacidad archivo de Google Drive"
                emailMsg = "Cordial saludo, este es un mensaje automatico para notificarte que el archivo {0} en Google Drive se encontraba con acceso publico y se ha cambiado a restringido".format(nombre)
                emailAccess = objeto_cifrado.encrypt(str.encode(variable["emailAddress"])) # Aseguramos el email del owner
                mimeMessage["to"] = objeto_cifrado.decrypt(emailAccess).decode() # Desencriptamos y decodificamos el email del owner para enviar el correo
                mimeMessage.attach(MIMEText(emailMsg, "plain"))
                raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
                message = service.users().messages().send(userId = "me", body = {"raw": raw_string}).execute()
                print(message)

                #---------------------SE ASIGNA VISIBILIDAD PRIVADA--------------------------
                gauth = GoogleAuth()
                drive = GoogleDrive(gauth) # authorization script
                file = drive.CreateFile({'id': f['id']}) # Se reemplaza el archivo existente (update)
                permission_list = file.GetPermissions() # Se obtienen los permisos del archivo
                for obj in permission_list: # Ciclo que recorre los permisos
                    for variable in infoPropietario: # Visitamos la data del owner
                        if obj.get('emailAddress') != objeto_cifrado.decrypt(emailAccess).decode(): # Si el email visitante no concuerda con el owner
                            file.DeletePermission(obj['id']) # Se restringe el permiso                             

            resultado.append(f)
        return resultado        
    except Exception as ex:
        print(ex)
    finally:
        cursor2.close()
        connection2.close() #Se cierra la conexión a la BD
        print("Conexión finalizada")




if __name__ == "__main__":
    insertDataBase()