from fastapi import APIRouter, status, Depends
from typing import List
from app.models.aluno import AlunoCreate, AlunoResponse, AlunoLogin, AlunoUpdate
import app.services.aluno_service as aluno_service