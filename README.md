# AutoU — Classificador & Auto‑Responder de Emails 🚀

[![Python](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI‑backend-green)](https://fastapi.tiangolo.com/) [![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

---
📋 Descrição

AutoU é um sistema backend em Python + FastAPI que automatiza a classificação de emails e sugere respostas corporativas automáticas.

O sistema identifica se um email é:

Produtivo — requer ação (suporte, protocolo, fatura, problema).

Improdutivo — mensagens sem necessidade de ação (felicitações, agradecimentos).

Dependendo da categoria, o sistema sugere uma resposta pronta e formal, agilizando o atendimento.

🧠 Diferenciais

Local-First: roda 100% offline usando modelo treinado TF-IDF + Regressão Logística.

Heurísticas inteligentes: palavras-chave e boosts aumentam precisão em casos ambíguos.

Suporte a múltiplos formatos: texto puro, PDF e arquivos .eml.

Interface simples para colar texto ou enviar arquivos.

Respostas automáticas corporativas adaptadas à categoria.

🏗️ Arquitetura
```bash
AutoU-emails/
├── backend/
│   ├── app.py              # FastAPI principal (rotas /health, /classify)
│   ├── models/
│   │   └── schemas.py      # Schemas Pydantic
│   ├── services/
│   │   ├── classifier.py   # Orquestrador (Modelo Local + Heurística)
│   │   ├── responders.py   # Respostas padrão
│   │   ├── pdf_reader.py   # Leitor PDF (PyPDF2)
│   │   └── eml_reader.py   # Leitor EML (opcional)
│   └── data/
│       └── model.pkl       # Modelo local treinado
├── requirements.txt
└── README.md
```
⚙️ Instalação

Clone o repositório:
```bash
git clone https://github.com/seu-usuario/AutoU-emails.git
cd AutoU-emails/backend
```

Crie ambiente virtual:
```powershell
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/Mac
```

Instale dependências:
```bash
pip install -r requirements.txt
```

Inicie o backend:
```bash
uvicorn app:app --reload
```
📚 Treinamento do modelo local (TF-IDF + Regressão Logística)

O projeto inclui um script para (re)treinar o modelo local a partir de um CSV rotulado.

Formato esperado do CSV

Arquivo: backend/data/train.csv (padrão).

Colunas (header):

texto → conteúdo do email (string)

categoria → rótulo Produtivo ou Improdutivo

Exemplo (train.csv):
```csv
texto,categoria
"Favor verificar o status do protocolo 12345","Produtivo"
"Agradeço o ótimo suporte prestado","Improdutivo"
"Em anexo segue a fatura do mês","Produtivo"
"Feliz Natal para toda a equipe!","Improdutivo"
```
Dica: mantenha a base equilibrada entre as classes para melhorar a qualidade.

Rodando o treinamento

No Windows (PowerShell):

```powershell
cd backend
.venv\Scripts\activate
python train_classifier.py
```

No Linux/Mac:
```bash
cd backend
source .venv/bin/activate
python train_classifier.py
```
Saída esperada

O modelo treinado será salvo em:
backend/data/model.pkl

O backend já lê esse caminho automaticamente (não precisa configurar nada).

Atualizei o modelo, preciso reiniciar algo?

Se o uvicorn estiver rodando, reinicie o backend para ele recarregar o novo model.pkl:

# na pasta backend
```bash
uvicorn app:app --reload
```

▶️ Uso

Acesse http://127.0.0.1:8000 para API.

Endpoint principal:
```json
POST /classify → recebe texto ou arquivo (.txt/.pdf/.eml) e retorna categoria, confiança, resposta sugerida e origem.
```
Interface web: basta abrir o arquivo HTML no navegador (index.html).

Frontend (Interface web)

Abra uma nova aba do terminal e vá até a pasta frontend/.

Sirva os arquivos estáticos com um servidor simples, por exemplo:
```bash
cd ../frontend
python -m http.server 5500
```
Por padrao o uso local sera
```url
http://127.0.0.1:5500/
```
para rodar manualmente

✅ Funcionalidades


Classificação automática Produtivo vs. Improdutivo

Resposta sugerida automaticamente

Upload de arquivo ou entrada manual de texto

Heurística robusta + modelo local híbrido

Fallback seguro sempre retorna algo


🧪 Testes

```python
Exemplo com pytest:

from fastapi.testclient import TestClient
from app import app

def test_health():
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_classify():
    client = TestClient(app)
    payload = {"texto": "Favor verificar protocolo 1234, não recebi resposta"}
    r = client.post("/classify", data=payload)
    data = r.json()
    assert r.status_code == 200
    assert data["categoria"] == "Produtivo"
```

📆 Roadmap

 Ampliar base de palavras-chave e treinar modelo com novos domínios.

 Persistir histórico de classificações em banco de dados.

 Criar frontend dedicado (React ou Vite).

 Dashboard com métricas (qtd. de emails, % produtivos, etc.).

📜 Licença

Projeto sob licença MIT — veja LICENSE
.

👤 Autor

Pedro Arthur Maia Damasceno
Desenvolvedor Full Stack em formação.

```markdown
🤝 Contribuições
Contribuições são bem-vindas!  
Abra uma *issue* para sugestões ou envie um *pull request*. 🚀
```
