from fastapi import APIRouter, HTTPException
from schemas.perfil_schema import Perfil_Lectura, Perfil
import MySQLdb
from config.db import db_config

perfil_r = APIRouter()

# Route to create a profile
@perfil_r.post("/perfiles/")
def create_perfil(perfil: Perfil): 
    # Create a connection to the database
    conn = MySQLdb.connect(**db_config)   
    cursor = conn.cursor()
    query = "INSERT INTO perfil (descripcion, estado, preferenciaTipografia, preferenciaOpRapida1, preferenciaOpRapida2, preferenciaUltimaOp, preferenciaRetiroRap) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (
        perfil.descripcion,
        perfil.estado,
        perfil.preferenciaTipografia,
        perfil.preferenciaOpRapida1,
        perfil.preferenciaOpRapida2,
        perfil.preferenciaUltimaOp,
        perfil.preferenciaRetiroRap
    )
    
    cursor.execute(query, values)
    conn.commit()
    aux = cursor.lastrowid
    cursor.close()
    conn.close()
    return aux

# Route to read a profile by id
@perfil_r.get("/perfiles/{perfil_id}", response_model=Perfil_Lectura)
def read_perfil(perfil_id: int):    
    # Create a connection to the database
    conn = MySQLdb.connect(**db_config)       
    cursor = conn.cursor()
    query = "SELECT idPerfilUsuario, descripcion, estado, preferenciaTipografia, preferenciaOpRapida1, preferenciaOpRapida2, preferenciaUltimaOp, preferenciaRetiroRap FROM perfil WHERE idPerfilUsuario=%s"
    cursor.execute(query, (perfil_id,))
    perfil_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if perfil_data is None:
        raise HTTPException(status_code=404, detail="Perfil not found")
    
    perfil = {
        "idPerfilUsuario": perfil_data[0],
        "descripcion": perfil_data[1],
        "estado": bool(perfil_data[2]),
        "preferenciaTipografia": bool(perfil_data[3]),
        "preferenciaOpRapida1": bool(perfil_data[4]),
        "preferenciaOpRapida2": bool(perfil_data[5]),
        "preferenciaUltimaOp": bool(perfil_data[6]),
        "preferenciaRetiroRap": bool(perfil_data[7])
    }
    
    return perfil



