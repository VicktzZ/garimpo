import sqlite3

import numpy as np

from garimpo.recuperacao.embeddings import OllamaEmbedder


class TransporteFalso:
    """Simula o servidor Ollama: devolve vetor determinístico por texto."""

    def __init__(self) -> None:
        self.chamadas = 0

    def post(self, url: str, json: dict) -> dict:
        self.chamadas += 1
        texto = json["prompt"]
        semente = sum(ord(c) for c in texto) % 1000
        rng = np.random.default_rng(semente)
        return {"embedding": rng.random(8).tolist()}


def test_embed_chama_transporte_na_primeira_vez():
    transporte = TransporteFalso()
    embedder = OllamaEmbedder(transporte=transporte)
    vetor = embedder.embed("filtro de oleo")
    assert vetor.shape == (8,)
    assert transporte.chamadas == 1


def test_embed_usa_cache_na_segunda_vez():
    transporte = TransporteFalso()
    conn = sqlite3.connect(":memory:")
    embedder = OllamaEmbedder(transporte=transporte, conn_cache=conn)
    v1 = embedder.embed("filtro de oleo")
    v2 = embedder.embed("filtro de oleo")
    assert transporte.chamadas == 1
    assert np.array_equal(v1, v2)


def test_embed_lote_mantem_ordem():
    embedder = OllamaEmbedder(transporte=TransporteFalso())
    vetores = embedder.embed_lote(["a", "b", "c"])
    assert vetores.shape == (3, 8)
