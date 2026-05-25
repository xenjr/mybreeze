from fastapi import FastAPI, Form, BackgroundTasks, Response
from supabase import create_client
from google import genai
from google.genai import types
from twilio.rest import Client as TwilioClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
twilio = TwilioClient(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

def get_or_create_user(telefono: str):
    result = supabase.table("usuarios").select("*").eq("telefono", telefono).execute()
    if result.data:
        return result.data[0]
    nuevo = supabase.table("usuarios").insert({"telefono": telefono}).execute()
    return nuevo.data[0]

def procesar(telefono: str, mensaje: str):
    usuario = get_or_create_user(telefono)
    uid = usuario["id"]

    # Guardar mensaje del usuario
    supabase.table("historial_chat").insert({
        "usuario_id": uid,
        "rol": "user",
        "contenido": mensaje
    }).execute()

    # Detectar si es un número suelto (glucosa directa)
    try:
        glucosa = float(mensaje.strip())
        supabase.table("registros").insert({
            "usuario_id": uid,
            "glucosa": glucosa,
            "mensaje_original": mensaje
        }).execute()
        respuesta = f"Registré tu glucosa: {glucosa} mg/dL ✓"
    except ValueError:
        # Es conversación — construir contexto
        contexto = supabase.table("contexto").select("resumen").eq("usuario_id", uid).execute()
        historial = supabase.table("historial_chat").select("*").eq("usuario_id", uid).order("creado_a", desc=True).limit(8).execute()

        resumen = contexto.data[0]["resumen"] if contexto.data else "Paciente nueva sin historial previo."

        system_prompt = f"""
Eres un asistente cálido y preciso para una paciente con diabetes.
Perfil y contexto acumulado: {resumen}
Tu rol es escuchar, acompañar y detectar patrones emocionales y físicos.
No des prescripciones médicas. Sé humana y directa.
"""
        chat_history = [
            types.Content(
                role=msg["rol"],
                parts=[types.Part(text=msg["contenido"])]
            )
            for msg in reversed(historial.data)
        ]

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(system_instruction=system_prompt),
            contents=chat_history
        )
        respuesta = response.text

    # Guardar respuesta
    supabase.table("historial_chat").insert({
        "usuario_id": uid,
        "rol": "model",
        "contenido": respuesta
    }).execute()

    # Enviar por WhatsApp
    twilio.messages.create(
        from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
        body=respuesta,
        to=f"whatsapp:{telefono}"
    )

@app.post("/webhook")
async def webhook(background_tasks: BackgroundTasks, From: str = Form(...), Body: str = Form(...)):
    telefono = From.replace("whatsapp:", "")
    background_tasks.add_task(procesar, telefono, Body)
    return Response(content="<Response></Response>", media_type="application/xml")