## AutoU — Classificador & Auto‑Responder de Emails 🚀

[![Python](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI‑backend-green)](https://fastapi.tiangolo.com/) [![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

---

App web (FastAPI + HTML/JS) que:
- Classifica emails em **Produtivo** ou **Improdutivo**
- Gera **resposta sugerida** conforme a categoria
- Aceita **texto** ou **arquivos** (.txt, .pdf, .eml)

## 🚀 Demo
- **Frontend (estático)**: https://autou-emails.onrender.com
- **Backend (FastAPI)**: https://autou-backend-ggdb.onrender.com
  - Health: `/health`
  - Docs (Swagger): `/docs`

## 🧩 Arquitetura
```tree
AutoU-emails/
├── backend/ # FastAPI
│ ├── app.py # Rotas /health /config /classify
│ ├── models/schemas.py # RespostaClassificacao (Pydantic)
│ └── services/ # classifier.py, pdf_reader.py, eml_reader.py (opcional)
└── frontend/ # HTML/CSS/JS estático
├── index.html
├── styles.css
├── app.js
└── config.js # window.APP_CONFIG.API_BASE
```
shell


## 🏃 Rodando local
```bash
# raiz do repo
uvicorn backend.app:app --reload
# abre http://127.0.0.1:8000/docs
```

# em outra aba, sirva o frontend
cd frontend
python -m http.server 8080
# abre http://127.0.0.1:8080
Em frontend/config.js:

```js
window.APP_CONFIG = { API_BASE: "http://127.0.0.1:8000" };
```
☁️ Deploy no Render
Backend

Root Directory: .

Build Command: pip install -r backend/requirements.txt

Start Command: uvicorn backend.app:app --host 0.0.0.0 --port $PORT

Frontend

Static Site apontando para /frontend (public root)

Em frontend/config.js usar: API_BASE: "https://autou-backend-ggdb.onrender.com"

🔎 API
GET /health → { "status": "ok" }

POST /classify

JSON: { "texto": "..." }

multipart/form-data: texto e/ou arquivo

Retorno:

```json
{
  "categoria": "Produtivo",
  "confianca": 0.96,
  "resposta_sugerida": "Olá! Recebemos...",
  "origem": "modelo"
}
```
🧠 IA
Pipeline com modelo local + heurística (fallback).

Leitura de .pdf via PyPDF2; .eml opcional.

Código desacoplado em services/ para trocar provedores (HF/OpenAI) depois.

✅ Testes rápidos
```bash
curl https://autou-backend-ggdb.onrender.com/health
curl -X POST https://autou-backend-ggdb.onrender.com/classify \
  -H "Content-Type: application/json" -d '{"texto":"Preciso do status do protocolo 123."}'
  ```

👤 Autor
Pedro Arthur 

Pedro Arthur Maia Damasceno (pxdroarth)
Desenvolvedor Full Stack em formação.

```markdown
🤝 Contribuições
Contribuições são bem-vindas!  
Abra uma *issue* para sugestões ou envie um *pull request*. 🚀
```
