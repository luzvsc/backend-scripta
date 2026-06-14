from fastapi import FastAPI
from app.routes import aluno_routes
from app.routes import professor_routes
from app.routes import empresa_routes
from app.routes import coordenador_routes

app = FastAPI()

app.include_router(aluno_routes.router)
app.include_router(professor_routes.router)
app.include_router(empresa_routes.router)
app.include_router(coordenador_routes.router)

@app.get("/")
def home():
    return {"message": "Scripta API funcionando"}