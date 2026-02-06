import os
from dotenv import load_dotenv
from google import genai
import argparse


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if api_key == None:
    raise RuntimeError("Something wrong with you API key...")


parser = argparse.ArgumentParser(description="bootdev-ai")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()


response = client.models.generate_content(
    model='gemini-2.5-flash', contents=args.user_prompt
)

if response.usage_metadata == None:
    raise RuntimeError("Something went wrong...")



print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
print(response.text)

