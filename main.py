import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from promts import system_prompt
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if api_key == None:
    raise RuntimeError("Something wrong with you API key...")



parser = argparse.ArgumentParser(description="bootdev-ai")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

model_name = 'gemini-2.5-flash'

for _ in range(20):
    
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )

    if response.candidates:
        for c in response.candidates:
            messages.append(c.content)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.usage_metadata == None:
        raise RuntimeError("Something went wrong...")



    function_responses = []

    function_calls = response.function_calls
    if function_calls != None:
        for function_call in function_calls:
            #print(f"Calling function: {function_call.name}({function_call.args})")
            result = call_function(function_call, args.verbose)
        
            if not result.parts:
                raise RuntimeError("No parts in function response")
            if result.parts[0].function_response is None:
                raise RuntimeError("No function_response in parts[0]")
            if result.parts[0].function_response.response is None:
                raise RuntimeError("No response in function_response")

            function_responses.append(result.parts[0])
            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")
            
        messages.append(types.Content(role="user", parts=function_responses))
        #print("added tool responses to messages:", len(function_responses))
    else:
        print(response.text)
        break

else:
    print("Error: reached max iterations without a final response")
    raise SystemExit(1)
