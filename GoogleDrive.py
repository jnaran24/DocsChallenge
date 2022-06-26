from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

directorio_credenciales = 'credentials_module.json'

#INICIAR SESION
def login():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(directorio_credenciales)

    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(directorio_credenciales)
    else:
        gauth.Authorize()
    
    return GoogleDrive(gauth)

#CREAR ARCHIVO DE TEXTO SIMPLE
def buscar():
    resultado = []
    credenciales = login() #Nos autenticamos
    # Se realiza el query para obtener los archivos de la carpeta contenedora
    lista_archivos = credenciales.ListFile({'q': "'1cY1CM7x-K0XovdcxRI7sPuAzMcmsTPzE' in parents and trashed=false"}).GetList()
    for f in lista_archivos:
        
        print('Nombre deel archivo:', f['title']) #Nombre del archivo
        tipo = f['title'] #Tipo del archivo
        print('Tipo archivo:', tipo.split(".",1)[1])
        print('ultima modificación:', f['modifiedDate']) #Fecha de modificación    
        atributos = f.metadata
        infoPropietario = atributos["owners"]
        for variable in infoPropietario:
            print("owner:", variable["displayName"]) #Nombre del owner y email 
            print("email:", variable["emailAddress"])
        

        if(f['shared'] == True):
            CLIENTE = "client_secrets.json"
            API_NAME = "gmail"
            API_VERSION = "v1"
            SCOPES = ["https://mail.google.com/"]

            service = Create_Service(CLIENTE, API_NAME, API_VERSION, SCOPES)

            mimeMessage = MIMEMultipart()
            mimeMessage["subject"] = "Notificación cambio de privacidad Google Drive"
            nombreArchivo = f['title']
            emailMsg = "Cordial saludo, este es un mensaje automatico para notificarte que el archivo {0} en Google Drive se encontraba con acceso publico y se ha cambiado a restringido".format(nombreArchivo)
            mimeMessage["to"] = variable["emailAddress"]
            
            mimeMessage.attach(MIMEText(emailMsg, "plain"))
            raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            message = service.users().messages().send(userId = "me", body = {"raw": raw_string}).execute()
            print(message)
            gauth = GoogleAuth()
            drive = GoogleDrive(gauth) # authorization script
            file = drive.CreateFile({'id': f['id']}) # Se reemplaza el archivo existente (update)
            permission_list = file.GetPermissions() # Se obtienen los permisos del archivo
            for obj in permission_list: # Ciclo que recorre los permisos
                for variable in infoPropietario: # Visitamos la data del owner
                    if obj.get('emailAddress') != variable["emailAddress"]: # Si el email visitante no concuerda con el owner
                        file.DeletePermission(obj['id']) # Se restringe el permiso 
                        

        resultado.append(f)

    return resultado




if __name__ == "__main__":
    buscar()