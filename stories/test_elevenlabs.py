import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

voice_id = "21m00Tcm4TlvDq8ikWAM"

text = """
नमस्ते! यह हमारे StoryVerse प्रोजेक्ट का पहला ElevenLabs ऑडियो टेस्ट है।
आज हम देख रहे हैं कि ElevenLabs हिंदी कहानी को कितनी अच्छी और प्राकृतिक आवाज़ में बदल सकता है।
"""

audio = client.text_to_speech.convert(
    voice_id=voice_id,
    model_id="eleven_multilingual_v2",
    text=text,
    output_format="mp3_44100_128",
)

output_file = "stories/test_audio.mp3"

with open(output_file, "wb") as f:
    for chunk in audio:
        f.write(chunk)

print(f"Audio generated successfully: {output_file}")