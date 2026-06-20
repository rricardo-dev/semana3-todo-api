from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def inicio():
	return {"mensagem": "Minha primeira API funcionando!"}

@app.get("/ola/{nome}")
def ola(nome: str):
	return {"mensagem": f"Olá, {nome}!"}
