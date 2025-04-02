from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gtts import gTTS
import os
import requests

app = FastAPI()

WEBHOOK_URL = "https://auto.ahmedds.us/webhook-test/35532d5a-10ff-4d1f-8bb1-1549dccf6cf1"

class TextRequest(BaseModel):
    text: str
    language: str = "ar"
    slow: bool = False

@app.post("/text-to-speech/")
def text_to_speech(request: TextRequest):
    try:
        output_file = "output.mp3"
        tts = gTTS(text=request.text, lang=request.language, slow=request.slow)
        tts.save(output_file)

        # إرسال إشعار إلى Webhook بعد إنشاء الملف
        webhook_data = {"message": "Text converted to speech successfully", "file": output_file}
        requests.post(WEBHOOK_URL, json=webhook_data)

        return {"message": "Audio file created", "file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
