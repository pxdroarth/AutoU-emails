import csv
from collections import Counter
from pathlib import Path
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ==========================
# 📂 Caminhos principais
# ==========================
DADOS = Path(__file__).parent / "data" / "samples.csv"
MODELO = Path(__file__).parent / "data" / "model.pkl"


def carregar_dados():
    """
    Lê o CSV com colunas:
      - text  : conteúdo do email
      - label : "Produtivo" | "Improdutivo"
    Retorna: X (textos) e y (rótulos).
    """
    textos, labels = [], []
    with open(DADOS, encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            txt = (linha.get("text") or "").strip()
            lb  = (linha.get("label") or "").strip()
            if txt and lb:
                textos.append(txt)
                labels.append(lb)
    if not textos:
        raise RuntimeError(f"Nenhum dado encontrado em {DADOS}.")
    return textos, labels


def montar_pipeline() -> Pipeline:
    """
    Monta o pipeline padrão:
      - TF-IDF (unigramas+bigramas) -> LogisticRegression
    Dica: class_weight='balanced' ajuda em datasets desbalanceados.
    """
    return Pipeline([
        ("vetorizador", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
        ("classificador", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])


def treinar():
    # 1) Carrega dados
    X, y = carregar_dados()
    n = len(y)
    cont = Counter(y)
    print(f"🔎 Total de exemplos: {n} | Distribuição por classe: {dict(cont)}")

    # 2) Decide estratégia de split de forma robusta
    # Regras simples:
    # - Se qualquer classe tiver < 2 amostras → NÃO dá pra estratificar.
    # - Se o dataset for muito pequeno (ex.: < 6), melhor treinar em tudo e pular avaliação.
    pode_estratificar = all(v >= 2 for v in cont.values())
    dataset_pequeno = n < 6

    pipe = montar_pipeline()

    if dataset_pequeno:
        print("⚠️ Dataset muito pequeno (<6). Treinando em TODO o conjunto e pulando avaliação.")
        pipe.fit(X, y)
    else:
        try:
            if pode_estratificar:
                Xtreino, Xteste, ytreino, yteste = train_test_split(
                    X, y, test_size=0.25, random_state=42, stratify=y
                )
            else:
                print("⚠️ Pelo menos uma classe tem só 1 exemplo. Fazendo split SEM estratificar.")
                Xtreino, Xteste, ytreino, yteste = train_test_split(
                    X, y, test_size=0.25, random_state=42
                )

            pipe.fit(Xtreino, ytreino)

            # Avaliação básica
            preds = pipe.predict(Xteste)
            print("\n📊 Relatório de classificação (conjunto de teste):")
            print(classification_report(yteste, preds))
        except ValueError as e:
            # Se ainda assim der erro (ex.: classe sumiu do teste), treinamos em tudo
            print(f"⚠️ Split falhou: {e}\n➡️ Treinando em TODO o conjunto.")
            pipe.fit(X, y)

    # 3) Salva modelo
    MODELO.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODELO)
    print(f"\n✅ Modelo salvo em: {MODELO}")


if __name__ == "__main__":
    treinar()
