// Lê a variável de ambiente injetada pelo Render (window.API_BASE).
// Fallback: produção usa backend público; local usa localhost.
(function () {
  const PROD_DEFAULT = "https://autou-backend-ggdb.onrender.com";
  const isRender = location.hostname.endsWith("onrender.com");

  // Valor “injetado” pelo Render a partir do index.html
  let injected = (typeof window.API_BASE === "string") ? window.API_BASE.trim() : "";

  // Se o Render NÃO substituiu, fica com "{{ API_BASE }}".
  // Detecta chaves/placeholder e invalida.
  const looksLikeTemplate = injected.includes("{{") || injected.includes("}}");
  if (!injected || looksLikeTemplate) {
    injected = "";
  }

  window.APP_CONFIG = {
    API_BASE: injected || (isRender ? PROD_DEFAULT : "http://127.0.0.1:8000")
  };
})();