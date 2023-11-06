from fastapi import APIRouter, HTTPException
import MySQLdb
from config.db import db_config

obtieneRuta_r = APIRouter()

# Ruta para obtener ruta que sigue despues de la pantalla login
@obtieneRuta_r.get("/obtener-ruta/login/{user_model_id}")
def get_obtener_ruta_post_login(user_model_id: int):
    try:
        # Create a connection to the database
        conn = MySQLdb.connect(**db_config)   
        cursor = conn.cursor()
    
        # Consultar el perfil_informado por idUserModel
        query = """
            SELECT idUserModel, idUsuario, perfil_informado FROM user_model WHERE idUserModel = %s
        """
        cursor.execute(query, (user_model_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result is None:
            raise HTTPException(status_code=404, detail="User Model not found")
        
        # Crear un objeto PerfilInformadoResponse para la respuesta
        response_data = {
            "idUserModel": result[0],
            "idUsuario": result[1],
            "perfil_informado": bool(result[2])
        }
        
        idUserModel_aux = response_data["idUserModel"]
        idUsuario_aux = response_data["idUsuario"]
        
        if response_data["perfil_informado"] == False:
            # Ahora obtenemos la ruta (en caso no este informado le mandamos)
            return f"/bienvenido/{idUsuario_aux}/{idUserModel_aux}"
        else:
            # Ahora obtenemos la ruta (en caso si este informado se va al menu)
            return f"/principal/{idUsuario_aux}/{idUserModel_aux}"    
        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error en el servidor")
    
    
