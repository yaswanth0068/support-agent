import os
from groq import Groq
from hindsight_client import Hindsight
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────
GROQ_API_KEY      = os.getenv("GROQ_API_KEY")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID")

groq_client = Groq(api_key=GROQ_API_KEY)

hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=HINDSIGHT_API_KEY
)

# ── Save memory ───────────────────────────────────────────
def save_memory(user_id: str, content: str):
    try:
        hindsight.retain(
            bank_id=HINDSIGHT_BANK_ID,
            content=content,
            context=f"support session for user {user_id}",
            metadata={"user_id": user_id}
        )
        print("[Memory saved]")
    except Exception as e:
        print(f"[Memory save failed: {e}]")

# ── Recall memories ───────────────────────────────────────
def recall_memories(user_id: str, query: str) -> str:
    try:
        results = hindsight.recall(
            bank_id=HINDSIGHT_BANK_ID,
            query=query,
            tags=[f"user:{user_id}"]
        )
        memories = [r.text for r in results.results if r.text]
        if not memories:
            return ""
        return "\n".join(memories)
    except Exception as e:
        print(f"[Memory recall failed: {e}]")
        return ""

# ── Agent reply ───────────────────────────────────────────
def get_reply(user_id: str, user_message: str) -> str:
    past = recall_memories(user_id, user_message)

    if past:
        system = f"""You are a helpful customer support agent.
You already know the following about this user from past conversations:
{past}

Use this context to give a personalized, informed response.
Do not ask for information you already know."""
    else:
        system = """You are a helpful customer support agent.
This is your first interaction with this user.
Be friendly and gather key information about their issue."""

    response = groq_client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user_message}
        ]
    )
    reply = response.choices[0].message.content

    # Save this exchange to memory
    save_memory(user_id, f"User: {user_message}\nAgent: {reply}")

    return reply

# ── Main loop ─────────────────────────────────────────────
def main():
    print("=== AI Customer Support Agent ===")
    print("Commands: 'quit' to exit | 'switch' to change user\n")

    user_id = input("Enter your user ID (e.g. 'yaswanth'): ").strip()
    print(f"\n[Logged in as: {user_id}]")
    print("Agent is ready. Describe your issue.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if user_input.lower() == "switch":
            user_id = input("Enter new user ID: ").strip()
            print(f"[Switched to: {user_id}]\n")
            continue

        print("\nAgent: ", end="", flush=True)
        reply = get_reply(user_id, user_message=user_input)
        print(reply)
        print()

if __name__ == "__main__":
    main()