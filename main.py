import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    try:
        user_prompt = sys.argv[1]
    except IndexError:
        print("The prompt was not provided.")
        sys.exit(1)

    try:
        verbose = sys.argv[2] == "--verbose"
    except IndexError:
        verbose = False

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    print(response.text)

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
