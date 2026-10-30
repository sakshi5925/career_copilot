
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from the environment")

client = Groq(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "user", "content": "Say hello"}
        ],
        temperature=0.2,
    )

    print(response.choices[0].message.content)

except Exception as error:
    print("Error type:", type(error).__name__)
    print("Error:", error)
