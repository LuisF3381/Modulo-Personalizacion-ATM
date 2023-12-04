from fastapi import APIRouter, HTTPException
from schemas.userModel_schema import UserModelCreate, UserModelListado, UserModelUpdate, PerfilInformadoResponse, UserModelUpdateIdioma
from schemas.operacion_schema import OperacionCreate, MetricaCreate

import MySQLdb
from config.db import db_config

operacion_r = APIRouter()

# Funcion que realiza una insercion en la tabla de operacion
from fastapi import HTTPException

# Ruta para insertar una operación
@operacion_r.post("/operacion/insert")
def insert_operacion(operacion_create: OperacionCreate):
    try:
        # Crear una conexión a la base de datos
        conn = MySQLdb.connect(**db_config)   
        cursor = conn.cursor()

        # Insertar un nuevo registro en la tabla de operaciones
        query = """
                INSERT INTO operacion (
                    tipoOperacion, montOperacion, fechaOperacion, 
                    constOperacion, cuentaDestino, moneda, nota, user_model_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """    
            
        values = (
            operacion_create.tipoOperacion,
            operacion_create.montOperacion,
            operacion_create.fechaOperacion,
            operacion_create.constOperacion,
            operacion_create.cuentaDestino,
            operacion_create.moneda,
            operacion_create.nota,
            operacion_create.user_model_id
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        # Obtener el ID generado para el nuevo registro
        new_record_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return {"idOperacion": new_record_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")


@operacion_r.get("/operacion/{idOperacion}")
def get_operacion_by_id(idOperacion: int):
    try:
        # Crear una conexión a la base de datos
        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()

        # Consultar la operación por su idOperacion
        query = """
                SELECT * FROM operacion WHERE idOperacion = %s;
            """
        cursor.execute(query, (idOperacion,))
        
        # Obtener el resultado de la consulta
        operacion = cursor.fetchone()
        
        cursor.close()
        conn.close()

        # Verificar si la operación existe
        if operacion:
            # Convertir la operación a un diccionario para el formato de respuesta
            operacion_dict = {
                "idOperacion": operacion[0],
                "tipoOperacion": operacion[1],
                "montOperacion": operacion[2],
                "fechaOperacion": operacion[3].isoformat(),  # Puedes ajustar el formato de la fecha si es necesario
                "constOperacion": operacion[4],
                "cuentaDestino": operacion[5],
                "moneda": operacion[6],
                "nota": operacion[7],
                "user_model_id": operacion[8],
            }

            return operacion_dict
        else:
            # Si no se encuentra la operación, devolver un error 404
            raise HTTPException(status_code=404, detail="Operación no encontrada")
    
    except Exception as e:
        # Devolver un error 500 en caso de cualquier problema
        raise HTTPException(status_code=500, detail="Error en el servidor")


@operacion_r.put("/operacion/update/{idOperacion}")
def update_const_operacion(idOperacion: int, const_operacion_update: str):
    try:
        # Crear una conexión a la base de datos
        conn = MySQLdb.connect(**db_config)   
        cursor = conn.cursor()

        # Actualizar el campo constOperacion de la operación específica
        query = """
                UPDATE operacion
                SET constOperacion = %s
                WHERE idOperacion = %s
            """    
            
        values = (const_operacion_update, idOperacion)
        
        cursor.execute(query, values)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return {"message": "Campo constOperacion actualizado correctamente"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")


@operacion_r.post("/operacion_tiempo/insert")
def insert_metrica(metrica_create: MetricaCreate):
    try:
        # Crear una conexión a la base de datos
        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()

        # Insertar un nuevo registro en la tabla de métricas
        query = """
                INSERT INTO MetricasXPantalla (
                    descripcion, tiempoUsoPantalla, fechaMetrica, user_model_id
                )
                VALUES (%s, %s, %s, %s)
            """

        values = (
            metrica_create.descripcion,
            metrica_create.tiempoUsoPantalla,
            metrica_create.fechaMetrica,
            metrica_create.user_model_id
        )

        cursor.execute(query, values)
        conn.commit()

        # Obtener el ID generado para el nuevo registro
        new_record_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return {"idMetrica": new_record_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")

