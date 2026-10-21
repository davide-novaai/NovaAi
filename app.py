
import os
import requests
import gradio as gr

HF_TOKEN = os.environ.get("HF_TOKEN")
MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

def rispondi(messaggio, cronologia):
    if not HF_TOKEN:
        return "NOVA deve ancora essere collegata al servizio AI."

    messaggi = [
        {
            "role": "system",
            "content": (
                "Ti chiami NOVA. Sei un'assistente AI personale, "
                "amichevole e intelligente. Rispondi in italiano."
            )
        }
    ]

    for elemento in (cronologia or [])[-10:]:
        if isinstance(elemento, dict):
            ruolo = elemento.get("role")
            contenuto = elemento.get("content")
            if ruolo in ["user", "assistant"] and isinstance(contenuto, str):
                messaggi.append({
                    "role": ruolo,
                    "content": contenuto
                })

    messaggi.append({"role": "user", "content": messaggio})

    try:
        risposta = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": messaggi,
                "max_tokens": 250
            },
            timeout=60
        )
        risposta.raise_for_status()
        dati = risposta.json()
        return dati["choices"][0]["message"]["content"]

    except Exception:
        return (
            "Non riesco a contattare il servizio AI. "
            "Controlla la configurazione e riprova."
        )

with gr.Blocks(title="NOVA AI", theme=gr.themes.Soft()) as app:
    gr.HTML("""
    <div style="text-align:center;padding:25px 10px">
      <div style="display:inline-flex;width:70px;height:70px;
      align-items:center;justify-content:center;border-radius:50%;
      background:linear-gradient(135deg,#6d5dfc,#00d4ff);
      color:white;font-size:34px;font-weight:bold">N</div>
      <h1>NOVA</h1>
      <p>La tua AI personale ✦</p>
    </div>
    """)
    gr.ChatInterface(fn=rispondi)

app.launch()
