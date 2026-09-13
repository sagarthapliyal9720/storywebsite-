import os
from elevenlabs.client import ElevenLabs


client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)


def generate_audio(text, output_path, voice_id):
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        text=text,
        output_format="mp3_44100_128",
    )

    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
            