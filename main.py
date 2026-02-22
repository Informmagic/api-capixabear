import os
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from supabase import create_client, Client

app = FastAPI()

# --- 1. CONFIGURAÇÃO DO SUPABASE ---
# Substitua os valores abaixo pelas chaves que você copiou do site do Supabase
SUPABASE_URL = "https://jykrxafzsrikgredfirv.supabase.co"
SUPABASE_KEY = "sb_publishable_zommCAP812fIC7P5ELHfdg_qwbBPfY7"

# Inicializa o cliente que faz a ponte entre o Python e a Nuvem
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. O MODELO DE DADOS ---
# Ele deve ser idêntico às colunas que criamos na tabela 'spots'
class TouristSpot(BaseModel):
    id: int           # O Supabase gera IDs numéricos por padrão
    name: str
    description: str
    imageUrl: str
    crowdStatus: str
    category: str     # Agora a categoria é obrigatória e vem do banco!
    latitude: float
    longitude: float

# --- 3. AS ROTAS DA API ---

# Rota para listar todos os pontos turísticos
@app.get("/spots", response_model=List[TouristSpot])
def get_spots():
    # Tradução: "No banco, selecione todos os dados da tabela spots e execute"
    query = supabase.table("spots").select("*").execute()
    return query.data

# Rota para pegar detalhes de um lugar específico pelo ID
@app.get("/spots/{spot_id}", response_model=TouristSpot)
def get_spot(spot_id: int):
    # Tradução: "Na tabela spots, selecione tudo onde o id seja igual ao spot_id"
    query = supabase.table("spots").select("*").eq("id", spot_id).single().execute()
    return query.data

# Rota para buscar os eventos da Agenda
@app.get("/eventos")
def get_eventos():
    try:
        # Busca todos os registros da tabela 'eventos' no Supabase
        response = supabase.table("eventos").select("*").execute()
        return response.data
    except Exception as e:
        # Se der erro (ex: tabela não existe), avisa sem derrubar o servidor
        return {"error": str(e)}

@app.get("/historias")
def get_historias():
    try:
        response = supabase.table("articles").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}
    
# Rota para buscar os Parceiros (Hotéis, Restaurantes, etc)
@app.get("/parceiros")
def get_parceiros():
    try:
        response = supabase.table("parceiros").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": str(e)}