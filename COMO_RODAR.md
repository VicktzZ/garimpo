# Como rodar o Garimpo em outra máquina

Passo a passo para quem acabou de pegar o repositório. Funciona em Windows,
Linux e macOS. Depois da instalação, nada precisa de internet.

## O que você precisa

| Item | Onde conseguir | Observação |
|---|---|---|
| Acesso ao repositório | Pedir ao dono do repo (VicktzZ) | O repo é privado |
| Git | https://git-scm.com | |
| Python 3.11 | https://www.python.org/downloads/ | No Windows, marque "Add python.exe to PATH" |
| Ollama | https://ollama.com/download | Opcional, mas sem ele a busca é só por texto |
| Planilha `BD_Proj_Integrador_5CD.xlsx` | Pedir ao grupo | **Não está no Git** (dados comerciais sigilosos) |

Hardware: qualquer PC com 4 GB de RAM livre. GPU não é necessária; com ela a
primeira carga fica mais rápida.

## 1. Baixar o código

```bash
git clone https://github.com/VicktzZ/garimpo.git
cd garimpo
```

## 2. Criar o ambiente Python e instalar as dependências

Opção A: pip com venv (mais simples)

```bash
python -m venv .venv
```

Ative o ambiente:

- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- Windows (cmd): `.venv\Scripts\activate.bat`
- Linux/macOS: `source .venv/bin/activate`

```bash
pip install -r requirements.txt
```

Se o PowerShell recusar o script de ativação, rode uma vez
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

Opção B: conda

```bash
conda env create -f environment.yml
conda activate garimpo
```

Para conferir que a instalação está certa, rode os testes (não usam a planilha real):

```bash
pytest
```

O esperado é todos passarem.

## 3. Instalar o Ollama e baixar o modelo de embeddings

1. Instale o Ollama:
   - Windows: instalador do site, ou `winget install Ollama.Ollama`
   - Linux: `curl -fsSL https://ollama.com/install.sh | sh`
   - macOS: app do site
2. Baixe o modelo (cerca de 1,2 GB, só uma vez):

   ```bash
   ollama pull bge-m3
   ```

3. Confira se o servidor está no ar:

   ```bash
   ollama list
   ```

   No Windows e no macOS o Ollama sobe sozinho com o sistema (ícone na bandeja).
   No Linux ele roda como serviço; se não estiver rodando, abra outro terminal e
   use `ollama serve`.

Pode pular esta etapa: o app funciona sem o Ollama, só que a busca fica apenas
lexical (por texto) e o indicador na barra lateral fica vermelho.

## 4. Gerar o banco a partir da planilha

Coloque a planilha em qualquer pasta e rode, de dentro da pasta `garimpo`:

```bash
python scripts/preparar_dados.py caminho/para/BD_Proj_Integrador_5CD.xlsx
```

Isso cria `data/garimpo.db` e imprime um relatório de qualidade dos dados
(total de linhas, GTINs válidos, fornecedores). A pasta `data/` fica fora do Git.

## 5. Abrir a interface

Com o Ollama rodando (etapa 3):

```bash
python -m streamlit run app.py
```

Abra http://localhost:8501 no navegador.

**Na primeira vez** o app gera os vetores do catálogo inteiro (cerca de 8,8 mil
peças) e grava em `data/embeddings_cache.db`. Leva por volta de 1 a 2 minutos com
GPU e alguns minutos só com CPU; a tela mostra "Carregando catálogo e vetores".
Nas vezes seguintes ele lê do cache e abre em segundos.

Para parar, `Ctrl+C` no terminal.

## Opcional: reproduzir os experimentos

```bash
python scripts/avaliar.py                                  # baseline lexical por nível
ollama pull all-minilm
python scripts/comparar_embeddings.py                      # lexical x embeddings x híbrida
```

## Problemas comuns

| Sintoma | Causa e solução |
|---|---|
| "Banco não encontrado" na tela | Faltou a etapa 4 |
| Indicador "🔴 offline — usando só lexical" | Ollama parado ou sem o modelo. Suba o Ollama, rode `ollama pull bge-m3` e reinicie o app |
| Ligou o Ollama depois do app e a busca continua só lexical | Os vetores são carregados na abertura. Pare o app (`Ctrl+C`) e rode de novo |
| `python` não é reconhecido (Windows) | Python fora do PATH. Reinstale marcando "Add python.exe to PATH" ou use `py -3.11` |
| `ModuleNotFoundError` | Ambiente não ativado. Repita a ativação da etapa 2 |
| Porta 8501 ocupada | `python -m streamlit run app.py --server.port 8502` |
| Primeira abertura muito demorada | Normal sem GPU; só acontece uma vez |

## Privacidade

- O app só escuta em `localhost` e a telemetria do Streamlit está desligada
  (`.streamlit/config.toml`).
- Nenhum dado sai do computador: o Ollama roda local em `127.0.0.1:11434`.
- Nunca faça commit da planilha nem dos arquivos `.db`; o `.gitignore` já os bloqueia.
