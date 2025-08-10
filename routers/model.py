from groq import Groq
import os
from pathlib import Path
from dotenv import load_dotenv
import assemblyai as aai
from .weather import fetch_days  # assuming it's a relative import
import asyncio

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

# Don't run this on import! Move to __main__
async def main():
    data = await fetch_days("Akure,NG")
    print(data)

client = Groq(api_key=os.getenv("GROQ_API_KEY") or "your_default_key")

async def build_system_prompt(city="Akure,NG") -> str:
    data = await fetch_days(city)
    return f"""
You are a helpful assistant that can answer questions on weather fit for election and nothing else.

Here is the weather data for {city}:
{data}

You are not allowed to answer any other questions outside of this context.
"""


# def chat(question: str) -> str:
#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": question}
#         ],
#         temperature=1,
#         max_tokens=1024,
#         top_p=1,
#         stream=True,
#     )

#     all_words = []
#     for chunk in response:
#         all_words.append(chunk.choices[0].delta.content or "")
#     return "".join(all_words)


async def ask_question(question: str, city="Akure,NG"):
    prompt = await build_system_prompt(city)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,  # Optional: switch to True if needed
    )

    return response.choices[0].message.content



if __name__ == "__main__":
    asyncio.run(main())  # ✅ only runs when executed directly
