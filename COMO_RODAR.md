# Como rodar o Garimpo em outra máquina (Windows, sem conda)

Passo a passo testado no Windows 11 com Python 3.11 e pip. Com conda, siga o `README.md`.
Depois da instalação, nada precisa de internet.

## O que você precisa

| Item | Onde conseguir | Observação |
|---|---|---|
| Git | https://git-scm.com | |
| Python 3.11 ou 3.12 | https://www.python.org/downloads/ | Marque "Add python.exe to PATH" |
| Ollama | https://ollama.com/download ou `winget install Ollama.Ollama` | Sem ele a busca é só por texto |
| Pasta `data/` do Drive do grupo | Pedir ao grupo | **Não está no Git** (dados comerciais sigilosos) |

## 1. Baixar o código

```bash
git clone https://github.com/VicktzZ/garimpo.git
cd garimpo
```

## 2. Ambiente Python

```bash
python -m venv .venv
```

Ative o ambiente (PowerShell): `.venv\Scripts\Activate.ps1`. No cmd: `.venv\Scripts\activate.bat`.
Se o PowerShell recusar o script, rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

```bash
pip install -e ".[dev]"
pytest
```

O `pip install -e ".[dev]"` instala o pacote `autopecas` (a pasta `src/`), as dependências e o pytest.
O esperado é todos os testes passarem.

## 3. Dados

Copie a pasta `data/` do Drive por cima da pasta `data/` do repositório. O mínimo para abrir o app é
`data/catalogo.db`, que já traz os vetores do bge-m3 calculados. Se vierem `catalogo.db-wal` e
`catalogo.db-shm`, copie os três juntos (feche o app e o Ollama antes).

Sem o Drive, dá para gerar tudo a partir da planilha (colocada em `data/raw/BD_Proj_Integrador_5CD.xlsx`):

```bash
python scripts/01_preparar_dados.py
python scripts/06_importar_catalogo.py
```

Nesse caso a primeira busca híbrida calcula os vetores de todo o catálogo (alguns minutos, uma única vez).

## 4. Ollama

```bash
ollama pull bge-m3          # obrigatório para a busca híbrida (~1,2 GB, uma vez)
ollama pull llama3.2:3b     # opcional: só para o "resumo por IA local"
```

No Windows o Ollama sobe sozinho (ícone na bandeja). Confira com `ollama list`.

## 5. Abrir o app

```bash
python -m streamlit run app/Home.py
```

Abra http://localhost:8501. O menu à esquerda tem **Busca**, **Atualizar catálogo** e **Adaptações**.
Para parar, `Ctrl+C` no terminal.

## Problemas comuns

| Sintoma | Solução |
|---|---|
| `ModuleNotFoundError` (autopecas, pandas, streamlit…) | Ambiente não ativado ou faltou o `pip install -e ".[dev]"` |
| Aviso "catálogo ainda está vazio" | Faltou a etapa 3 |
| Indicador "🔴 offline — usando só lexical" | Ollama parado ou sem o `bge-m3`. O app volta para a híbrida sozinho quando o Ollama voltar |
| Porta 8501 ocupada | `python -m streamlit run app/Home.py --server.port 8502` |
