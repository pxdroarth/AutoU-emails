const API_BASE =
  (location.hostname === "localhost" || location.hostname === "127.0.0.1")
    ? "http://127.0.0.1:8000"
    : "http://127.0.0.1:8000"; // local-first

const $ = (q) => document.querySelector(q);
const txt = $("#emailText");
const file = $("#emailFile");
const btn = $("#btnProcessar");
const box = $("#result");
const outCat = $("#outCategory");
const outConf = $("#outConfidence");
const outReply = $("#outReply");
const btnCopy = $("#btnCopiar");
const originBadge = $("#originBadge");
const originTitle = $("#originTitle");

// mapeia origem -> [label, classes CSS, texto do título]
function setBadge(origin) {
  const map = {
    hf:        ["HF",         "badge b-hf", "via Hugging Face"],
    modelo:    ["Local",      "badge b-ml", "via Modelo Local"],
    heuristica:["Heurística", "badge b-h",  "via Heurística"],
  };
  const [label, cls, titleText] = map[origin] || ["?", "badge", ""];
  if (originBadge) {
    originBadge.textContent = label;
    originBadge.className = cls;
  }
  if (originTitle) {
    originTitle.textContent = titleText ? ` (${titleText})` : "";
  }
}

btn.addEventListener("click", async () => {
  // monta o FormData enviando OU arquivo OU texto
  const fd = new FormData();
  const f = file.files[0];
  const t = (txt.value || "").trim();

  if (f) {
    fd.append("arquivo", f);
  } else if (t) {
    fd.append("texto", t);
  } else {
    alert("Cole um texto ou selecione um arquivo .txt/.pdf/.eml");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Processando...";
  try {
    const res = await fetch(`${API_BASE}/classify`, { method: "POST", body: fd });
    if (!res.ok) {
      const err = await res.text().catch(() => "");
      throw new Error(err || `HTTP ${res.status}`);
    }
    const data = await res.json();

    outCat.textContent = data.categoria || "-";
    outConf.textContent = data.confianca != null
      ? `${(data.confianca * 100).toFixed(1)}%`
      : "-";
    outReply.value = data.resposta_sugerida || "";

    setBadge(data.origem);
    box.classList.remove("hidden");
  } catch (e) {
    alert("Erro: " + (e.message || e));
  } finally {
    btn.disabled = false;
    btn.textContent = "Processar";
  }
});

btnCopy.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(outReply.value || "");
    btnCopy.textContent = "Copiado!";
    setTimeout(() => (btnCopy.textContent = "Copiar resposta"), 1200);
  } catch {
    alert("Não foi possível copiar.");
  }
});
