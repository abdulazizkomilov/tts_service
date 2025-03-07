import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from config import openai_api_key

app = FastAPI()

open_ai_key = openai_api_key


class TextInput(BaseModel):
    text: str


async def generate_speech(text):
    """Generate speech using OpenAI API asynchronously."""
    try:
        client = OpenAI(api_key=open_ai_key)

        response = await asyncio.to_thread(
            client.audio.speech.create,
            model="tts-1",
            voice="alloy",
            input=text,
            response_format="opus"
        )

        return response.content
    except Exception as e:
        print(f"Error generating speech: {e}")
        return ""


@app.post("/generate_speech")
async def generate_speech_api(request: TextInput):
    audio_content = await generate_speech(request.text)
    return {"audio_data": audio_content.hex()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
