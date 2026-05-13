from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from .CryptoSolver import CryptoSolver

app = FastAPI()

# Permitir CORS para el frontend en localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SolveRequest(BaseModel):
    matrix: List[List[str]]  #Matriz de letras
    encoded_message: List[int]  #Mensaje codificado como lista de dígitos

class SolveResponse(BaseModel):
    has_solution: bool  
    predictions: Dict[str, int]  # -> esta parte lo que hace es un Mapeo letra a dígito
    history: List[Dict[str, int]]  
    decoded_message: List[str]  


@app.post("/solve", response_model=SolveResponse)
def solve_cryptosolver(data: SolveRequest):
    """
    Endpoint principal
    Recibe una matriz de letras y un mensaje codificado, despues ejecuta el archivo de CryptoSolver y retorna la solución, el historial 
    y el mensaje decodificado.
    """
    solver = CryptoSolver(data.matrix, data.encoded_message)
    return SolveResponse(
        has_solution=solver.has_solution,
        predictions=solver.predictions,
        history=solver.history,
        decoded_message=solver.message_decoded
    )


@app.get("/health")
def health():
    """
    Endpoint de prueba para comprobar que el servidor está corriendo.
    """
    return {"status": "ok"}
