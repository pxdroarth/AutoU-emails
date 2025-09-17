// Lê a variável de ambiente injetada pelo Render (window.API_BASE).
// Fallback: produção usa backend público; local usa localhost.
(function () {
  const PROD_DEFAULT = "https://autou-backend-ggdb.onrender.com";
  const isRender = location.hostname.endsWith("onrender.com");

  // Render injeta window.API_BASE a partir de {{ API_BASE }} no index.html
  const injected = (typeof window.API_BASE === "string" && window.API_BASE.trim())
    ? window.API_BASE.trim()
    : null;

  window.APP_CONFIG = {
    API_BASE: injected || (isRender ? PROD_DEFAULT : "http://127.0.0.1:8000")
  };
})();
