from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pathlib import Path
import os

# carregar .env de forma robusta (pega backend/.env mesmo se rodar de outro cwd)
from dotenv import load_dotenv, find_dotenv
ENV_PATH = find_dotenv(usecwd=True) or str((Path(__file__).parent / ".env").resolve())
load_dotenv(ENV_PATH, override=False)

from .models.schemas import RespostaClassificacao
from .services.classifier import classificar_e_sugerir
from .services.pdf_reader import extract_text_from_pdf  # leve, PyPDF2

# Leitor de EML é opcional
try:    
    from .services.eml_reader import extract_text_from_eml
    HAS_EML = True
except Exception:
    HAS_EML = False

# ====== FASTAPI APP ======
app = FastAPI(title="AutoU — Classificador de Emails (Local-Only)")

# CORS para permitir o frontend local acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # local-first
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== HELPERS ======
MAX_BYTES = 5 * 1024 * 1024  # 5 MB

def _infer_ext(filename: Optional[str]) -> str:
    if not filename:
        return ""
    lower = filename.lower()
    for ext in (".txt", ".pdf", ".eml"):
        if lower.endswith(ext):
            return ext
    return os.path.splitext(lower)[1].lower()

# ====== ENDPOINTS ======
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/config")
def config():
    """Diagnóstico simples (HF removida neste build)."""
    return {
        "build": "local+heuristica",
        "timeout": os.getenv("HF_TIMEOUT"),
        "cwd": os.getcwd(),
        "has_env_file": os.path.exists(".env"),
        "env_path_loaded": ENV_PATH,
    }

@app.post("/classify", response_model=RespostaClassificacao)
async def classify(
    arquivo: Optional[UploadFile] = File(None),
    texto: Optional[str] = Form(None),
):
    # 1) Extrair conteúdo (prioriza arquivo, se enviado)
    conteudo = (texto or "").strip()

    if arquivo is not None:
        data = await arquivo.read()
        if not data:
            raise HTTPException(status_code=400, detail="Arquivo vazio.")
        if len(data) > MAX_BYTES:
            raise HTTPException(status_code=413, detail="Arquivo muito grande (máx. 5MB).")

        ext = _infer_ext(arquivo.filename)

        if ext in (".txt", ""):
            conteudo = data.decode("utf-8", errors="ignore")

        elif ext == ".pdf":
            try:
                conteudo = extract_text_from_pdf(data)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Falha ao ler PDF: {e}")

        elif ext == ".eml":
            if not HAS_EML:
                raise HTTPException(status_code=400, detail="Leitor de EML não disponível.")
            try:
                conteudo = extract_text_from_eml(data)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Falha ao ler EML: {e}")

        else:
            raise HTTPException(status_code=400, detail="Tipo de arquivo não suportado. Use .txt, .pdf ou .eml.")

    if not conteudo:
        return RespostaClassificacao(
            categoria="Improdutivo",
            confianca=0.5,
            resposta_sugerida="Mensagem vazia ou ilegível. Por favor, reenviar com mais detalhes.",
            origem="heuristica",
        )

    # 2) Classificar e sugerir resposta (Modelo Local → Heurística)
    categoria, confianca, resposta, origem = classificar_e_sugerir(conteudo)

    return RespostaClassificacao(
        categoria=categoria,
        confianca=float(confianca),
        resposta_sugerida=resposta,
        origem=origem,
    )
