(function () {
  if (window.RAG_API_URL) {
    return;
  }
  // TODO: Replace with your deployed FastAPI URL, e.g. https://docs-rag.onrender.com
  window.RAG_API_URL = "https://YOUR-BACKEND-URL";
})();
