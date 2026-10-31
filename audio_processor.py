
from gtts import gTTS
from io import BytesIO


def generate_audio(text, language="en"):

    if not text.strip():
        return None

    audio_buffer = BytesIO()

    speech = gTTS(
        text=text,
        lang=language
    )

    speech.write_to_fp(audio_buffer)

    audio_buffer.seek(0)

    return audio_buffer
