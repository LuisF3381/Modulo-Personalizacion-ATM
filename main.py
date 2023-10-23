from fastapi import FastAPI, HTTPException
from routes.perfil_route import perfil_r
from routes.userModel_route import userModel_r
from routes.obtieneRutas_route import obtieneRuta_r
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Incluimos los routers
app.include_router(perfil_r)
app.include_router(userModel_r)
app.include_router(obtieneRuta_r)

# Configuración de CORS para permitir solicitudes desde http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/hola")
def mensaje():
    return "Hola desde fast API"



    
