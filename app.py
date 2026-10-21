
import os
import gradio as gr
from gradio_client import Client

# Manteniamo il collegamento attuale a NOVA su Kaggle
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


CSS = """
.gradio-container {
    background:
        radial-gradient(ellipse at 50% 0%, #20204a 0%, transparent 55%),
        #090d1b !important;
    color: #eef0ff !important;
    min-height: 100vh;
}

#nova-header {
    max-width: 900px;
    margin: 0 auto;
    padding: 24px 12px 12px;
    text-align: center;
}

#nova-logo {
    width: 68px;
    height: 68px;
    margin: 0 auto 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 22px;
    background: linear-gradient(135deg, #7464ff, #20d5f5);
    box-shadow: 0 0 36px #6558e855;
    color: white;
    font-size: 38px;
    font-weight: 800;
}

#nova-header h1 {
    margin: 0;
    font-size: 36px;
    letter-spacing: 5px;
    color: white;
}

#nova-header p {
    color: #aab4d3;
    margin-top: 8px;
}

#nova-status {
    display: inline-block;
    padding: 6px 12px;
    margin-top: 8px;
    border: 1px solid #285f55;
    border-radius: 999px;
    color: #70e6bd;
    font-size: 12px;
}

#nova-chatbot {
    max-width: 900px;
    margin: 0 auto;
    border: 1px solid #292e49 !important;
    border-radius: 20px !important;
    background: #0e1323 !important;
}

#nova-chatbot .message {
    border-radius: 18px !important;
    padding: 12px 16px !important;
    line-height: 1.6 !important;
}

#nova-chatbot .message.user {
    background: linear-gradient(135deg, #6254dc, #5144bd) !important;
    color: white !important;
    border: none !important;
}

#nova-chatbot .message.bot {
    background: #1a2035 !important;
    color: #edf0ff !important;
    border: 1px solid #2b3351 !important;
}

#nova-input textarea {
    background: #151b2d !important;
    color: white !important;
    border: 1px solid #343b5a !important;
    border-radius: 16px !important;
}

#nova-input textarea:focus {
    border-color: #8072ff !important;
    box-shadow: 0 0 0 2px #8072ff30 !important;
}

button.primary {
    background: linear-gradient(135deg, #7464ff, #5144bd) !important;
    border: none !important;
    border-radius: 14px !important;
}

footer {
    display: none !important;
}

@media (max-width: 600px) {
    #nova-header h1 {
        font-size: 30px;
    }

    #nova-chatbot {
        border-radius: 14px !important;
    }
}
"""


with gr.Blocks(
    title="NOVA AI",
    theme=gr.themes.Soft(
        primary_hue="violet",
        secondary_hue="blue",
        neutral_hue="slate"
    ),
    css=CSS
) as app:

    gr.HTML("""
    <div id="nova-header">
        <div id="nova-logo">N</div>
        <h1>NOVA</h1>
        <p>La tua AI personale ✦</p>
        <div id="nova-status">● Assistente AI</div>
    </div>
    """)

    gr.ChatInterface(
        fn=rispondi,
        chatbot=gr.Chatbot(
            height=500,
            show_label=False,
            elem_id="nova-chatbot"
        ),
        textbox=gr.Textbox(
            placeholder="Scrivi un messaggio a NOVA...",
            show_label=False,
            container=False,
            lines=1,
            max_lines=5,
            elem_id="nova-input"
        ),
        submit_btn="Invia",
        stop_btn="Interrompi"
    )


app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
