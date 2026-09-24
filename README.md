# Garimpo

Busca híbrida offline (texto + embeddings locais + filtros) pro catálogo de
autopeças de carros antigos. Spec: `Garimpo_Relato_Tecnologico.docx`.

## Setup

```bash
conda env create -f environment.yml
conda activate garimpo
# ou: pip install -r requirements.txt
```

## Uso

```bash
python scripts/preparar_dados.py caminho/para/BD_Proj_Integrador_5CD.xlsx
python scripts/avaliar.py
pytest
```

## Estrutura

- `garimpo/dados.py` — carga, normalização de texto, validação GTIN (GS1).
- `garimpo/banco.py` — SQLite + índice FTS5.
- `garimpo/recuperacao/lexical.py` — baseline TF-IDF de n-gramas de caracteres.
- `garimpo/recuperacao/embeddings.py` — cliente Ollama com cache (embeddings locais).
- `garimpo/avaliacao.py` — gabarito por GTIN, Hit@k / Recall@k / MRR.
- `scripts/` — CLIs (preparar dados, avaliar).
- `tests/` — pytest, fixtures sintéticas (não usa a planilha real).

## Não feito ainda (P2, ver relato §4.5)

Busca semântica com modelo real (código pronto, precisa Ollama rodando),
fusão híbrida de scores, Modo Adaptações, explicação com LLM local,
interface Streamlit.
