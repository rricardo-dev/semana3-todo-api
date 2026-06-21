from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from models import Tarefa
from database import criar_tabelas, get_session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    criar_tabelas()

@app.get("/tarefas")
def listar_tarefas(session: Session = Depends(get_session)):
    tarefas = session.exec(select(Tarefa)).all()
    return tarefas

@app.post("/tarefas")
def criar_tarefa(tarefa: Tarefa, session: Session = Depends(get_session)):
    session.add(tarefa)
    session.commit()
    session.refresh(tarefa)
    return tarefa

@app.put("/tarefas/{id}")
def atualizar_tarefa(id: int, dados: Tarefa, session: Session = Depends(get_session)):
    tarefa = session.get(Tarefa, id)
    if not tarefa:
        return {"erro": "Tarefa não encontrada"}
    tarefa.titulo = dados.titulo
    tarefa.concluida = dados.concluida
    session.commit()
    session.refresh(tarefa)
    return tarefa

@app.delete("/tarefas/{id}")
def deletar_tarefa(id: int, session: Session = Depends(get_session)):
    tarefa = session.get(Tarefa, id)
    if not tarefa:
        return {"erro": "Tarefa não encontrada"}
    session.delete(tarefa)
    session.commit()
    return {"mensagem": "Tarefa deletada"}
