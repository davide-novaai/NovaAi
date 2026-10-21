
import os
import gradio as gr
from gradio_client import Client

NOVA_API_URL = "https://4e203d07b8df8e1a72.gradio.live"

def rispondi(messaggio, cronologia):
    if not messaggio or not messaggio.strip():
        return "Scrivimi qualcosa e ti risponderò!"

    try:
        client = Client(NOVA_API_URL)
        risposta = client.predict(
            messaggio,
            api_name="/predict"
        )
        return str(risposta)

    except Exception as e:
        return (
            "NOVA non riesce a raggiungere il modello su Kaggle. "
            "Controlla che il notebook sia attivo. "
            f"Dettagli: {type(e).__name__}: {e}"
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

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
