from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from models import Tarefa, Usuario
from database import criar_tabelas, get_session
from auth import hash_senha, verificar_senha, criar_token, verificar_token

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.on_event("startup")
def on_startup():
    criar_tabelas()

# --- Autenticação ---

@app.post("/cadastro")
def cadastrar(email: str, senha: str, session: Session = Depends(get_session)):
    usuario = Usuario(email=email, senha_hash=hash_senha(senha))
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return {"mensagem": "Usuário criado com sucesso"}

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    usuario = session.exec(select(Usuario).where(Usuario.email == form.username)).first()
    if not usuario or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    token = criar_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}

def get_usuario_atual(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    usuario = session.exec(select(Usuario).where(Usuario.email == payload["sub"])).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario

# --- Tarefas (protegidas) ---

@app.get("/tarefas")
def listar_tarefas(session: Session = Depends(get_session), usuario: Usuario = Depends(get_usuario_atual)):
    tarefas = session.exec(select(Tarefa)).all()
    return tarefas

@app.post("/tarefas")
def criar_tarefa(tarefa: Tarefa, session: Session = Depends(get_session), usuario: Usuario = Depends(get_usuario_atual)):
    session.add(tarefa)
    session.commit()
    session.refresh(tarefa)
    return tarefa

@app.delete("/tarefas/{id}")
def deletar_tarefa(id: int, session: Session = Depends(get_session), usuario: Usuario = Depends(get_usuario_atual)):
    tarefa = session.get(Tarefa, id)
    if not tarefa:
        return {"erro": "Tarefa não encontrada"}
    session.delete(tarefa)
    session.commit()
    return {"mensagem": "Tarefa deletada"}
