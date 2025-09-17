import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

# ---------------------------------------------------------------------
# Este módulo cuida do pré-processamento de texto (NLP).
# Objetivo: deixar o texto "limpo e reduzido" antes de ir para o modelo.
# Inclui:
#   - Remoção de links, caracteres estranhos e stopwords.
#   - Redução de palavras para o radical (stemming).
# ---------------------------------------------------------------------

# Garante que os pacotes do NLTK necessários estão disponíveis.
for pkg in ("stopwords", "rslp"):
    try:
        nltk.data.find(f"corpora/{pkg}")
    except:
        nltk.download(pkg)

# Stopwords em português (palavras irrelevantes para análise, ex: "de", "para", "com").
STOPWORDS = set(stopwords.words("portuguese"))

# Stemmer específico para português (RSLP = algoritmo adaptado ao idioma).
STEM = RSLPStemmer()


def limpar_texto(texto: str) -> str:
    """
    Normaliza e reduz o texto a um formato útil para o classificador.

    Passos:
      1. Converte para minúsculas.
      2. Remove links (http/https/www).
      3. Mantém apenas letras, números e acentos comuns do português.
      4. Remove excesso de espaços.
      5. Quebra em tokens (palavras).
      6. Remove stopwords (ex.: "o", "a", "de").
      7. Reduz palavras ao radical via Stemmer (ex.: "atualizar" → "atualiz").
      8. Rejunta tudo em uma string única.

    Exemplo:
      Entrada: "Poderiam atualizar o status do protocolo 2319? Ainda ocorre erro!"
      Saída:   "pod atual status protocol 2319 aind ocorr err"
    """
    # Garantia contra None
    texto = (texto or "").lower()

    # Remove links
    texto = re.sub(r"http\S+|www\S+", " ", texto)

    # Mantém apenas letras (com acento), números e espaços
    texto = re.sub(r"[^a-záéíóúâêîôûàèìòùãõç0-9\s]", " ", texto)

    # Normaliza espaços (múltiplos → um só)
    texto = re.sub(r"\s+", " ", texto).strip()

    # Remove stopwords e aplica stemming
    tokens = [STEM.stem(t) for t in texto.split() if t not in STOPWORDS]

    return " ".join(tokens)
