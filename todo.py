from fastapi import FastAPI, Body

app = FastAPI()

#banco de dado falso por enquanto (lista na memória)
tarefas = []
contador_id = 1

@app.get("/tarefas")
def listar_tarefas():
	return tarefas

@app.post("/tarefas")
def criar_tarefa(tarefa: dict):
	global contador_id
	nova_tarefa = {
	"id": contador_id,
	"titulo": tarefa["titulo"],
	"concluida": False
	}
	tarefas.append(nova_tarefa)
	contador_id += 1 
	return nova_tarefa

@app.put("/tarefas/{id}")
def atualizar_tarefa(id: int, dados: dict = Body(...)):
    for tarefa in tarefas:
        if tarefa["id"] == id:
            tarefa["titulo"] = dados.get("titulo", tarefa["titulo"])
            tarefa["concluida"] = dados.get("concluida", tarefa["concluida"])
            return tarefa
    return {"erro": "Tarefa não encontrada"}

@app.delete("/tarefas/{id}")
def deletar_tarefa(id: int):
    for i, tarefa in enumerate(tarefas):
        if tarefa["id"] == id:
            tarefas.pop(i)
            return {"mensagem": "Tarefa deletada"}
    return {"erro": "Tarefa não encontrada"}
