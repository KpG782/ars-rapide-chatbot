# ARS Rapide LangGraph Chatbot — AI Coding Assistant Guide

**For: Ken | Junior AI/ML Engineer**
**Last Updated: February 2026**
**Purpose: Paste this into Cursor / Windsurf / ChatGPT Codex before you start coding. Follow the rules. Don't skip.**

---

## PART 1: MASTER SYSTEM PROMPT

> **How to use this:** Copy the entire block below and paste it into your AI coding assistant's system prompt or "rules" section (Cursor → Settings → Rules, or .cursorrules file). This tells your AI helper exactly what the project is, what stack to use, and how to behave.

---

```
You are a senior AI/ML engineer helping build the ARS Rapide auto-repair chatbot for the Philippine market.

PROJECT CONTEXT:
- Name: ARS Rapide Chatbot
- Purpose: Car problem diagnosis, cost estimation, and service booking
- Target market: Philippines (Metro Manila)
- Language: Filipino-English (Taglish) with natural code-switching
- Competition entry: Must demonstrate agentic AI architecture

TECH STACK (do not suggest alternatives):
- Python 3.10
- LangChain (orchestration and chains)
- LangGraph (agentic graph-based flow control)
- Google Gemini API (LLM backbone)
- ChromaDB (vector database for RAG)
- Pydantic v2 (data validation and state models)
- python-dotenv (environment variables)

RULES YOU MUST FOLLOW:
1. Never suggest Rasa, Dialogflow, or any other chatbot framework. We chose LangGraph deliberately.
2. Never use async unless I specifically ask for it. Keep it synchronous and readable.
3. Always use Pydantic v2 BaseModel for any data structure. No raw dicts.
4. Every function must have type hints. No exceptions.
5. Write docstrings on every function. One-liner is fine, but it must exist.
6. Never hardcode API keys. Always use os.getenv() or dotenv.
7. Keep each file under 150 lines. If it goes over, split it.
8. Do not over-engineer. If a simple solution works, use it.
9. When writing prompts for Gemini, put them in app/utils/prompts.py. Never inline them.
10. If I ask you to add a feature, show me the minimal code change needed. Do not rewrite the whole file.
11. Always show the exact file path before any code block.
12. If something could break in production, warn me. Don't just silently do it.
13. Test assumptions out loud. If you're unsure about something, say so. Don't guess.

PROJECT STRUCTURE (stick to this exactly):
ars-langgraph-chatbot/
├── .env
├── requirements.txt
├── app/
│   ├── main.py
│   ├── graph.py
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── classifier.py
│   │   ├── diagnosis.py
│   │   ├── cost_estimator.py
│   │   ├── booking.py
│   │   └── taglish.py
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   ├── knowledge_base/
│   │   ├── car_problems.json
│   │   ├── services.json
│   │   └── pricing.json
│   └── utils/
│       ├── __init__.py
│       └── prompts.py
└── tests/
    └── test_diagnosis.py

WHEN I ASK YOU TO WRITE CODE:
- Show the full file if it's new.
- Show only the changed function if it's an edit.
- Always include the imports at the top.
- Tell me if I need to run any install commands.
- If it connects to an API, tell me what env variable it needs.
```

---

## PART 2: .CURSORRULES FILE

> **How to use this:** If you use Cursor, create a file called `.cursorrules` in the root of your project folder and paste this content inside. Cursor automatically reads it.

---

```
# ARS Rapide Chatbot — Cursor Rules

# Python version
python_version = "3.10"

# Never suggest these
deny_packages = ["rasa", "rasa-sdk", "dialogflow", "botpress"]

# Code style
- Use type hints on every function signature
- Use Pydantic v2 BaseModel for all data classes
- Max 150 lines per file
- Docstrings on every function (one-liner is okay)
- No inline API keys ever
- All LLM prompts go in app/utils/prompts.py
- Imports at the top, grouped: stdlib → third-party → local

# When editing
- Show only the minimal diff needed
- Confirm file path before code
- Warn about anything that could break

# Naming conventions
- Files: snake_case
- Classes: PascalCase
- Functions: snake_case
- Constants: UPPER_CASE
- Pydantic models: PascalCase (e.g., ChatState, DiagnosisResult)
```

---

## PART 3: WHAT TO DO AND WHAT NOT TO DO

> **Read this before you write a single line of code.** These are the mistakes that waste the most time. Learn them now, not after 3 hours of debugging.

---

### DO

**Do use Pydantic for everything that holds data.**

```python
# app/graph.py
from pydantic import BaseModel
from typing import List, Optional

class ChatState(BaseModel):
    user_message: str = ""
    symptoms: List[str] = []
    diagnosis: Optional[str] = None
    urgency_level: Optional[str] = None
    response: str = ""
```

Why: LangGraph expects Pydantic models for state. It also catches bugs early — if you pass the wrong type, it fails immediately instead of silently breaking later.

---

**Do put all prompts in one place.**

```python
# app/utils/prompts.py — ALL prompts live here, nowhere else

CLASSIFICATION_PROMPT = """You are classifying a user's intent..."""

DIAGNOSIS_PROMPT = """You are an expert mechanic AI..."""

COST_ESTIMATION_PROMPT = """Given this diagnosis, estimate the cost..."""
```

Why: When you need to tune a prompt (and you will, many times), you don't want to hunt through 10 files. One file, easy to find, easy to change.

---

**Do validate your .env file before the app starts.**

```python
# app/main.py — top of the file, before anything else runs
import os
from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = ["GOOGLE_API_KEY"]

for var in REQUIRED_VARS:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing required env variable: {var}")
```

Why: Nothing is more frustrating than an app that crashes 30 seconds in because an API key is missing. Fail fast, fail loud.

---

**Do test each node independently before connecting them.**

```python
# tests/test_diagnosis.py
from app.nodes.diagnosis import diagnose_problem
from app.graph import ChatState

def test_dead_battery_diagnosis():
    state = ChatState(
        user_message="car won't start, no lights",
        symptoms=["won't start", "no dashboard lights"]
    )
    result = diagnose_problem(state)
    assert result.diagnosis is not None
    assert result.urgency_level in ["EMERGENCY", "DON'T DRIVE", "DRIVE CAREFULLY", "CAN DRIVE"]
```

Why: If you only test the full graph end-to-end, you won't know which node broke. Test nodes alone first.

---

**Do keep your knowledge base in clean JSON.**

```json
// knowledge_base/car_problems.json
[
  {
    "id": "dead_battery",
    "category": "electrical",
    "symptoms": ["won't start", "no lights", "silent when turning key", "clicking sound"],
    "diagnosis": "Dead or weak battery. May need jump-start or replacement.",
    "urgency": "DON'T DRIVE",
    "taglish_symptoms": ["hindi gumagana", "walang ilaw", "tahimik lang"]
  }
]
```

Why: This is what gets loaded into ChromaDB. Clean structured JSON = better vector embeddings = better retrieval = better diagnosis.

---

### DO NOT

**Do not use async unless you absolutely need it.**

```python
# BAD for this project right now
async def diagnose_problem(state: ChatState) -> ChatState:
    result = await llm.ainvoke(prompt)

# GOOD — simple, readable, debuggable
def diagnose_problem(state: ChatState) -> ChatState:
    result = llm.invoke(prompt)
```

Why: Async adds complexity with no benefit when you're making single sequential API calls. You're not handling 1000 users simultaneously. Keep it simple.

---

**Do not hardcode anything.**

```python
# BAD
api_key = "AIza..."
model_name = "gemini-1.5-pro"
top_k = 3

# GOOD
import os
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")  # default fallback is fine
TOP_K = int(os.getenv("RETRIEVER_TOP_K", "3"))
```

---

**Do not build the booking system first.**

The diagnosis engine is the brain of this project. That's what judges will evaluate. Build that first, make it work well, then add booking as a secondary feature.

Priority order: Diagnosis → Cost Estimation → Taglish → Booking → Polish.

---

**Do not over-engineer the Taglish handling.**

```python
# BAD — don't build a translation model, don't use a separate API
# GOOD — a simple dictionary + include Taglish awareness in your prompts

TAGLISH_TERMS = {
    "kumakatok": "knocking engine sound",
    "umiinit": "overheating",
    "mahina ang preno": "weak brakes",
    "hindi gumagana": "not working",
    "nag-check engine": "check engine light on",
}
```

A dictionary of 30-50 common terms + telling Gemini to understand Taglish in the system prompt will handle 90% of cases. Don't waste a week on the other 10%.

---

**Do not forget to .gitignore these.**

```
# .gitignore — create this immediately
.env
venv/
chroma_db/
__pycache__/
*.pyc
models/
.DS_Store
```

If you push your API key to GitHub, you'll have to rotate it and deal with that mess. Don't.

---

## PART 4: WHY WE MADE THESE DECISIONS

> **This is the "architecture decision log."** When someone (a judge, a teammate, or future you) asks "why did you do it this way," this is your answer.

---

| Decision | Why | What we didn't do and why not |
|---|---|---|
| LangGraph over Rasa | LangGraph gives us agentic reasoning — the LLM decides what to do next. Rasa forces scripted intent flows. | Rasa is rigid. Adding a new symptom path means retraining. |
| Gemini over GPT-4 | Google provides Gemini free tier with generous limits. We're in the Philippines — lower latency to Google servers in the region. | GPT-4 costs more and has higher latency from PH. |
| ChromaDB over Pinecone/Weaviate | ChromaDB runs locally. No extra cloud service to manage, no extra cost, no network dependency during demos. | Pinecone is cloud-only. Overkill for this dataset size. |
| Pydantic v2 for state | LangGraph requires typed state. Pydantic catches type errors at runtime immediately. | Raw dicts are error-prone and hard to debug. |
| Single-threaded / synchronous | Easier to debug, easier to understand, sufficient for demo and competition scale. | Async adds complexity with zero benefit at this scale. |
| JSON knowledge base | Simple, version-controllable, easy to edit without code changes. Loads directly into ChromaDB. | SQL database is overkill for ~50-100 car problems. |
| Taglish via dictionary + prompt | Handles common cases with zero extra compute. Gemini already understands Filipino context. | Training a separate NLP model for Filipino is massive overkill. |

---

## PART 5: BUILD ORDER (THE EXACT SEQUENCE)

> **Do these in order. Do not skip. Do not jump ahead. Each step builds on the last.**

---

### Day 1 — Get the skeleton running

```
Step 1: Create the project folder structure (exactly as shown above)
Step 2: Create requirements.txt and install dependencies
Step 3: Create .env with your GOOGLE_API_KEY
Step 4: Create .gitignore
Step 5: Write app/graph.py with ChatState and an empty graph (no nodes yet)
Step 6: Write app/main.py that loads .env and prints "ARS Chatbot ready"
Step 7: Run it. Make sure it starts without errors.
```

Stop here for Day 1. Seriously. A clean skeleton that runs is worth more than half-finished features.

---

### Day 2 — First working diagnosis

```
Step 1: Write app/knowledge_base/car_problems.json (start with 10 problems)
Step 2: Write app/rag/vector_store.py — loads the JSON into ChromaDB
Step 3: Write app/rag/retriever.py — retrieves top 3 relevant docs
Step 4: Write app/utils/prompts.py — CLASSIFICATION_PROMPT and DIAGNOSIS_PROMPT
Step 5: Write app/nodes/classifier.py — classifies user intent using Gemini
Step 6: Wire classifier into the graph in graph.py
Step 7: Test: type a car problem, see it classified. Does it work?
Step 8: Write app/nodes/diagnosis.py — uses RAG retriever + Gemini to diagnose
Step 9: Wire diagnosis into the graph with a conditional edge from classifier
Step 10: Test: type "my car won't start". See if it diagnoses correctly.
```

This is your MVP. A user types a problem, the system retrieves relevant knowledge, and Gemini diagnoses it. This is what you demo if you run out of time.

---

### Day 3 — Cost estimation + Taglish

```
Step 1: Write app/knowledge_base/pricing.json (Metro Manila 2024 rates)
Step 2: Write app/nodes/cost_estimator.py — takes diagnosis, returns price range
Step 3: Wire cost estimator after diagnosis in the graph
Step 4: Write app/nodes/taglish.py — the dictionary normalizer
Step 5: Add Taglish awareness to your prompts in prompts.py
Step 6: Test with Taglish inputs: "kumakatok ang engine ko"
Step 7: Add urgency classification to diagnosis output
Step 8: Test the full flow: symptom → diagnosis → urgency → cost
```

---

### Day 4 — Booking + Polish

```
Step 1: Write app/knowledge_base/services.json
Step 2: Write app/nodes/booking.py — collects service type, date, car details
Step 3: Wire booking as an optional path after cost estimation
Step 4: Add conversation history to ChatState so context persists across turns
Step 5: Write 5 test cases in tests/test_diagnosis.py
Step 6: Run all tests. Fix anything that breaks.
Step 7: Do a full end-to-end walkthrough pretending you're a user.
Step 8: Clean up any dead code. Make sure .env is not committed.
```

---

### Competition Day — What to demo

Show this exact flow, in this order:

1. "My car is making a knocking sound" → diagnosis → cost estimate
2. "Kumakatok ang engine ko" → same flow but in Taglish (this impresses judges)
3. "My brakes are squeaking and the car vibrates" → multi-symptom diagnosis (this shows the AI reasoning)
4. Ask to book a service → show the booking flow

That's it. Four demos. Clean, clear, impressive. Don't try to show everything. Show the best four things.

---

## PART 6: QUICK REFERENCE CARD

> **Pin this somewhere visible while you code.**

---

```
STACK:          Python 3.10 | LangChain | LangGraph | Gemini | ChromaDB
STATE:          Always Pydantic BaseModel
PROMPTS:        Always in app/utils/prompts.py
API KEYS:       Always in .env, always os.getenv()
FILE LENGTH:    Max 150 lines. Split if over.
ASYNC:          No. Keep it sync.
TEST FIRST:     Each node alone, then the full graph.
BUILD ORDER:    Diagnosis → Cost → Taglish → Booking → Polish
DEMO ORDER:     English symptom → Taglish symptom → Multi-symptom → Booking
```

---

*Written from a senior AI/ML engineering perspective. The goal is not to make this impressive-looking. The goal is to make it actually work, be maintainable, and win. Those are not the same thing.*