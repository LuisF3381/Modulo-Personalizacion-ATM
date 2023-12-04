from pydantic import BaseModel
from datetime import datetime

# Modelo Pydantic para la creación de un user_model
class OperacionCreate(BaseModel):
    tipoOperacion: str
    montOperacion: int | None = None
    fechaOperacion: datetime
    constOperacion: str | None = None
    cuentaDestino: str
    moneda: str | None = None
    nota:str | None = None 
    user_model_id: int 
    

# Modelo de datos simplificado para la creación de la métrica
class MetricaCreate(BaseModel):
    descripcion: str
    tiempoUsoPantalla: int
    fechaMetrica: datetime
    user_model_id: int