// Lê a base da API da config injetada
const API_BASE = window.APP_CONFIG?.API_BASE;
if (!API_BASE) {
  alert("Config inválida: API_BASE não definida.");
}

// Helpers e refs
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
    hf:         ["HF",         "badge b-hf", "via Hugging Face"],
    modelo:     ["Local",      "badge b-ml", "via Modelo Local"],
    heuristica: ["Heurística", "badge b-h",  "via Heurística"],
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
  const f = file.files[0];
  const t = (txt.value || "").trim();

  if (!f && !t) {
    alert("Cole um texto ou selecione um arquivo .txt/.pdf/.eml");
    return;
  }

  btn.disabled = true;
  btn.textContent = "Processando...";
  try {
    let res;

    if (f) {
      // arquivo -> multipart/form-data
      const fd = new FormData();
      fd.append("arquivo", f);
      res = await fetch(`${API_BASE}/classify`, { method: "POST", body: fd });
    } else {
      // só texto -> JSON (backend típico com Pydantic)
      res = await fetch(`${API_BASE}/classify`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({ texto: t })
      });
    }

    if (!res.ok) {
      let msg = `HTTP ${res.status}`;
      try { msg = await res.text(); } catch {}
      throw new Error(msg || `HTTP ${res.status}`);
    }

    // pode vir vazio se backend não retornou JSON — tenta proteger
    const text = await res.text();
    if (!text) throw new Error("Resposta vazia da API.");
    let data;
    try { data = JSON.parse(text); } catch { throw new Error("Resposta não é JSON válido."); }

    outCat.textContent = data.categoria ?? "-";
    outConf.textContent = (typeof data.confianca === "number")
      ? `${(data.confianca * 100).toFixed(1)}%`
      : "-";
    outReply.value = data.resposta_sugerida ?? "";

    setBadge(data.origem);
    box.classList.remove("hidden");
  } catch (e) {
    alert("Erro ao classificar: " + (e?.message || e));
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
