import asyncio
import logging
import itertools
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from config import openai_api_keys

app = FastAPI()

# API kalitlarini navbat bilan aylantirish
api_key_cycle = itertools.cycle(openai_api_keys)

# Maksimal 5 ta parallel so‘rovni qo‘llab-quvvatlash
semaphore = asyncio.Semaphore(5)

# OpenAI mijoz obyektini global holatda yaratish
clients = {key: OpenAI(api_key=key) for key in openai_api_keys}


class TextInput(BaseModel):
    text: str


async def generate_speech(text):
    """Generate speech using OpenAI API asynchronously with key rotation."""
    async with semaphore:
        attempts = len(openai_api_keys)  # API kalitlar soni
        last_exception = None

        for _ in range(attempts):
            api_key = next(api_key_cycle)
            client = clients[api_key]  # Mavjud OpenAI mijozdan foydalanish

            try:
                response = await asyncio.to_thread(
                    client.audio.speech.create,
                    model="tts-1",
                    voice="alloy",
                    input=text,
                    response_format="opus"
                )
                return response.content

            except Exception as e:
                logging.error(f"API Key {api_key[:5]}... ishlamayapti: {e}")
                last_exception = e

        logging.error(f"Barcha API kalitlar ishlamayapti: {last_exception}")
        return ""


@app.post("/generate_speech")
async def generate_speech_api(request: TextInput):
    """FastAPI endpoint for text-to-speech generation."""
    try:
        audio_content = await generate_speech(request.text)
        return {"audio_data": audio_content.hex()} if audio_content else {"error": "Speech generation failed"}
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        return {"audio_data": "", "error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
