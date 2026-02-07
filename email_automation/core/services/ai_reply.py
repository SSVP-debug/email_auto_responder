import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_acknowledgement(subject):
    """
    Generates a polite, professional automated acknowledgement.
    Falls back to static text if Gemini fails.
    """

    fallback = (
        "Thank you for your email.\n\n"
        "This is an automated acknowledgment to let you know "
        "that I’ve received your message. "
        "I’ll review it and get back to you soon.\n\n"
        "Best regards"
    )

    try:
        prompt = (
            "Write a short, professional email acknowledgement.\n"
            "It must clearly say it is automated.\n"
            "Do NOT promise any decision.\n"
            f"Email subject: {subject}"
        )

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        if response and response.text:
            return response.text.strip()

    except Exception:
        pass  # silent fallback

    return fallback
