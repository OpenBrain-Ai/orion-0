from random import uniform
from time import sleep
from groq import Groq
import os

model_analysis = "qwen/qwen3-32b"
model_reasoning = "llama-3.3-70b-compound"
model_thinking = "llama-3.3-70b-instruct" 
model_synthesis = "openai/gpt-oss-120b" 

api_key = os.environ.get("AGENT")
client = Groq(api_key=api_key)

def generate(user_input: str, system_msg: str, model: str) -> str:
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error with {model}: {e}"

def is_simple(query: str) -> bool:
    if "--deep" in query:
        return False
    return True

def deep_think(query: str) -> tuple:
    print("analysing...", end="\r")
    analysis = generate(query, 
                        "Provide a deep analysis of core requirements.", model_analysis)

    print("reasoning...", end="\r")
    reasoning = generate(f"Query: {query}\nAnalysis: {analysis}", 
                         "Develop a logical step-by-step solution.", model_reasoning)

    print("thinking... ", end="\r")
    thinking = generate(f"Query: {query}\nLogic: {reasoning}", 
                        "Critique the logic and look for edge cases.", model_thinking)
    
    print("generating...", end="\r")
    return analysis, reasoning, thinking

def simple_response(query: str) -> str:
    print("generating...", end="\r")
    response = generate(query, "You are a helpful assistant called Orion-0 developed by OpenBrain. Provide concise and accurate responses. If something is wrong dont lie.", model_synthesis)
    return response

def say(response: str) -> None:
    print(" " * 20, end="\r")
    response = f"Orion-0> {response}"
    for char in response:
        print(char, end="", flush=True)
        sleep(uniform(0.0001, 0.005))

def main() -> None:
    print("--- Orion-0 Multi-Model System ---")
    while True:
        query = input("\n>>> ")
        if query.lower() in ["exit", "quit"]:
            break
        
        if is_simple(query):
            response = simple_response(query)
            say(response)
            continue

        query = query.replace("--deep", "")
        
        analysis, reasoning, thinking = deep_think(query)
        final_prompt = f"Original Query: {query}\nAnalysis: {analysis}\nLogic: {reasoning}\nCritique: {thinking}"
        response = generate(final_prompt, "You are a helpful assistant called Orion-0 developed by OpenBrain. Provide concise and accurate responses. If something is wrong dont lie.", model_synthesis)
        say(response)

if __name__ == "__main__":
    main()