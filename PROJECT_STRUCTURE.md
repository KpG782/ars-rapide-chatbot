# 📁 ARS Rapide Project Structure — Visual Guide

## Complete File Tree (Phase 1)

```
c:\Users\kpg78\Downloads\ARS\ARS_Lang\
│
├── 📄 START_HERE.md                    ← READ THIS FIRST! Quick start guide
├── 📄 PROJECT_PROGRESS.md              ← Master progress tracker
├── 📄 master.md                        ← Original master guide
├── 📄 spec.md                          ← Original technical spec
├── 📄 comparison.md                    ← Original tool comparison
│
└── 📁 ars-langgraph-chatbot/           ← YOUR PROJECT FOLDER
    │
    ├── 📄 README.md                    ← Project overview
    ├── 📄 PHASE1_COMPLETE.md           ← Phase 1 testing guide
    ├── 📄 requirements.txt             ← Python dependencies
    ├── 📄 .env.example                 ← Environment template
    ├── 📄 .gitignore                   ← Git ignore rules
    ├── 📄 .cursorrules                 ← Cursor AI rules
    ├── 📄 setup.bat                    ← Windows setup script
    ├── 📄 setup.sh                     ← Linux/Mac setup script
    │
    ├── 📁 app/                         ← Main application code
    │   ├── 📄 __init__.py
    │   ├── 📄 main.py                  ← Entry point (START HERE)
    │   ├── 📄 graph.py                 ← LangGraph state machine
    │   │
    │   ├── 📁 nodes/                   ← Graph nodes (Phase 2+)
    │   │   └── 📄 __init__.py
    │   │
    │   ├── 📁 rag/                     ← RAG components (Phase 2)
    │   │   └── 📄 __init__.py
    │   │
    │   ├── 📁 knowledge_base/          ← Car data JSON (Phase 2)
    │   │   (empty — ready for Phase 2)
    │   │
    │   └── 📁 utils/                   ← Utilities
    │       ├── 📄 __init__.py
    │       └── 📄 prompts.py           ← All LLM prompts
    │
    └── 📁 tests/                       ← Unit tests
        └── 📄 test_diagnosis.py        ← Test suite (Phase 2+)
```

---

## File Purposes — Quick Reference

| File | Purpose | When You Need It |
|------|---------|------------------|
| **START_HERE.md** | Quick start guide | Right now — to test Phase 1 |
| **PROJECT_PROGRESS.md** | Master tracker with all phases | Check progress daily |
| **PHASE1_COMPLETE.md** | Phase 1 testing instructions | Before moving to Phase 2 |
| **app/main.py** | Entry point | Every time you run the app |
| **app/graph.py** | State machine definition | Phase 2 when adding nodes |
| **app/utils/prompts.py** | All LLM prompts | Phase 2-4 when tuning AI responses |
| **requirements.txt** | Dependencies | Installation (pip install) |
| **.env.example** | Environment template | Creating your .env file |
| **.gitignore** | Git exclusions | Prevents committing secrets |
| **setup.bat** | Windows installer | Automated setup on Windows |

---

## What Gets Created After Setup

After running `pip install` and creating `.env`:

```
ars-langgraph-chatbot/
├── .env                        ← YOUR API KEYS (not in git)
├── venv/                       ← Python virtual env (optional)
└── chroma_db/                  ← ChromaDB storage (Phase 2)
```

---

## Phase 2 Will Add

```
app/
├── nodes/
│   ├── classifier.py           ← Intent classification
│   ├── diagnosis.py            ← Car problem diagnosis
│   └── (more in Phase 3-4)
│
├── rag/
│   ├── vector_store.py         ← ChromaDB setup
│   └── retriever.py            ← Semantic search
│
└── knowledge_base/
    ├── car_problems.json       ← Car issue database
    ├── services.json           ← Available services
    └── pricing.json            ← Metro Manila pricing
```

---

## Code Flow (Phase 1 Complete)

```
1. python app/main.py
   ↓
2. Load .env variables
   ↓
3. Validate GOOGLE_API_KEY exists
   ↓
4. Build LangGraph skeleton
   ↓
5. Print "ARS Rapide Chatbot ready"
```

---

## Code Flow (Phase 2 Target)

```
User Input
   ↓
1. Classify Intent (diagnose/cost/book/general)
   ↓
2. Retrieve relevant docs from ChromaDB
   ↓
3. Gemini diagnoses using retrieved context
   ↓
4. Return diagnosis + urgency + response
```

---

## Important Files You'll Edit Most

### During Development:
1. `app/graph.py` — Add nodes and edges
2. `app/utils/prompts.py` — Tune AI prompts
3. `app/knowledge_base/*.json` — Add car knowledge
4. `tests/test_diagnosis.py` — Add tests

### During Configuration:
1. `.env` — API keys and settings
2. `requirements.txt` — If adding packages

### Never Edit:
- `__pycache__/` — Auto-generated
- `chroma_db/` — Auto-generated
- `.env` — (Don't commit this!)

---

## Terminal Commands You'll Use

```bash
# Phase 1 — Setup
cd "c:\Users\kpg78\Downloads\ARS\ARS_Lang\ars-langgraph-chatbot"
pip install -r requirements.txt
copy .env.example .env
python app/main.py

# Phase 2+ — Development
python app/main.py                      # Run app
python -m pytest tests/ -v              # Run tests
python -c "import langchain; print('OK')"  # Check imports

# Debugging
python app/main.py --verbose            # (Future: add verbose flag)
python -m pdb app/main.py               # Python debugger
```

---

## 🎯 Current Status

| Component | Status | Location |
|-----------|--------|----------|
| **Project Structure** | ✅ Complete | All folders created |
| **Configuration Files** | ✅ Complete | .env.example, requirements.txt, .gitignore |
| **State Model** | ✅ Complete | app/graph.py (ChatState) |
| **Entry Point** | ✅ Complete | app/main.py |
| **Prompt Templates** | ✅ Complete | app/utils/prompts.py |
| **Test Framework** | ✅ Complete | tests/test_diagnosis.py |
| **Dependencies** | ⏳ Need install | Run: pip install -r requirements.txt |
| **API Key** | ⏳ Need setup | Create .env with GOOGLE_API_KEY |
| **Knowledge Base** | ⬜ Phase 2 | Will add car_problems.json |
| **RAG System** | ⬜ Phase 2 | Will add vector_store.py |
| **Diagnosis Logic** | ⬜ Phase 2 | Will add nodes/diagnosis.py |

---

## 🚀 What to Do Right Now

### Step 1: Install (2-3 minutes)
```bash
cd "c:\Users\kpg78\Downloads\ARS\ARS_Lang\ars-langgraph-chatbot"
pip install -r requirements.txt
```

### Step 2: Configure (1 minute)
```bash
copy .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Step 3: Test (30 seconds)
```bash
python app/main.py
```

### Expected Result:
```
✓ Environment validated
✓ ARS Rapide Chatbot ready
============================================================
Phase 1 — Environment & Foundation: Complete
============================================================
```

---

**If you see this message, Phase 1 is successful and you're ready for Phase 2!** 🎉

See [START_HERE.md](../START_HERE.md) for detailed instructions.
