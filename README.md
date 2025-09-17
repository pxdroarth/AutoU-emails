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
```bash
🏗️ Arquitetura
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