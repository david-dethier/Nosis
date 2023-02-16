import pandas as pd

from fastapi import FastAPI, status, HTTPException
from math import floor

app = FastAPI(
    title="Nosis API - Scoring",
    description="Endpoint de consulta sobre el Valor de Score de un cliente determinado.",
    version="1.0.0")

df_clientes = pd.read_excel("CSV.xltx")


def categoriza_score_50(score: int) -> int:
    """Categoriza el valor de score segun este por debajo/igual o por encima del 50.

    Args:
        score (int): Valor de Score entero.

    Returns:
        int: Valor de Score categorizado.
    """
    es_mayor_50 = score % 100 > 50
    score_centena = floor(score/100) * 100
    score_50 = score_centena + 50 if es_mayor_50 else score_centena
    return score_50


@app.get("/api/v1/scores/clients/{id}")
async def scores(id: int):
    """Devuelve el score de un cliente y categoriza su valor de 50 en 50.

    Args:
        id (int): Id del cliente a consultar.

    Raises:
        HTTPException: Si no existe el recurso, devuelve HTTP_404_NOT_FOUND.

    Returns:
        json: Retorna "NroCliente", "Score", "Score_50"
    """
    df = df_clientes.query(f"NroCliente == {id}")

    if df.empty:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"Cliente {id} No Encontrado.")

    score = int(df["Score"].values[0])
    score_50 = categoriza_score_50(score)

    contexto = [{
        "NroCliente": id,
        "Score": score,
        "Score_50": score_50
    }]

    return {"Resultado": contexto}


@app.get("/")
async def home():
    return {"Link del primer recurso": "/api/v1/scores/clients/1"}
