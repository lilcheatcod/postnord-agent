from flask import Flask, request, send_file
from twilio.twiml.voice_response import VoiceResponse
import requests
import os

app = Flask(__name__)

@app.route("/voice", methods=['POST'])
def voice():
    # Start Twilio response
    response = VoiceResponse()

    # Get user's speech as text (placeholder - actual Whisper API would be used)
    user_text = "Mitt paket är fast i Tyskland. Vad händer?"

    # Simulate GPT response logic (normally this would call OpenAI API)
    if "Tyskland" in user_text or "fast" in user_text:
        ai_response = (
            "Ditt paket är för närvarande fast i tullen i Tyskland. "
            "Anledningen är att tullmyndigheterna väntar på en kopia av fakturan. "
            "För att frigöra paketet måste du skicka en kopia av ditt inköpskvitto till PostNord via deras tullportal."
        )
    else:
        ai_response = "Jag kunde inte förstå ditt ärende. Kan du upprepa vad problemet gäller med ditt paket?"

    # Convert response to speech using ElevenLabs API
    audio_url = elevenlabs_tts(ai_response)

    # Tell Twilio to play the MP3 file
    response.play(audio_url)
    return str(response)

def elevenlabs_tts(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL"  # Rachel voice
    headers = {
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        # Save audio to static file
        with open("static/response.mp3", "wb") as f:
            f.write(response.content)
        return request.url_root + "static/response.mp3"
    else:
        return "https://yourdomain.com/static/fallback.mp3"

if __name__ == "__main__":
    app.run(debug=True)
