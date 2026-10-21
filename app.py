
import os
import gradio as gr
import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from gradio_client import Client


NOVA_API_URL = "https://792c284910eefa1a32.gradio.live"

app = FastAPI(title="NOVA AI")


# --------------------------------------------------
# FRONTEND: HTML, CSS E JAVASCRIPT PERSONALIZZATI
# --------------------------------------------------

HTML = r"""
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f7f7f8">
<title>NOVA AI</title>

<style>
:root {
  --bg: #f7f7f8;
  --sidebar: #f0f0f2;
  --white: #fff;
  --text: #202123;
  --muted: #85858e;
  --border: #e5e5e9;
  --hover: #e6e6ea;
  --accent: #202123;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: Inter, -apple-system, BlinkMacSystemFont,
               "Segoe UI", sans-serif;
  color: var(--text);
  background: var(--bg);
}

button, textarea { font: inherit; }
button { cursor: pointer; }

.app {
  display: flex;
  min-height: 100dvh;
}

/* SIDEBAR */

.sidebar {
  width: 255px;
  flex-shrink: 0;
  background: var(--sidebar);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 19px 13px;
  transition: width .2s;
}

.brand {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 4px 8px 24px;
}

.logo {
  width: 41px;
  height: 41px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 13px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
}

.logo svg { width: 29px; height: 29px; }

.brand-name {
  font-weight: 750;
  letter-spacing: -.6px;
  font-size: 19px;
}

.brand-caption {
  color: var(--muted);
  font-size: 11px;
  margin-top: 3px;
}

.new-chat {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 13px;
  border: 1px solid #dedee3;
  background: #fff;
  border-radius: 13px;
  text-align: left;
  font-size: 13px;
  font-weight: 550;
  color: var(--text);
  transition: background .15s, transform .15s;
}

.new-chat:hover { background: #f9f9fa; }
.new-chat:active { transform: scale(.98); }

.section-label {
  padding: 26px 9px 10px;
  color: var(--muted);
  font-size: 11px;
  font-weight: 650;
  letter-spacing: .7px;
  text-transform: uppercase;
}

.history {
  display: flex;
  flex-direction: column;
  gap: 3px;
  overflow-y: auto;
}

.history-item {
  width: 100%;
  padding: 10px;
  border: 0;
  border-radius: 9px;
  background: transparent;
  text-align: left;
  color: #51515a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 12px;
}

.history-item:hover,
.history-item.active { background: var(--hover); }

.sidebar-bottom {
  margin-top: auto;
  padding: 14px 8px 0;
  color: #8a8a92;
  font-size: 11px;
}

/* MAIN */

.main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
}

.topbar {
  height: 67px;
  padding: 0 29px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
  background: rgba(247,247,248,.88);
}

.mobile-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  letter-spacing: -.4px;
}

.mobile-brand .logo {
  width: 35px;
  height: 35px;
  border-radius: 11px;
}

.mobile-brand .logo svg {
  width: 25px;
  height: 25px;
}

.status {
  display: flex;
  align-items: center;
  gap: 7px;
  color: #777780;
  font-size: 11px;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #b8b8c0;
}

.content {
  width: 100%;
  max-width: 850px;
  margin: 0 auto;
  padding: 26px 27px 20px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 25px;
  padding-bottom: 25px;
}

.welcome {
  margin: auto 0 10px;
  padding-top: 48px;
  animation: appear .35s ease;
}

.welcome-symbol {
  width: 54px;
  height: 54px;
  display: grid;
  place-items: center;
  border-radius: 18px;
  background: white;
  border: 1px solid var(--border);
  margin-bottom: 25px;
}

.welcome-symbol svg { width: 38px; height: 38px; }

h1 {
  margin: 0;
  font-size: clamp(27px, 4vw, 38px);
  line-height: 1.17;
  letter-spacing: -1.6px;
  font-weight: 650;
}

.subtitle {
  color: var(--muted);
  font-size: 15px;
  margin-top: 13px;
  line-height: 1.6;
}

.suggestions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 33px;
}

.suggestion {
  border: 1px solid var(--border);
  background: #fff;
  border-radius: 16px;
  padding: 17px;
  text-align: left;
  transition: border-color .18s, transform .18s,
              box-shadow .18s;
}

.suggestion:hover {
  border-color: #c9c9d1;
  box-shadow: 0 5px 18px #20212308;
  transform: translateY(-2px);
}

.suggestion-icon {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border-radius: 11px;
  background: #f1efff;
  color: #7161d8;
  font-size: 17px;
  margin-bottom: 15px;
}

.suggestion:nth-child(2) .suggestion-icon {
  background: #eaf2ff;
  color: #4275c5;
}

.suggestion-title {
  font-size: 13px;
  font-weight: 650;
  margin-bottom: 6px;
}

.suggestion-description {
  font-size: 11px;
  line-height: 1.55;
  color: var(--muted);
}

/* MESSAGES */

.message {
  display: flex;
  flex-direction: column;
  gap: 8px;
  animation: appear .2s ease;
}

.message.user { align-items: flex-end; }

.message-bubble {
  max-width: 84%;
  padding: 13px 17px;
  border-radius: 18px;
  font-size: 14px;
  line-height: 1.75;
  overflow-wrap: anywhere;
  white-space: pre-wrap;
}

.user .message-bubble {
  background: #e9e9ef;
  border: 1px solid #e4e4e9;
  border-bottom-right-radius: 5px;
}

.assistant .message-bubble {
  padding-left: 0;
  padding-right: 0;
  max-width: 100%;
}

.message-label {
  font-size: 10px;
  color: #92929a;
  padding: 0 3px;
}

.typing {
  display: flex;
  gap: 5px;
  padding: 14px 0;
}

.typing span {
  width: 6px;
  height: 6px;
  background: #9999a1;
  border-radius: 50%;
  animation: bounce 1s infinite alternate;
}

.typing span:nth-child(2) { animation-delay: .15s; }
.typing span:nth-child(3) { animation-delay: .3s; }

/* COMPOSER */

.composer-area {
  position: sticky;
  bottom: 0;
  padding-top: 10px;
  background: linear-gradient(
    to bottom, rgba(247,247,248,0), var(--bg) 18%
  );
}

.composer {
  display: flex;
  align-items: flex-end;
  gap: 9px;
  background: white;
  border: 1px solid #dedee3;
  border-radius: 22px;
  padding: 10px 10px 10px 17px;
  box-shadow: 0 5px 20px #00000007;
  transition: border-color .18s, box-shadow .18s;
}

.composer:focus-within {
  border-color: #bdbdc6;
  box-shadow: 0 5px 22px #0000000b;
}

#prompt {
  flex: 1;
  min-width: 0;
  resize: none;
  outline: none;
  border: 0;
  background: transparent;
  color: var(--text);
  font-size: 14px;
  line-height: 1.6;
  max-height: 160px;
  padding: 8px 0;
}

#prompt::placeholder { color: #9999a1; }

.send {
  width: 41px;
  height: 41px;
  flex-shrink: 0;
  border: 0;
  border-radius: 13px;
  background: #202123;
  color: white;
  font-size: 23px;
  display: grid;
  place-items: center;
  transition: background .15s, transform .15s;
}

.send:hover { background: #39393f; }
.send:active { transform: scale(.94); }
.send:disabled { opacity: .45; cursor: not-allowed; }

.disclaimer {
  color: #9999a1;
  text-align: center;
  font-size: 10px;
  padding: 12px 0 2px;
}

.mobile-menu { display: none; }

@keyframes appear {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes bounce {
  from { transform: translateY(0); opacity: .5; }
  to { transform: translateY(-4px); opacity: 1; }
}

@media (max-width: 700px) {
  .sidebar {
    position: fixed;
    z-index: 10;
    top: 0;
    bottom: 0;
    left: 0;
    width: 260px;
    transform: translateX(-101%);
    transition: transform .22s ease;
    box-shadow: 10px 0 30px #0000000c;
  }

  .sidebar.open { transform: translateX(0); }

  .mobile-menu {
    display: grid;
    place-items: center;
    width: 36px;
    height: 36px;
    background: white;
    border: 1px solid var(--border);
    border-radius: 11px;
    color: var(--text);
    font-size: 19px;
  }

  .topbar { padding: 0 15px; height: 59px; }
  .content { padding: 17px 15px 14px; }
  .welcome { padding-top: 35px; }
  .suggestions { gap: 9px; margin-top: 25px; }
  .suggestion { padding: 13px; }
  .suggestion-icon { margin-bottom: 10px; }
  .message-bubble { max-width: 94%; }
  .status { font-size: 10px; }
}

@media (max-width: 390px) {
  .suggestions { grid-template-columns: 1fr; }
  .suggestion { display: grid; grid-template-columns: 35px 1fr;
                column-gap: 11px; align-items: center; }
  .suggestion-icon { grid-row: span 2; margin: 0; }
  .suggestion-title { margin: 0 0 3px; }
}
</style>
</head>

<body>
<div class="app">

  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <div class="logo">__LOGO__</div>
      <div>
        <div class="brand-name">NOVA</div>
        <div class="brand-caption">La tua AI personale</div>
      </div>
    </div>

    <button class="new-chat" id="newChat">
      <span style="font-size:19px">＋</span>
      <span>Nuova chat</span>
    </button>

    <div class="section-label">Cronologia</div>
    <div class="history" id="history"></div>

    <div class="sidebar-bottom">NOVA AI · Il tuo spazio creativo</div>
  </aside>

  <main class="main">
    <header class="topbar">
      <div style="display:flex;align-items:center;gap:11px">
        <button class="mobile-menu" id="menuBtn" aria-label="Apri menu">☰</button>
        <div class="mobile-brand">
          <div class="logo">__LOGO__</div>
          <span>NOVA</span>
        </div>
      </div>
      <div class="status">
        <span class="status-dot"></span>
        <span>Assistente AI</span>
      </div>
    </header>

    <section class="content">
      <div class="chat" id="chat">
        <div class="welcome" id="welcome">
          <div class="welcome-symbol">__LOGO__</div>
          <h1>Come posso aiutarti?</h1>
          <div class="subtitle">La tua prossima idea inizia qui.</div>

          <div class="suggestions">
            <button class="suggestion" data-prompt="Aiutami a trovare idee creative per un nuovo progetto.">
              <div class="suggestion-icon">✳</div>
              <div class="suggestion-title">Idee creative</div>
              <div class="suggestion-description">Dai forma alle tue idee e scopri nuove possibilità.</div>
            </button>

            <button class="suggestion" data-prompt="Aiutami a studiare un argomento difficile, spiegandomelo in modo semplice.">
              <div class="suggestion-icon">⌘</div>
              <div class="suggestion-title">Studia con NOVA</div>
              <div class="suggestion-description">Spiegazioni chiare, esempi e aiuto nello studio.</div>
            </button>
          </div>
        </div>
      </div>

      <div class="composer-area">
        <form class="composer" id="composer">
          <textarea id="prompt" rows="1" placeholder="Scrivi un messaggio a NOVA..." aria-label="Messaggio"></textarea>
          <button class="send" id="send" type="submit" aria-label="Invia messaggio">↑</button>
        </form>
        <div class="disclaimer">NOVA può commettere errori. Verifica le informazioni importanti.</div>
      </div>
    </section>
  </main>
</div>

<script>
const chatEl = document.getElementById("chat");
const promptEl = document.getElementById("prompt");
const sendBtn = document.getElementById("send");
const historyEl = document.getElementById("history");
const sidebar = document.getElementById("sidebar");

let conversations = [];
let activeId = null;
let busy = false;

function createConversation() {
  const item = {
    id: crypto.randomUUID(),
    title: "Nuova chat",
    messages: []
  };
  conversations.unshift(item);
  activeId = item.id;
  renderHistory();
  renderChat();
}

function activeConversation() {
  return conversations.find(c => c.id === activeId);
}

function renderHistory() {
  historyEl.innerHTML = "";
  conversations.forEach(c => {
    if (!c.messages.length && conversations.length > 1) return;

    const b = document.createElement("button");
    b.className = "history-item" + (c.id === activeId ? " active" : "");
    b.textContent = c.title;
    b.title = c.title;
    b.onclick = () => {
      activeId = c.id;
      renderHistory();
      renderChat();
      sidebar.classList.remove("open");
    };
    historyEl.appendChild(b);
  });
}

function addMessage(role, content) {
  const wrapper = document.createElement("div");
  wrapper.className = "message " + role;

  const label = document.createElement("div");
  label.className = "message-label";
  label.textContent = role === "user" ? "Tu" : "NOVA";

  const bubble = document.createElement("div");
  bubble.className = "message-bubble";
  // Testo semplice, non HTML: evita di eseguire contenuti ricevuti dall'AI.
  bubble.textContent = content;

  wrapper.append(label, bubble);
  chatEl.appendChild(wrapper);
  return wrapper;
}

function renderChat() {
  const c = activeConversation();
  chatEl.innerHTML = "";

  if (!c || !c.messages.length) {
    const welcome = document.createElement("div");
    welcome.className = "welcome";
    welcome.id = "welcome";
    welcome.innerHTML = `
      <div class="welcome-symbol">__LOGO__</div>
      <h1>Come posso aiutarti?</h1>
      <div class="subtitle">La tua prossima idea inizia qui.</div>
      <div class="suggestions">
        <button class="suggestion" data-prompt="Aiutami a trovare idee creative per un nuovo progetto.">
          <div class="suggestion-icon">✳</div>
          <div class="suggestion-title">Idee creative</div>
          <div class="suggestion-description">Dai forma alle tue idee e scopri nuove possibilità.</div>
        </button>
        <button class="suggestion" data-prompt="Aiutami a studiare un argomento difficile, spiegandomelo in modo semplice.">
          <div class="suggestion-icon">⌘</div>
          <div class="suggestion-title">Studia con NOVA</div>
          <div class="suggestion-description">Spiegazioni chiare, esempi e aiuto nello studio.</div>
        </button>
      </div>`;
    chatEl.appendChild(welcome);
    bindSuggestions();
    return;
  }

  c.messages.forEach(m => addMessage(m.role === "user" ? "user" : "assistant", m.content));
  chatEl.scrollTop = chatEl.scrollHeight;
}

function bindSuggestions() {
  chatEl.querySelectorAll("[data-prompt]").forEach(b => {
    b.addEventListener("click", () => {
      promptEl.value = b.dataset.prompt;
      promptEl.focus();
      resizePrompt();
    });
  });
}

function resizePrompt() {
  promptEl.style.height = "auto";
  promptEl.style.height = Math.min(promptEl.scrollHeight, 160) + "px";
}

async function sendMessage(text) {
  text = text.trim();
  if (!text || busy) return;

  if (!activeConversation()) createConversation();
  const c = activeConversation();

  if (!c.messages.length) {
    c.title = text.length > 35 ? text.slice(0, 35) + "…" : text;
  }

  c.messages.push({role: "user", content: text});
  renderHistory();
  renderChat();

  promptEl.value = "";
  resizePrompt();
  busy = true;
  sendBtn.disabled = true;

  const loading = document.createElement("div");
  loading.className = "message assistant";
  loading.innerHTML = '<div class="message-label">NOVA</div><div class="typing"><span></span><span></span><span></span></div>';
  chatEl.appendChild(loading);
  chatEl.scrollTop = chatEl.scrollHeight;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        message: text,
        history: c.messages.slice(0, -1)
      })
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Errore del server");

    loading.remove();
    c.messages.push({role: "assistant", content: data.reply});
    addMessage("assistant", data.reply);
  } catch (error) {
    loading.remove();
    const message = "Non riesco a contattare il servizio AI. " + error.message;
    c.messages.push({role: "assistant", content: message});
    addMessage("assistant", message);
  } finally {
    busy = false;
    sendBtn.disabled = false;
    promptEl.focus();
    chatEl.scrollTop = chatEl.scrollHeight;
    renderHistory();
  }
}

document.getElementById("composer").addEventListener("submit", e => {
  e.preventDefault();
  sendMessage(promptEl.value);
});

promptEl.addEventListener("input", resizePrompt);

promptEl.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    document.getElementById("composer").requestSubmit();
  }
});

document.getElementById("newChat").addEventListener("click", () => {
  createConversation();
  sidebar.classList.remove("open");
  promptEl.focus();
});

document.getElementById("menuBtn").addEventListener("click", () => {
  sidebar.classList.toggle("open");
});

bindSuggestions();
createConversation();
</script>
</body>
</html>
"""


# Simbolo SVG originale a quattro assi di simmetria.
LOGO = """
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"
     fill="none" stroke="currentColor" stroke-width="4.5"
     stroke-linejoin="round">
  <path d="M50 8 L69 27 L69 40 L50 50 L31 40 L31 27 Z"/>
  <path d="M92 50 L73 69 L60 69 L50 50 L60 31 L73 31 Z"/>
  <path d="M50 92 L31 73 L31 60 L50 50 L69 60 L69 73 Z"/>
  <path d="M8 50 L27 31 L40 31 L50 50 L40 69 L27 69 Z"/>
  <path d="M50 39 L61 50 L50 61 L39 50 Z" fill="currentColor"/>
</svg>
"""

# Il logo viene inserito nelle varie posizioni dell'interfaccia.
HTML = HTML.replace("__LOGO__", LOGO)


class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML


@app.post("/api/chat")
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Messaggio vuoto.")

    try:
        client = Client(NOVA_API_URL)
        result = client.predict(
            message,
            request.history or [],
            api_name="/predict"
        )
        return {"reply": str(result)}
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                f"{type(exc).__name__}: {exc}. "
                "Controlla che il servizio AI su Kaggle sia attivo."
            )
        )


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
