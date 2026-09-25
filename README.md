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

### Interface

```bash
ollama pull bge-m3                      # uma vez; depois roda sem internet
python scripts/comparar_embeddings.py --modelos bge-m3   # gera o cache de vetores (~6 min em CPU)
streamlit run app.py
```

Sem o Ollama rodando, a interface cai sozinha pra busca só lexical.

## Estrutura

- `garimpo/dados.py` — carga, normalização de texto, validação GTIN (GS1).
- `garimpo/banco.py` — SQLite + índice FTS5.
- `garimpo/recuperacao/lexical.py` — baseline TF-IDF de n-gramas de caracteres.
- `garimpo/recuperacao/embeddings.py` — cliente Ollama com cache (embeddings locais).
- `garimpo/avaliacao.py` — gabarito por GTIN, Hit@k / Recall@k / MRR.
- `scripts/` — CLIs (preparar dados, avaliar).
- `tests/` — pytest, fixtures sintéticas (não usa a planilha real).

## Não feito ainda (P2, ver relato §4.5)

Modo Adaptações, explicação com LLM local.
