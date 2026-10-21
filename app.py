
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


CSS = """
.gradio-container {
    background: #212121 !important;
    color: #ececec !important;
    min-height: 100vh;
}
body {
    background: #212121 !important;
}
#sidebar {
    background: #171717 !important;
    border-right: 1px solid #303030;
    min-height: 95vh;
    padding: 18px 12px;
}
#nova-name {
    padding: 5px 8px 20px;
}
#main {
    max-width: 900px;
    width: 100%;
    margin: 0 auto;
    padding: 12px 22px;
}
#welcome {
    text-align: center;
    padding: 90px 10px 30px;
    color: #ececec;
    font-size: 25px;
    font-weight: 500;
}
#chatbot {
    background: transparent !important;
    border: none !important;
}
#chatbot .message {
    border: none !important;
    border-radius: 20px !important;
    padding: 12px 16px !important;
    line-height: 1.65 !important;
}
#chatbot .message.user {
    background: #303030 !important;
    color: #f5f5f5 !important;
}
#chatbot .message.bot {
    background: transparent !important;
    color: #ececec !important;
}
#composer {
    background: #303030 !important;
    border: 1px solid #454545 !important;
    border-radius: 25px !important;
    padding: 9px 12px !important;
    gap: 8px !important;
}
#message-box textarea {
    background: transparent !important;
    color: #f5f5f5 !important;
    border: none !important;
    box-shadow: none !important;
    padding: 9px 6px !important;
    font-size: 15px !important;
}
#send-button {
    min-width: 42px !important;
    width: 42px !important;
    height: 42px !important;
    min-height: 42px !important;
    border-radius: 50% !important;
    background: #f5f5f5 !important;
    color: #212121 !important;
    border: none !important;
    font-size: 21px !important;
    font-weight: bold !important;
}
#new-chat {
    background: transparent !important;
    border: 1px solid #414141 !important;
    border-radius: 12px !important;
    color: #eeeeee !important;
    text-align: left !important;
}
footer {
    display: none !important;
}
button:hover {
    opacity: .88;
}
@media (max-width: 650px) {
    #sidebar {
        min-width: 76px !important;
        padding: 12px 6px;
    }
    #main {
        padding: 8px;
    }
    #welcome {
        padding-top: 55px;
        font-size: 21px;
    }
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

    cronologia = gr.State([])

    with gr.Row(equal_height=False, elem_id="layout"):

        with gr.Column(
            scale=0,
            min_width=175,
            elem_id="sidebar"
        ):

            gr.HTML("""
            <div id="nova-name">
              <svg viewBox="0 0 120 120"
                   width="42" height="42"
                   xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <linearGradient id="novaLogo"
                                  x1="0" y1="0"
                                  x2="1" y2="1">
                    <stop offset="0%"
                          stop-color="#B6A5FF"/>
                    <stop offset="100%"
                          stop-color="#64D9F2"/>
                  </linearGradient>
                </defs>
                <g fill="none"
                   stroke="url(#novaLogo)"
                   stroke-width="8"
                   stroke-linecap="round"
                   stroke-linejoin="round">
                  <path d="M60 17 C73 17 82 27 82 39 C82 46 78 51 72 56 L49 74 C39 82 38 94 47 101"/>
                  <path d="M87 31 C99 38 101 51 95 61 C91 68 85 71 77 72 L49 72 C36 72 27 81 28 93"/>
                  <path d="M101 60 C101 73 91 82 79 82 C72 82 67 78 62 72 L44 49 C36 39 24 38 17 47"/>
                  <path d="M89 88 C82 100 69 102 59 96 C52 92 49 86 48 78 L48 50 C48 37 39 28 27 29"/>
                  <path d="M60 103 C47 103 38 93 38 81 C38 74 42 69 48 64 L71 46 C81 38 82 26 73 19"/>
                  <path d="M31 89 C20 82 18 69 24 59 C28 52 34 49 42 48 L70 48 C83 48 92 39 91 27"/>
                </g>
                <circle cx="60" cy="60" r="5"
                        fill="#E8E7FF"/>
              </svg>
            </div>
            """)

            nuovo = gr.Button(
                "＋  Nuova chat",
                elem_id="new-chat"
            )

        with gr.Column(
            scale=1,
            min_width=0,
            elem_id="main"
        ):

            benvenuto = gr.HTML(
                '<div id="welcome">Come posso aiutarti?</div>'
            )

            chat = gr.Chatbot(
                type="messages",
                height=510,
                show_label=False,
                elem_id="chatbot"
            )

            with gr.Row(elem_id="composer"):

                messaggio = gr.Textbox(
                    placeholder="Scrivi a NOVA...",
                    show_label=False,
                    container=False,
                    lines=1,
                    max_lines=6,
                    scale=1,
                    elem_id="message-box"
                )

                invia_btn = gr.Button(
                    "↑",
                    variant="primary",
                    elem_id="send-button",
                    scale=0,
                    min_width=42
                )

    def invia(messaggio, cronologia):
        cronologia = list(cronologia or [])

        if not messaggio or not messaggio.strip():
            return (
                cronologia,
                "",
                cronologia,
                gr.update()
            )

        risposta = rispondi(
            messaggio.strip(),
            cronologia
        )

        cronologia.extend([
            {
                "role": "user",
                "content": messaggio.strip()
            },
            {
                "role": "assistant",
                "content": risposta
            }
        ])

        return (
            cronologia,
            "",
            cronologia,
            gr.update(visible=False)
        )

    def nuova_chat():
        return (
            [],
            "",
            [],
            gr.update(visible=True)
        )

    outputs = [
        chat,
        messaggio,
        cronologia,
        benvenuto
    ]

    inputs = [
        messaggio,
        cronologia
    ]

    invia_btn.click(
        invia,
        inputs=inputs,
        outputs=outputs
    )

    messaggio.submit(
        invia,
        inputs=inputs,
        outputs=outputs
    )

    nuovo.click(
        nuova_chat,
        outputs=[
            chat,
            messaggio,
            cronologia,
            benvenuto
        ]
    )


app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
