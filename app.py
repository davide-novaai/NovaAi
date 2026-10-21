import os
import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM

# Modello di NOVA
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

print("NOVA si sta avviando...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

modello = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)

print("NOVA è pronta!")

def rispondi(messaggio, cronologia):
    if not messaggio or not messaggio.strip():
        return "Scrivi qualcosa e NOVA ti risponderà!"

    messaggi = [
        {
            "role": "system",
            "content": (
                "Ti chiami NOVA. Sei un'assistente AI personale, "
                "intelligente, amichevole e disponibile. "
                "Rispondi in italiano, salvo diversa richiesta. "
                "Spiega le cose in modo chiaro."
            )
        }
    ]

    # Mantiene il contesto degli ultimi messaggi
    for elemento in (cronologia or [])[-10:]:
        if isinstance(elemento, dict):
            ruolo = elemento.get("role")
            contenuto = elemento.get("content")

            if ruolo in ["user", "assistant"] and isinstance(contenuto, str):
                messaggi.append({
                    "role": ruolo,
                    "content": contenuto
                })

    messaggi.append({
        "role": "user",
        "content": messaggio
    })

    input_ids = tokenizer.apply_chat_template(
        messaggi,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    )

    with torch.no_grad():
        output = modello.generate(
            input_ids,
            max_new_tokens=250,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )

    nuovi_token = output[0][input_ids.shape[-1]:]

    risposta = tokenizer.decode(
        nuovi_token,
        skip_special_tokens=True
    )

    return risposta.strip()

with gr.Blocks(
    title="NOVA AI",
    theme=gr.themes.Soft()
) as app:

    gr.HTML("""
    <div style="text-align:center;padding:25px 10px">
        <div style="
            display:inline-flex;
            width:70px;height:70px;
            align-items:center;justify-content:center;
            border-radius:50%;
            background:linear-gradient(135deg,#6d5dfc,#00d4ff);
            color:white;font-size:34px;font-weight:bold;
            box-shadow:0 0 30px #5145cd;
        ">N</div>
        <h1 style="margin-bottom:5px">NOVA</h1>
        <p>La tua AI personale ✦</p>
    </div>
    """)

    gr.ChatInterface(
        fn=rispondi,
        type="messages",
        chatbot=gr.Chatbot(height=450),
        textbox=gr.Textbox(
            placeholder="Scrivi un messaggio a NOVA...",
            lines=2
        )
    )

app.launch()
