# AI Customer Support Agent with Persistent Memory

An AI-powered customer support agent that remembers users across sessions using [Hindsight](https://github.com/vectorize-io/hindsight) memory.

## What it does
- Remembers every user's past issues across sessions
- No more repeating yourself — the agent already knows your history
- Powered by Groq (free, fast LLM) + Hindsight (persistent memory)

## Demo
**Session 1:** User reports order #1234 is delayed  
**Session 2:** User says "Hi I'm back" → Agent immediately recalls the order issue by name

## Setup

1. Clone the repo
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Create a `.env` file:

GROQ_API_KEY=your_groq_key

HINDSIGHT_API_KEY=your_hindsight_key

HINDSIGHT_BANK_ID=your_bank_id
4. Run:
```bash
   python agent.py
```

## Tech Stack
- [Groq](https://groq.com) — fast, free LLM API
- [Hindsight](https://hindsight.vectorize.io) — persistent agent memory
- Python
