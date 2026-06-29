import os, argparse, sys
from dotenv import load_dotenv
from prompts import system_prompt
from functions.call_function import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("Try having an API key this time, nerd.")

from google import genai

from google.genai import types

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="User Request")
parser.add_argument("user_prompt", type=str, help="User's prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]   

def main():

    for _ in range(20):

        response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt, temperature=0),
        )

        if response.candidates:
            for cand in response.candidates:
                messages.append(cand.content)

        if response.usage_metadata == None:
            raise RuntimeError("No sufficient metadata for the request made.")

        if response.function_calls:
            
            function_responses = []
            
            for call in response.function_calls:    

                function_call_result = call_function(call, verbose=args.verbose)
        
                if not function_call_result.parts:
                    raise Exception("Content object contains no parts")
        
                if not function_call_result.parts[0].function_response:
                    raise Exception("Function call produced no response")
        
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Function call produced no response")

                function_responses.append(function_call_result.parts[0])
            
            messages.append(types.Content(role="user", parts=function_responses))
            
        if not response.function_calls:
            print (response.text)
            return
    
    sys.exit(1)

if __name__ == "__main__":
    main()
