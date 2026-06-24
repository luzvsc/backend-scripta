from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import aluno_routes
from app.routes import professor_routes
from app.routes import empresa_routes
from app.routes import coordenador_routes
from app.routes import projeto_routes
from app.routes import portfolio_routes
from app.routes import contato_empresa_routes
from app.routes import projeto_integrante_routes
from app.routes import certificado_routes
from app.routes import avaliacao_routes
from app.routes import arquivo_projeto_routes
from app.routes import versao_projeto_routes
from app.routes import link_projeto_routes
from app.routes import relatorios_routes
from app.routes import auth_routes
from app.routes import ranking_routes


app = FastAPI()


origins = [
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS"
        ],
    allow_headers=["Authorization", "Content-Type"]
)


app.include_router(aluno_routes.router)
app.include_router(professor_routes.router)
app.include_router(empresa_routes.router)
app.include_router(coordenador_routes.router)
app.include_router(projeto_routes.router)
app.include_router(portfolio_routes.router)
app.include_router(contato_empresa_routes.router)
app.include_router(projeto_integrante_routes.router)
app.include_router(certificado_routes.router)
app.include_router(avaliacao_routes.router)
app.include_router(arquivo_projeto_routes.router)
app.include_router(versao_projeto_routes.router)
app.include_router(link_projeto_routes.router)
app.include_router(relatorios_routes.router)
app.include_router(auth_routes.router)
app.include_router( ranking_routes.router )

@app.get("/")
def home():
    return {"message": "Scripta API funcionando"}