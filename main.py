import psycopg2





    # ----------------------CONEXIÓN A LA BASE DE DATOS SQL--------------------------------
try:
    connection=psycopg2.connect(
        host='localhost',
        user='postgres',
        password='123456789',
        database='MELI-CHALLENGE'
    ) #Datos basicos para conexión con la BD

    # -------------------CONEXIÓN EXITOSA/VERSION COMPILADO--------------------------------
    print("Conexión exitosa")
    cursor=connection.cursor() #Creación del cursor para cambios en BD
    cursor.execute("SELECT version()") #Información de compilado
    row=cursor.fetchone()
    print(row)

    # -----------------------INSERT A LA TABLA INFORMACIÓN---------------------------------
    nombreArchivo = 'archivo4'
    propietario = 'Sebastian'
    #cursor.execute(
        # """INSERT INTO informacion(nombre_archivo,extension_archivo,propietario,visibilidad,fecha_modificacion) 
        # VALUES ('{0}','pdf','{1}','publica','2022-06-21')""".format(nombreArchivo,propietario))
    #connection.commit() #Confirmar la acción

    # -----------------------UPDATE A LA TABLA INFORMACIÓN---------------------------------
    #cursor.execute(
        #"""UPDATE informacion 
        #SET propietario = '{0}', extension_archivo = 'xml' 
        #WHERE propietario = 'juan'""".format(propietario))
    #connection.commit() #Confirmar la acción

    # -----------------------DELETE A LA TABLA INFORMACIÓN---------------------------------
    cursor.execute(
        """DELETE FROM informacion 
        WHERE nombre_archivo = 'archivo4'
        AND extension_archivo = 'pdf'
        AND propietario = 'Andres'
        """)
    connection.commit() #Confirmar la acción

    # -------------------------CONSULTA A TABLA INFORMACIÓN--------------------------------

    cursor.execute("SELECT * from informacion")
    rows=cursor.fetchall()
    for row in rows:
        print(row)
    print("Total de registros:", cursor.rowcount)
except Exception as ex:
    print(ex)
finally:
    connection.close() #Se cierra la conexión a la BD
    print("Conexión finalizada")