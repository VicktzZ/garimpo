"""Cliente de embeddings locais via Ollama, com cache em SQLite.

`transporte` é injetável (protocolo com .post(url, json) -> dict) para testar
sem servidor Ollama real, seguindo o "servidor simulado" citado no relato.
"""

from __future__ import annotations

import hashlib
import sqlite3
from typing import Protocol

import numpy as np
import requests

_CACHE_SCHEMA = """
create table if not exists embeddings_cache (
    modelo text not null,
    texto_hash text not null,
    vetor blob not null,
    primary key (modelo, texto_hash)
);
"""


class Transporte(Protocol):
    def post(self, url: str, json: dict) -> dict: ...


class _TransporteRequests:
    def post(self, url: str, json: dict) -> dict:
        resposta = requests.post(url, json=json, timeout=30)
        resposta.raise_for_status()
        return resposta.json()


def _hash_texto(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


class OllamaEmbedder:
    def __init__(
        self,
        modelo: str = "all-minilm",
        base_url: str = "http://localhost:11434",
        conn_cache: sqlite3.Connection | None = None,
        transporte: Transporte | None = None,
    ) -> None:
        self.modelo = modelo
        self._url = f"{base_url.rstrip('/')}/api/embeddings"
        self._conn = conn_cache or sqlite3.connect(":memory:")
        self._conn.executescript(_CACHE_SCHEMA)
        self._transporte = transporte or _TransporteRequests()

    def embed(self, texto: str) -> np.ndarray:
        h = _hash_texto(texto)
        linha = self._conn.execute(
            "select vetor from embeddings_cache where modelo=? and texto_hash=?",
            (self.modelo, h),
        ).fetchone()
        if linha is not None:
            return np.frombuffer(linha[0], dtype=np.float32)

        resposta = self._transporte.post(self._url, {"model": self.modelo, "prompt": texto})
        vetor = np.array(resposta["embedding"], dtype=np.float32)
        self._conn.execute(
            "insert into embeddings_cache(modelo, texto_hash, vetor) values (?, ?, ?)",
            (self.modelo, h, vetor.tobytes()),
        )
        self._conn.commit()
        return vetor

    def embed_lote(self, textos: list[str]) -> np.ndarray:
        return np.stack([self.embed(t) for t in textos])
