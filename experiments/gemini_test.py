import os
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


response = client.interactions.create(
    model="gemini-3.8-flash",
    input="Explain machine learning in two sentences."
)

print(response.output_text)