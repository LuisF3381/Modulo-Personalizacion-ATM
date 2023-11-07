from fastapi import APIRouter, HTTPException
import MySQLdb
from config.db import db_config
from routes.userModel_route import get_perfil_by_id_user_model 
from datetime import datetime, timedelta


algoritmo_r = APIRouter()


@algoritmo_r.post("/actualizar_user_model/{user_model_id}")
def actualiza_user_model(user_model_id: int):
    # Primero obtenemos el perfil del usuario
    perfil = get_perfil_by_id_user_model(user_model_id)
    
    # Vemos de que perfil se trata con el fin de poder iniciar la rutina algoritmica correspondiente
    if perfil.descripcion == "Perfil Cliente Frecuente":
        # Revisamos las acciones personalizables
        preferencias = perfil.preferencias
        
        for preferencia, valor in preferencias.dict().items():
            # Revisamos la ultima transaccion
            if preferencia == "preferenciaUltimaOp" and valor:
                calcula_ultima_operacion(user_model_id)
        
        return "Perfil Cliente Frecuente Actualizado"
    
    if perfil.descripcion == "Perfil Cliente Ocasional":        
        # Revisamos las acciones personalizables
        preferencias = perfil.preferencias

        # Iteramos sobre las preferencias y llamamos a la funcion de calculo correspondiente
        for preferencia, valor in preferencias.dict().items():
            # Revisamos el retiro rapido al ser perfil ocasional
            if preferencia == "preferenciaRetiroRap" and valor:
                calcula_retiro_rapido(user_model_id)
    
        return "Perfil Cliente Ocasional Actualizado"
    
    if perfil.descripcion == "Perfil Cliente Senior":
        return "GEEE"
    
    
    
    
    return perfil
    
    return {"mensaje": "User Model correctamente actualizado"}


# PARA LA ULTIMA OPERACION
def calcula_ultima_operacion(user_model_id: int):
    try:
        # Create a connection to the database
        conn = MySQLdb.connect(**db_config)   
        cursor = conn.cursor()
        
        # Consulta SQL
        query = """
            SELECT *
            FROM operacion
            WHERE user_model_id = %s
            ORDER BY fechaOperacion DESC
            LIMIT 1;
        """
        
        cursor.execute(query, (user_model_id,))
        result = cursor.fetchone()
        
        if result:
            # Convertir el resultado a un diccionario para devolverlo como JSON
            column_names = [desc[0] for desc in cursor.description]
            result_dict_model_op = dict(zip(column_names, result))
            print(result_dict_model_op)
            operacion_nombre= result_dict_model_op.get('tipoOperacion', '')
            # Se procede a realizar la insercion
            resulto_insertado = insertar_en_operation_model_y_desactivar(result_dict_model_op, "UltimaOp", user_model_id, operacion_nombre)
            conn.close()
        else:
            conn.close()
            return -1
            
    except Exception as e:
        print(e)    

    return -1 



# PARA LOS RETIROS RAPIDOS
# Funcion que calcula el retiro rapido para los clientes ocasionales
def calcula_retiro_rapido(user_model_id: int):
    # Primero verificaremos que en la tabla model operation exista algun registro (o no) de un retiro rapido
    try:
        # Create a connection to the database
        conn = MySQLdb.connect(**db_config)   
        cursor = conn.cursor()
        
        # Consulta SQL
        query = """
            SELECT *
            FROM operation_model
            WHERE user_model_id = %s
            AND descripcion = "RetiroRap"
            AND activo = TRUE;
        """
        cursor.execute(query, (user_model_id,))
        result = cursor.fetchone()
        
        if result:
            # Convertir el resultado a un diccionario para devolverlo como JSON
            column_names = [desc[0] for desc in cursor.description]
            result_dict_model_op = dict(zip(column_names, result))
            
            # Al existir devemos evaluar si hay necesidad de cambiarlo o no
            # Si es necesario cambiarlo entonces se hara un insert y se pondra en activo este model
            #print("Model operation actual", result_dict_model_op)

            # Traemos el retiro mas utilizado
            result_retiro_mas_usado = retiro_mas_empleado(user_model_id)
            #print("Resultado de retiro mas usado",result_retiro_mas_usado)
            
            # Traemos los 3 ultimos retiros  
            result_3_ult_retiros = ultimos_3_retiros(user_model_id)
            #print("Resultado de ultimas 3 operaciones",result_3_ult_retiros)
            
            if result_3_ult_retiros != -1:
                result_actualizacion = insertar_en_operation_model_y_desactivar(result_3_ult_retiros, "RetiroRap", user_model_id, "Retiro")
            else:
                # Comparamos el operation model actual con el mas empleado
                print("Aqui deberia ir la logica")
                son_diferentes = objetos_diferentes(result_dict_model_op, result_retiro_mas_usado)
            
                # Aqui insertamos o no el objeto
                if son_diferentes:
                    #print("Insertamos el nuevo operation model")
                    result_actualizacion = insertar_en_operation_model_y_desactivar(result_retiro_mas_usado, "RetiroRap", user_model_id, "Retiro")

            
        else:
            # En caso no haber registros debe tomarse de la tabla operacion el ultimo retiro realizado por el usuario
            # Hacemos un query a la tabla 
            conn = MySQLdb.connect(**db_config)   
            cursor = conn.cursor()
            
            # Consulta SQL para obtener el último retiro
            query_retiro = """
                SELECT *
                FROM operacion
                WHERE user_model_id = %s
                AND tipoOperacion = "Retiro"
                ORDER BY fechaOperacion DESC
                LIMIT 1;
            """
            cursor.execute(query_retiro, (user_model_id,))
            ultimo_retiro = cursor.fetchone()
            
            
            if ultimo_retiro:
                # Convertir el resultado a un diccionario para devolverlo como JSON
                column_names = [desc[0] for desc in cursor.description]
                ultimo_retiro_dict = dict(zip(column_names, ultimo_retiro))
                print(ultimo_retiro_dict)
                
                # Se realiza la insercion en la tabla operation_model poniendo en activo este campo
                # Hacemos un query a la tabla 
                conn = MySQLdb.connect(**db_config)   
                cursor = conn.cursor()
                
                # Obtener la fecha y hora actual en Lima, Perú (GMT-5)
                fecha_actual_lima = datetime.utcnow() - timedelta(hours=5)
                
                # Crear la consulta SQL para la inserción
                query_insert = """
                    INSERT INTO operation_model (
                        descripcion,
                        cuentaDestino,
                        constOperacion,
                        tipoOperacion,
                        montOperacion,
                        moneda,
                        user_model_id,
                        activo,
                        fechaModel
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    );
                """
                
                        # Valores para la inserción
                values = (
                    "RetiroRap",
                    ultimo_retiro_dict['cuentaDestino'],
                    ultimo_retiro_dict['constOperacion'],
                    ultimo_retiro_dict['tipoOperacion'],
                    ultimo_retiro_dict['montOperacion'],
                    ultimo_retiro_dict['moneda'],
                    ultimo_retiro_dict['user_model_id'],
                    True,  # activo
                    fecha_actual_lima
                )
                
                # Ejecutar la consulta
                cursor.execute(query_insert, values)
                conn.commit()

                print("Información insertada en operation_model")

            else:
                # En caso de no haber registros de retiros, puedes manejarlo según tus necesidades
                print("No hay registros de retiros")
                return "No se actualiza por ahora"
        
        conn.close()
        
    except Exception as e:
        print(e)    
    
    return "Retiro rapido calculado"


def retiro_mas_empleado(user_model_id: int):
    try:
        # Crear conexión a la base de datos
        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()
        
        # Consulta SQL
        query = """
            SELECT
                montOperacion,
                cuentaDestino,
                moneda,
                constOperacion,
                COUNT(*) as cantidad
            FROM
                operacion
            WHERE
                user_model_id = %s
                AND tipoOperacion = "Retiro"
            GROUP BY
                montOperacion,
                cuentaDestino,
                moneda,
                constOperacion
            ORDER BY
                cantidad DESC
            LIMIT 1;
        """
        
        cursor.execute(query, (user_model_id,))
        result = cursor.fetchone()
        
        if result:
            # Convertir el resultado a un diccionario para devolverlo como JSON
            column_names = ["montOperacion", "cuentaDestino", "moneda", "constOperacion", "cantidad"]
            result_dict = dict(zip(column_names, result))
            return result_dict
        else:
            return -1 
            
    except Exception as e:
        return -1



def ultimos_3_retiros(user_model_id: int):
    try:
        # Create a connection to the database
        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()
        
        
        # Query para obtener las transacciones de retiro más recientes y repetidas
        query = """
            SELECT
                montOperacion,
                cuentaDestino,
                moneda,
                constOperacion,
                COUNT(*) as totalRepeticiones
            FROM (
                SELECT
                    montOperacion,
                    cuentaDestino,
                    moneda,
                    constOperacion
                FROM
                    operacion
                WHERE
                    user_model_id = %s
                    AND tipoOperacion = "Retiro"
                ORDER BY
                    fechaOperacion DESC
                LIMIT 3
            ) AS TransaccionesRecientes
            GROUP BY
                montOperacion,
                cuentaDestino,
                moneda,
                constOperacion
            HAVING
                totalRepeticiones = 3;
        """
        
        # Ejecutar la consulta
        cursor.execute(query, (user_model_id,))
        result = cursor.fetchone()
        
        
        if result:
            # Convertir el resultado a una lista de diccionarios para devolverla como JSON
            column_names = [desc[0] for desc in cursor.description]
            result_dict = dict(zip(column_names, result))
            
            cursor.close()
            conn.close()
            return result_dict
        else:
            cursor.close()
            conn.close()
            return -1
        
        
    except Exception as e:
        return -1


# Se berifica si los objetos son diferentes
def objetos_diferentes(objeto1, objeto2):
    # Obtener las claves comunes de ambos objetos
    claves_comunes = set(objeto1.keys()) & set(objeto2.keys())

    # Verificar si los valores en las claves comunes son iguales
    for clave in claves_comunes:
        if objeto1[clave] != objeto2[clave]:
            return True  # Hay al menos una diferencia en los valores

    # No se encontraron diferencias en los valores
    return False


# Funcion que realiza un insert del operation model cuando se actualiza
def insertar_en_operation_model_y_desactivar(objeto, descripcion_a_desactivar, user_model_id, tipoOperacion):
    try:
        # Create a connection to the database
        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()

        # Desactivar registros con la descripción y user_model_id dados
        query_desactivar = """
            UPDATE operation_model
            SET activo = 0
            WHERE descripcion = %s
              AND user_model_id = %s
              AND activo = 1;
        """
        
        cursor.execute(query_desactivar, (descripcion_a_desactivar, user_model_id))
        conn.commit()

        # Obtener la fecha y hora actual en Lima, Perú (GMT-5)
        fecha_actual_lima = datetime.utcnow() - timedelta(hours=5)
        
        # Crear la consulta SQL para la inserción
        query_insert = """
            INSERT INTO operation_model (
                descripcion,
                cuentaDestino,
                constOperacion,
                tipoOperacion,
                montOperacion,
                moneda,
                user_model_id,
                activo,
                fechaModel
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            );
        """
        
        # Valores para la inserción
        values = (
            descripcion_a_desactivar,
            objeto.get('cuentaDestino', ''),
            objeto.get('constOperacion', ''),
            tipoOperacion,
            objeto.get('montOperacion', 0),
            objeto.get('moneda', ''),  # moneda (cambiar según necesidades)
            user_model_id,
            1,  # activo
            fecha_actual_lima
        )
        
        
        # Ejecutar la consulta por lo que insertamos en efecto
        cursor.execute(query_insert, values)
        conn.commit()
        
        conn.close()
        
        return "Update completado"
        
    except Exception as e:
        print(e)
        return -1