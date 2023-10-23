from pydantic import BaseModel

# Modelo Pydantic para la creación de un user_model
class UserModelCreate(BaseModel):
    idUsuario: int
    perfil_id: int

class UserModelListado(BaseModel):
    idUserModel: int
    idUsuario: int
    idiomaPreferido: str | None = None 
    tamFuente: int | None = None 
    opRapida1: int | None = None 
    opRapida2: int | None = None 
    opRetRapido: int | None = None 
    ultOp: int | None = None 
    perfil_informado: bool
    perfil_id: int
    
# Para obtener el perfil informado
class PerfilInformadoResponse(BaseModel):
    idUserModel: int
    perfil_informado: bool
    
    
# Modelo Pydantic para la actualización de perfil_informado
class UserModelUpdate(BaseModel):
    perfil_informado: bool
    