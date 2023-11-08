from fastapi import APIRouter, HTTPException
import MySQLdb
from config.db import db_config
from datetime import datetime, timedelta


operation_model_r = APIRouter()

@operation_model_r.get("/operation_model/{idOperacionModel}")
def get_operacion_model_by_id(idOperacionModel: int):
    try:
        # Crear una conexión a la base de datos
        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()
        
        # Consultar la operación por su idOperacion
        query = """
            SELECT idOperationModel, descripcion, cuentaDestino, constOperacion, tipoOperacion, montOperacion, moneda, user_model_id, fechaModel FROM operation_model WHERE idOperationModel = %s;
        """
        
        cursor.execute(query, (idOperacionModel,))

        # Obtener el resultado de la consulta
        operacion = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
                # Verificar si la operación existe
        if operacion:
            # Convertir la operación a un diccionario para el formato de respuesta
            operacion_dict = {
                "idOperationModel": operacion[0],
                "descripcion": operacion[1],
                "cuentaDestino": operacion[2],
                "constOperacion": operacion[3],
                "tipoOperacion": operacion[4],
                "montOperacion": operacion[5],
                "moneda": operacion[6],
                "user_model_id": operacion[7],
                "fechaModel": operacion[8].isoformat(),  # Puedes ajustar el formato de la fecha si es necesario
            }

            return operacion_dict
        else:
            # Si no se encuentra la operación, devolver un error 404
            raise HTTPException(status_code=404, detail="Operación no encontrada")
        
            
    except Exception as e:
        # Devolver un error 500 en caso de cualquier problema
        raise HTTPException(status_code=500, detail="Error en el servidor")
