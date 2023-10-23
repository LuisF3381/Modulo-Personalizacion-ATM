import MySQLdb

# Database configuration
db_config = {
    'host': 'tesis2-database.czwpv7w8kpxj.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'passwd': 'LUISF3436',
    'db': 'usermodeldatabase',
    'port': 3306,
}

# Create a connection to the database
conn = MySQLdb.connect(**db_config)


from fastapi import FastAPI, HTTPException
from schemas.perfil import Perfil_Lectura, Perfil

app = FastAPI()


@app.get("/hola")
def mensaje():
    return "Hola desde fast API"


# Route to create a profile
@app.post("/perfiles/")
def create_perfil(perfil: Perfil):    
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
    return aux

# Route to read a profile by id
@app.get("/perfiles/{perfil_id}", response_model=Perfil_Lectura)
def read_perfil(perfil_id: int):    
    cursor = conn.cursor()
    query = "SELECT idPerfilUsuario, descripcion, estado, preferenciaTipografia, preferenciaOpRapida1, preferenciaOpRapida2, preferenciaUltimaOp, preferenciaRetiroRap FROM perfil WHERE idPerfilUsuario=%s"
    cursor.execute(query, (perfil_id,))
    perfil_data = cursor.fetchone()
    cursor.close()
    #conn.close()
    
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


    
