# 📌 ARS RAPIDE — QUICK REFERENCE CARD

**Keep this open while coding!**

---

## 🚀 QUICK START (3 Steps)

```bash
# 1. Install
cd "c:\Users\kpg78\Downloads\ARS\ARS_Lang\ars-langgraph-chatbot"
pip install -r requirements.txt

# 2. Configure
copy .env.example .env
# Edit .env, add GOOGLE_API_KEY

# 3. Run
python app/main.py
```

---

## 📂 WHERE IS EVERYTHING?

| What | Where |
|------|-------|
| **Entry point** | `app/main.py` |
| **State model** | `app/graph.py` → ChatState |
| **All prompts** | `app/utils/prompts.py` |
| **Tests** | `tests/test_diagnosis.py` |
| **Knowledge base** | `app/knowledge_base/*.json` |
| **RAG code** | `app/rag/` |
| **Graph nodes** | `app/nodes/` |

---

## 🎯 PHASE STATUS

| Phase | Status | What It Does |
|-------|--------|--------------|
| **1** | ✅ DONE | Foundation & structure |
| **2** | ⏳ NEXT | RAG + Diagnosis brain |
| **3** | ⬜ TODO | Cost + Taglish |
| **4** | ⬜ TODO | Booking + Polish |

---

## 🔑 KEY FILES TO KNOW

```
app/
├── main.py           ← Start here every time
├── graph.py          ← ChatState + LangGraph setup
├── utils/
│   └── prompts.py    ← ALL prompts (edit often)
├── nodes/
│   ├── classifier.py ← Intent classification
│   └── diagnosis.py  ← Main diagnosis logic
└── rag/
    ├── vector_store.py  ← ChromaDB setup
    └── retriever.py     ← Semantic search
```

---

## 🛠️ RULES TO REMEMBER

1. **Never hardcode** — Use `.env` for everything
2. **All prompts in one place** — `app/utils/prompts.py`
3. **Type hints everywhere** — No raw dicts, use Pydantic
4. **Max 150 lines per file** — Split if longer
5. **No async** — Keep it simple and synchronous
6. **Test nodes individually** — Before connecting to graph

---

## 📚 DOCUMENTATION

| File | Purpose |
|------|---------|
| **START_HERE.md** | Quick start (read first) |
| **PROJECT_PROGRESS.md** | Master tracker (check daily) |
| **TESTING_CHECKLIST.md** | Phase 1 verification |
| **PROJECT_STRUCTURE.md** | Visual file tree |
| **PHASE1_COMPLETE.md** | Phase 1 details |

---

## 💻 TERMINAL COMMANDS

```bash
# Run app
python app/main.py

# Run tests
python -m pytest tests/ -v

# Test imports
python -c "import langchain; print('OK')"

# Check Python
python --version

# List packages
pip list | grep lang
```

---

## 🧠 CHATSTATE FIELDS

```python
class ChatState(BaseModel):
    user_message: str              # What user said
    conversation_history: List     # Past messages
    intent: Optional[str]          # diagnose|cost|book|general
    symptoms: List[str]            # Collected symptoms
    car_details: Dict              # make, model, year
    diagnosis: Optional[str]       # The diagnosis
    urgency_level: Optional[str]   # EMERGENCY|DON'T DRIVE|...
    cost_estimate: Optional[Dict]  # Price info
    booking_info: Optional[Dict]   # Booking details
    response: str                  # Final response
```

---

## 🎨 URGENCY LEVELS

| Level | Meaning | Example |
|-------|---------|---------|
| **EMERGENCY** | Danger | Brake failure |
| **DON'T DRIVE** | Unsafe | Engine overheating |
| **DRIVE CAREFULLY** | Risky | Worn brake pads |
| **CAN DRIVE** | Safe | Minor noise |

---

## 🌐 ENVIRONMENT VARIABLES

```bash
# Required
GOOGLE_API_KEY=AIzaSyC...        # Get at: makersuite.google.com

# Optional
GEMINI_MODEL=gemini-1.5-pro      # LLM model
EMBEDDING_MODEL=models/embedding-001
RETRIEVER_TOP_K=3                # How many docs to retrieve
CHROMA_DB_PATH=./chroma_db       # Vector store location
```

---

## 🔗 USEFUL LINKS

- **Google API Key:** https://makersuite.google.com/app/apikey
- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/
- **LangChain Docs:** https://python.langchain.com/docs/
- **Gemini Docs:** https://ai.google.dev/docs
- **ChromaDB Docs:** https://docs.trychroma.com/

---

## 🐛 QUICK TROUBLESHOOTING

| Error | Fix |
|-------|-----|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| Missing API key | Create `.env` with `GOOGLE_API_KEY=...` |
| Import error | Check Python version (need 3.10+) |
| pip not found | Use `python -m pip install ...` |

---

## 📊 TECH STACK

```
Python 3.10+
├── LangChain 0.2.16      (orchestration)
├── LangGraph 0.2.20      (agentic graph)
├── Google Gemini 1.5     (LLM inference)
├── ChromaDB 0.4.24       (vector store)
└── Pydantic 2.9.2        (data validation)
```

---

## 🎯 COMPETITION DEMO (4 parts)

1. **English diagnosis** → "My car won't start"
2. **Taglish input** → "Kumakatok ang engine ko"
3. **Multi-symptom** → "Brakes squeaking + vibrating"
4. **Booking flow** → Full appointment scheduling

**Time:** 5-7 minutes total

---

## ✅ BEFORE PHASE 2

- [ ] Phase 1 tested successfully
- [ ] `python app/main.py` works
- [ ] All dependencies installed
- [ ] `.env` configured
- [ ] Understand ChatState
- [ ] Read phase 2 plan

---

## 📝 QUICK NOTES SPACE

Write down your API key prefix (first 10 chars):
```
AIzaSyC_______________
```

Current Python version:
```
_______________
```

Date Phase 1 completed:
```
_______________
```

---

**Print this and keep it visible while coding!** 📌
