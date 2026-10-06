# src/youtube_university/llm.py
"""Everything that talks to the local LLM (Ollama)."""
import ollama

MODEL = "llama3.2:3b"


def ask_llm(prompt: str) -> str:
    """Send one prompt to the local model and return its reply as text."""
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt},
                  {"role": "system", "content": "Answer like a pirate."}],  # a conversation = list of {role, content}
        options={"temperature": 0}
    )
    return response.message.content



if __name__ == "__main__":  # like Main(): runs only when you execute this file directly
    print(ask_llm("In one sentence, what is a curriculum?"))