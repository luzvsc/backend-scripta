from fastapi import FastAPI
from app.routes import aluno_routes
from app.routes import professor_routes
from app.routes import empresa_routes
from app.routes import coordenador_routes
from app.routes import projeto_routes
from app.routes import portfolio_routes
from app.routes import contato_empresa_routes
from app.routes import projeto_integrante_routes
from app.routes import certificado_routes
from app.routes import logs_sistema_routes
from app.routes import avaliacao_routes

app = FastAPI()

app.include_router(aluno_routes.router)
app.include_router(professor_routes.router)
app.include_router(empresa_routes.router)
app.include_router(coordenador_routes.router)
app.include_router(projeto_routes.router)
app.include_router(portfolio_routes.router)
app.include_router(contato_empresa_routes.router)
app.include_router(projeto_integrante_routes.router)
app.include_router(certificado_routes.router)
app.include_router(logs_sistema_routes.router)
app.include_router(avaliacao_routes.router)

@app.get("/")
def home():
    return {"message": "Scripta API funcionando"}