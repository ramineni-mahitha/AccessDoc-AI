
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


def translate_text(text, target_language="Telugu"):

    if not text.strip():
        return ""

    if client is None:
        raise ValueError("Gemini API key not found. Check your .env file.")

    prompt = f"""
    Translate the following document into {target_language}.
    Preserve the meaning, dates, numbers, names and important details.
    Do not summarize or remove information.

    Document:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text


def simplify_text(text):

    if not text.strip():
        return ""

    if client is None:
        raise ValueError("Gemini API key not found. Check your .env file.")

    prompt = f"""
    Simplify the following official document into easy,
    clear English that an ordinary person can understand.

    Important instructions:
    1. Use simple words and short sentences.
    2. Preserve all dates, numbers and deadlines.
    3. Preserve eligibility requirements and instructions.
    4. Do not remove important information.
    5. Do not invent facts.
    6. Use headings and bullet points where helpful.

    Document:
    {text}
    """

    for attempt in range(3):

        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            if response.text:
                return response.text

            raise ValueError("Gemini returned an empty response.")

        except Exception as e:

            if "503" in str(e) and attempt < 2:
                time.sleep(5)
            else:
                raise

    return ""
