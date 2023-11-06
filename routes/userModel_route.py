from fastapi import APIRouter, HTTPException
from schemas.userModel_schema import UserModelCreate, UserModelListado, UserModelUpdate, PerfilInformadoResponse, UserModelUpdateIdioma
from schemas.perfil_schema import PerfilResponse

import MySQLdb
from config.db import db_config

userModel_r = APIRouter()

# Ruta para crear un user_model
@userModel_r.post("/user-model/create")
def create_user_model(user_model_create: UserModelCreate):
    try:
        # Create a connection to the database
        conn = MySQLdb.connect(**db_config)   
        cursor = conn.cursor()

        # Insertar un nuevo registro en la tabla user_model
        query = """
                INSERT INTO user_model (idUsuario, perfil_informado, perfil_id)
                VALUES (%s, %s, %s)
            """    
            
        values = (
            user_model_create.idUsuario,
            False,  # Valor predeterminado de perfil_informado
            user_model_create.perfil_id
        )
        
        cursor.execute(query, values)
        conn.commit()
        
        # Obtener el ID generado para el nuevo registro
        aux = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return aux
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")
    
    
# Ruta para obtener el idUserModel basándote en el idUsuario
@userModel_r.get("/user-model/by-id-usuario/{id_usuario}", response_model=dict)
def get_user_model_id_by_id_usuario(id_usuario: int):
    try:
        # Create a connection to the database
        conn = MySQLdb.connect(**db_config)   
        cursor = conn.cursor()
        
        # Consultar el registro de user_model por su idUsuario
        query = """
            SELECT idUserModel FROM user_model WHERE idUsuario = %s
        """ 
        
        cursor.execute(query, (id_usuario,))
        user_model_id = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user_model_id is None:
            raise HTTPException(status_code=404, detail="User Model not found")
        
        # Devolver solo el idUserModel como un diccionario
        return {"idUserModel": user_model_id[0]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")
 
    
# Ruta para listar un user_model por su idUserModel
@userModel_r.get("/user-model/{user_model_id}", response_model=UserModelListado)
def get_user_model(user_model_id: int):
    try:
        # Create a connection to the database
        conn = MySQLdb.connect(**db_config)   
        cursor = conn.cursor()
        
        # Consultar el registro de user_model por su idUserModel
        query = """
            SELECT * FROM user_model WHERE idUserModel = %s
        """
        cursor.execute(query, (user_model_id,))
        user_model_data = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if user_model_data is None:
            raise HTTPException(status_code=404, detail="User Model not found")
        
        # Crear un objeto UserModel para la respuesta
        response_user_model = UserModelListado(
            idUserModel = user_model_data[0],
            idUsuario = user_model_data[1],
            idiomaPreferido = user_model_data[2],
            tamFuente = user_model_data[3],
            opRapida1 = user_model_data[4],
            opRapida2 = user_model_data[5],
            opRetRapido = user_model_data[6],
            ultOp = user_model_data[7],
            perfil_informado = bool(user_model_data[8]),
            perfil_id = user_model_data[9]
        )

        return response_user_model    

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error en el servidor")

@userModel_r.get("/user-model/{id_user_model}/perfil", response_model=PerfilResponse)
def get_perfil_by_id_user_model(id_user_model: int):
    try:
        # Create a connection to the database
        conn = MySQLdb.connect(**db_config)   
        cursor = conn.cursor()
        
        # Consultar el perfil del usuario por su idUserModel
        query = """
            SELECT perfil.*
            FROM perfil
            JOIN user_model ON perfil.idPerfilUsuario = user_model.perfil_id
            WHERE user_model.idUserModel = %s
        """
        
        cursor.execute(query, (id_user_model,))
        perfil_data = cursor.fetchone()
        
        cursor.execute(query, (id_user_model,))
        perfil_data = cursor.fetchone()
        
        if perfil_data is None:
            raise HTTPException(status_code=404, detail="Perfil not found")
        
        # Crear un objeto PerfilResponse para la respuesta
        response_perfil = PerfilResponse(
            idPerfilUsuario = perfil_data[0],
            descripcion = perfil_data[1],
            estado = bool(perfil_data[2]),
            preferenciaTipografia = bool(perfil_data[3]),
            preferenciaOpRapida1 = bool(perfil_data[4]),
            preferenciaOpRapida2 = bool(perfil_data[5]),
            preferenciaUltimaOp = bool(perfil_data[6]),
            preferenciaRetiroRap = bool(perfil_data[7])
        )

        return response_perfil
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")


# Ruta para actualizar la columna perfil_informado de un user_model por su idUserModel
@userModel_r.put("/user-model/{user_model_id}/update-perfil-informado")
def update_perfil_informado(user_model_id: int, updated_data: UserModelUpdate):
    try:
        # Create a connection to the database
        conn = MySQLdb.connect(**db_config)   
        cursor = conn.cursor()
        
        # Actualizar la columna perfil_informado del user_model por su idUserModel
        query = """
            UPDATE user_model
            SET perfil_informado = %s
            WHERE idUserModel = %s
        """
        values = (updated_data.perfil_informado, user_model_id)
        
        cursor.execute(query, values)
        conn.commit()
        
        return "Perfil informado actualizado"

        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")
    
    
    
# Ruta para actualizar el idioma seleccionado por el usuario
@userModel_r.put("/user-model/{user_model_id}/update-idioma")
def update_idioma_preferido(user_model_id: int, updated_data: UserModelUpdateIdioma):
    try:
        # Create a connection to the database
        conn = MySQLdb.connect(**db_config)   
        cursor = conn.cursor()
        
        # Actualizar la columna idioma del user_model por su idUserModel
        query = """
            UPDATE user_model
            SET idiomaPreferido = %s
            WHERE idUserModel = %s
        """
        values = (updated_data.idiomaPreferido, user_model_id)

        cursor.execute(query, values)
        conn.commit()
        
        return "Idioma preferido actualizado"
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")
    

# Api que devuelve el idUsuario que pertenece al userModel
@userModel_r.get("/user-model/by-id-user-model/{id_user_model}")
def get_user_id_by_user_model(id_user_model: int):
    try:
        # Crear una conexión a la base de datos
        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()

        # Consultar el registro de user_model por su idUserModel
        query = """
            SELECT idUsuario FROM user_model WHERE idUserModel = %s
        """
        
        cursor.execute(query, (id_user_model,))
        user_id = cursor.fetchone()

        cursor.close()
        conn.close()

        if user_id is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Devolver el idUsuario como un diccionario
        return {"idUsuario": user_id[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servidor")
