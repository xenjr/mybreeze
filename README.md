# 🌬️ myBreeze

> *"No pienses de más. Esto para ti."*

Acompañamiento integral para personas con diabetes que sienten que la enfermedad es difícil de explicar —y de ser comprendidos al 100%.

**myBreeze** es un asistente conversacional por WhatsApp que combina inteligencia artificial con memoria a largo plazo para acompañar a pacientes con diabetes en su día a día: escuchando cómo se sienten, registrando su glucosa de forma natural, y construyendo un perfil clínico-emocional que evoluciona con el tiempo.

---

## ✨ ¿Qué hace?

- **Conversación natural** — Rose no necesita aprender comandos. Escribe como habla. El bot la escucha, responde con contexto y nunca la trata como paciente.
- **Registro automático de glucosa** — Si Rose escribe un número, se registra en Supabase con timestamp. Sin formularios, sin fricción.
- **Memoria acumulada** — Cada conversación alimenta un resumen clínico-emocional. Gemini siempre sabe quién es ella, cómo ha estado, y qué patrones están emergiendo.
- **Reporte interno** — Los datos estructurados (glucosa + emoción + timestamp) permiten correlaciones para el médico: ¿qué pasó los días antes de un pico?

---

## 🧠 El problema real

Los trackers de diabetes muestran curvas. Los médicos ven números. Nadie ve a la persona.

myBreeze captura lo que ningún glucómetro puede: el contexto emocional detrás de los datos. El estrés del martes, la alegría del domingo, el "estoy bien" dicho demasiado rápido.

---

## 🛠️ Stack

- **Backend:** Python + FastAPI (desplegado en Render)
- **Mensajería:** Twilio WhatsApp Sandbox
- **Base de datos y memoria:** Supabase (PostgreSQL)
- **IA:** Gemini 2.5 Flash Lite (Google GenAI SDK)
- **Contexto:** Historial de chat a corto plazo + resumen clínico a largo plazo

---

## 🗄️ Modelo de datos

```sql
usuarios          -- Identificación por número de teléfono
registros         -- Glucosa + emoción + timestamp
historial_chat    -- Últimos N mensajes (memoria a corto plazo)
contexto          -- Resumen clínico-emocional acumulado (memoria a largo plazo)
```

---

## 🚀 Instalación local

```bash
git clone https://github.com/xenjr/mybreeze.git
cd mybreeze
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Crea un archivo `.env` con:

```env
SUPABASE_URL=tu_project_url
SUPABASE_KEY=tu_anon_key
GEMINI_API_KEY=tu_api_key
TWILIO_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

```bash
uvicorn main:app --reload
```

---

## 🗺️ Roadmap

**Completado**
- [x] Webhook funcional con FastAPI
- [x] Integración con WhatsApp vía Twilio
- [x] Registro automático de glucosa con timestamp en Supabase
- [x] Conversación con contexto acumulado via Gemini
- [x] Memoria a corto y largo plazo
- [x] Deploy en Render (24/7)

**En progreso**
- [ ] Reescritura del system prompt centrado en la persona, no en la enfermedad
- [ ] Actualización automática del resumen de contexto (memory compression)
- [ ] Mensaje semanal de acompañamiento (versículo + imagen)

**Siguiente etapa**
- [ ] Preprocesamiento de correlación emocional-glucosa para reportes médicos
- [ ] Reporte narrativo generado por IA ("esta semana tuviste 4 días tranquilos")
- [ ] Interfaz web responsive para visualización de patrones

---

## ⚠️ Disclaimer

myBreeze es una herramienta de acompañamiento y registro personal. No sustituye el consejo, diagnóstico o tratamiento médico profesional.
