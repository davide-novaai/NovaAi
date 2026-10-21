
import os
import gradio as gr
from gradio_client import Client

NOVA_API_URL = "https://4e203d07b8df8e1a72.gradio.live"

def rispondi(messaggio, cronologia):
    if not messaggio or not messaggio.strip():
        return "Scrivimi qualcosa e ti risponderò!"

    try:
        client = Client(NOVA_API_URL)
        return str(client.predict(messaggio, api_name="/predict"))
    except Exception as e:
        return f"NOVA non riesce a rispondere. Dettagli: {type(e).__name__}: {e}"

CSS = """
.gradio-container {
    background: #101114 !important;
    color: #f4f4f5 !important;
}
#header {
    max-width: 850px;
    margin: auto;
    padding: 18px 8px;
}
#logo {
    display: inline-flex;
    width: 40px;
    height: 40px;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: #29262f;
    color: #d2c6ff;
    font-size: 25px;
    margin-right: 12px;
}
#brand {
    display: flex;
    align-items: center;
    gap: 2px;
}
#brand h1 {
    font-size: 23px;
    margin: 0;
    letter-spacing: 1px;
}
#subtitle {
    color: #a1a1aa;
    font-size: 13px;
    margin: 3px 0 0 52px;
}
#welcome {
    text-align: center;
    padding: 65px 10px 30px;
}
#welcome h2 {
    color: #f4f4f5;
    font-size: 30px;
    font-weight: 600;
}
#chat {
    max-width: 850px;
    margin: auto;
    border: none !important;
    background: transparent !important;
}
#chat .message {
    border-radius: 20px !important;
    padding: 12px 16px !important;
}
#chat .message.user {
    background: #292a2f !important;
    color: #f4f4f5 !important;
}
#chat .message.bot {
    background: #17181c !important;
    color: #f4f4f5 !important;
}
#input textarea {
    background: #1b1c20 !important;
    color: #f4f4f5 !important;
    border: 1px solid #393a40 !important;
    border-radius: 20px !important;
    padding: 15px !important;
}
button.primary {
    background: #f4f4f5 !important;
    color: #18181b !important;
    border: none !important;
    border-radius: 50px !important;
}
footer {
    display: none !important;
}
"""

with gr.Blocks(
    title="NOVA",
    theme=gr.themes.Base(
        primary_hue="neutral",
        neutral_hue="zinc"
    ),
    css=CSS
) as app:
    gr.HTML("""
    <div id="header">
      <div id="brand">
        <div id="logo">✳</div>
        <h1>NOVA</h1>
      </div>
      <div id="subtitle">Creata da Davide Breno</div>
    </div>
    <div id="welcome">
      <h2>Come posso aiutarti?</h2>
      <p style="color:#a1a1aa">Chiedimi qualcosa. Partiamo da lì.</p>
    </div>
    """)

    gr.ChatInterface(
        fn=rispondi,
        chatbot=gr.Chatbot(
            height=430,
            show_label=False,
            elem_id="chat"
        ),
        textbox=gr.Textbox(
            placeholder="Scrivi a NOVA...",
            show_label=False,
            container=False,
            lines=2,
            max_lines=6,
            elem_id="input"
        ),
        submit_btn="↑",
        stop_btn="Interrompi"
    )

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
