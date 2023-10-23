from pydantic import BaseModel

# Creamos el schema para insertar un perfil
class Perfil(BaseModel):
    descripcion: str
    estado: bool
    preferenciaTipografia: bool
    preferenciaOpRapida1: bool
    preferenciaOpRapida2: bool
    preferenciaUltimaOp: bool
    preferenciaRetiroRap: bool

# Creamos el schema para leer un perfil
class Perfil_Lectura(BaseModel):
    idPerfilUsuario: int
    descripcion: str
    estado: bool
    preferenciaTipografia: bool
    preferenciaOpRapida1: bool
    preferenciaOpRapida2: bool
    preferenciaUltimaOp: bool
    preferenciaRetiroRap: bool