(function () {
  if (window.__docsChatLoaded) {
    return;
  }
  window.__docsChatLoaded = true;

  const apiBase = (window.RAG_API_URL || "http://localhost:8001").replace(/\/$/, "");
  const endpoint = `${apiBase}/chat`;

  const state = {
    open: false,
    busy: false,
  };

  function escapeHtml(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function toMultiline(text) {
    return escapeHtml(text).replace(/\n/g, "<br>");
  }

  function createMessage(role, text, opts = {}) {
    const el = document.createElement("div");
    el.className = `chat-message ${role}` + (opts.pending ? " pending" : "");

    const body = document.createElement("div");
    body.className = "text";
    body.innerHTML = toMultiline(text || "");
    el.appendChild(body);

    if (opts.sources && opts.sources.length) {
      const sources = document.createElement("div");
      sources.className = "sources";
      const heading = document.createElement("strong");
      heading.textContent = "Sources";
      sources.appendChild(heading);

      const list = document.createElement("ul");
      opts.sources.forEach((src) => {
        const item = document.createElement("li");
        item.textContent = src;
        list.appendChild(item);
      });
      sources.appendChild(list);
      el.appendChild(sources);
    }

    return el;
  }

  function updateMessage(el, text, opts = {}) {
    const body = el.querySelector(".text");
    body.innerHTML = toMultiline(text || "");
    el.classList.remove("pending");

    const existingSources = el.querySelector(".sources");
    if (existingSources) {
      existingSources.remove();
    }

    const sources = opts.sources || [];
    if (sources.length) {
      const srcDiv = document.createElement("div");
      srcDiv.className = "sources";
      const heading = document.createElement("strong");
      heading.textContent = "Sources";
      srcDiv.appendChild(heading);

      const list = document.createElement("ul");
      sources.forEach((src) => {
        const item = document.createElement("li");
        item.textContent = src;
        list.appendChild(item);
      });

      srcDiv.appendChild(list);
      el.appendChild(srcDiv);
    }
  }

  function scrollToBottom(container) {
    container.scrollTop = container.scrollHeight;
  }

  function buildUi() {
    const toggle = document.createElement("button");
    toggle.id = "chat-toggle";
    toggle.type = "button";
    toggle.innerHTML = "<span>Chat with docs</span>";

    const panel = document.createElement("aside");
    panel.id = "chat-panel";
    panel.setAttribute("aria-hidden", "true");

    const header = document.createElement("header");
    header.innerHTML = '<span>Ask the docs</span><button type="button" aria-label="Close chat">×</button>';

    const messages = document.createElement("div");
    messages.id = "chat-messages";

    const inputRow = document.createElement("div");
    inputRow.className = "chat-input-row";

    const input = document.createElement("input");
    input.id = "chat-input";
    input.type = "text";
    input.placeholder = "Ask about these docs";
    input.autocomplete = "off";

    const send = document.createElement("button");
    send.id = "chat-send";
    send.type = "button";
    send.textContent = "Send";

    inputRow.appendChild(input);
    inputRow.appendChild(send);

    panel.appendChild(header);
    panel.appendChild(messages);
    panel.appendChild(inputRow);

    document.body.appendChild(toggle);
    document.body.appendChild(panel);

    function openChat() {
      state.open = true;
      panel.classList.add("open");
      panel.setAttribute("aria-hidden", "false");
      input.focus();
    }

    function closeChat() {
      state.open = false;
      panel.classList.remove("open");
      panel.setAttribute("aria-hidden", "true");
    }

    toggle.addEventListener("click", () => {
      if (state.open) {
        closeChat();
      } else {
        openChat();
      }
    });

    header.querySelector("button").addEventListener("click", closeChat);

    async function handleSend() {
      const question = input.value.trim();
      if (!question || state.busy) {
        return;
      }

      state.busy = true;
      send.disabled = true;
      input.value = "";

      const userMsg = createMessage("user", question);
      messages.appendChild(userMsg);
      scrollToBottom(messages);

      const assistantMsg = createMessage("assistant", "Thinking…", { pending: true });
      messages.appendChild(assistantMsg);
      scrollToBottom(messages);

      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query: question }),
        });

        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`);
        }

        const payload = await response.json();
        const answer = payload.answer || "I couldn't find anything relevant.";
        const sources = Array.isArray(payload.sources)
          ? payload.sources.filter(Boolean)
          : [];

        updateMessage(assistantMsg, answer, { sources });
      } catch (error) {
        updateMessage(
          assistantMsg,
          error.message || "Something went wrong. Please try again.",
        );
        assistantMsg.classList.add("chat-error");
      } finally {
        state.busy = false;
        send.disabled = false;
        scrollToBottom(messages);
      }
    }

    send.addEventListener("click", handleSend);
    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        handleSend();
      }
    });

    return { toggle, panel, messages, input, send };
  }

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn, { once: true });
    } else {
      fn();
    }
  }

  ready(buildUi);
})();
