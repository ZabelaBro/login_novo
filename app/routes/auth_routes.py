from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.controllers.auth_controller import AuthController

router = APIRouter(prefix='/api/auth', tags=['auth'])
controller = AuthController()


class LoginSchema(BaseModel):
    nome: str
    senha: str


@router.post('/login')
def login(dados: LoginSchema):
    usuario = controller.login(dados.nome, dados.senha)
    if usuario is None:
        raise HTTPException(status_code=401, detail='nome ou senha inválidos')
    return usuario

