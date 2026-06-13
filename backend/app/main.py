from fastapi import FastAPI
from app.routes import aluno_routes

app = FastAPI()

app.include_router(aluno_routes.router)
@app.get("/")
def home():
    return {"message": "Scripta API funcionando"}