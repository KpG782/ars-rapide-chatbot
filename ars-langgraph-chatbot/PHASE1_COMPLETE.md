# ARS Rapide Phase 1 — Quick Start Guide

## 🚀 You're Ready to Start Testing!

### Phase 1 Setup is Complete ✅

All files and folders have been created. Now you need to:

### Step 1: Install Dependencies

Open a terminal in the `ars-langgraph-chatbot` folder and run:

**Windows:**
```bash
cd "c:\Users\kpg78\Downloads\ARS\ARS_Lang\ars-langgraph-chatbot"
pip install -r requirements.txt
```

**Or use the setup script:**
```bash
cd "c:\Users\kpg78\Downloads\ARS\ARS_Lang\ars-langgraph-chatbot"
setup.bat
```

This will install:
- LangChain & LangGraph
- Google Generative AI
- ChromaDB
- Pydantic v2
- All other dependencies

**Installation takes 2-3 minutes.**

---

### Step 2: Set Up Your API Key

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Get your Google API key:
   - Visit: https://makersuite.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

3. Edit `.env` and replace:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   With your actual key:
   ```
   GOOGLE_API_KEY=AIzaSyC...your_actual_key_here
   ```

---

### Step 3: Test Phase 1

Run the application:

```bash
python app/main.py
```

**Expected Output:**

```
✓ Environment validated
✓ ARS Rapide Chatbot ready

============================================================
Phase 1 — Environment & Foundation: Complete
============================================================

Project structure created successfully!
Next steps:
  1. Copy .env.example to .env
  2. Add your GOOGLE_API_KEY to .env
  3. Run: pip install -r requirements.txt
  4. Ready for Phase 2 development

============================================================
```

If you see this, **Phase 1 is successful!** ✅

---

## 🔍 What We Built in Phase 1

### ✅ Project Structure
```
ars-langgraph-chatbot/
├── app/
│   ├── main.py                 # Entry point with env validation
│   ├── graph.py                # LangGraph state machine (skeleton)
│   ├── nodes/                  # Ready for Phase 2 nodes
│   ├── rag/                    # Ready for Phase 2 RAG
│   ├── knowledge_base/         # Ready for Phase 2 data
│   └── utils/
│       └── prompts.py          # All prompts centralized
├── tests/
│   └── test_diagnosis.py       # Ready for Phase 2 tests
├── .env.example                # Environment template
├── .gitignore                  # Configured for Python/AI projects
├── requirements.txt            # All dependencies pinned
├── README.md                   # Project documentation
└── setup.bat / setup.sh        # Automated setup scripts
```

### ✅ Core Components Created

1. **ChatState (app/graph.py)**
   - Pydantic model that holds conversation state
   - Flows through all graph nodes
   - Includes: symptoms, diagnosis, cost, booking, etc.

2. **Environment Validation (app/main.py)**
   - Checks for required API keys
   - Fails fast with clear error messages
   - Loads environment variables securely

3. **Prompt Templates (app/utils/prompts.py)**
   - All LLM prompts in one file
   - Ready for Phase 2: classification, diagnosis, cost, booking
   - Follows best practices (no inline prompts)

4. **Development Configuration**
   - `.cursorrules` for Cursor AI assistant
   - `.gitignore` prevents committing secrets
   - Type hints and docstrings throughout

---

## 🎯 What's Next — Phase 2

Phase 2 will add:
- Knowledge base JSON files (car problems, services, pricing)
- ChromaDB vector store setup
- RAG retrieval system
- Intent classifier node
- Diagnosis node with Gemini
- First working end-to-end diagnosis

**You can start Phase 2 development as soon as Phase 1 tests successfully!**

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'pydantic'"
**Solution:** Run `pip install -r requirements.txt`

### "Missing required environment variables: GOOGLE_API_KEY"
**Solution:** Create `.env` file and add your API key

### "pip is not recognized"
**Solution:** Make sure Python is installed and added to PATH

### "Permission denied" on setup.sh (Linux/Mac)
**Solution:** Run `chmod +x setup.sh` first

---

## ✅ Phase 1 Checklist

Before moving to Phase 2, verify:

- [ ] All folders created (app/, app/nodes/, app/rag/, etc.)
- [ ] Dependencies installed (`pip install -r requirements.txt` completed)
- [ ] `.env` file created with your GOOGLE_API_KEY
- [ ] `python app/main.py` runs without errors
- [ ] You see "ARS Rapide Chatbot ready" message

---

**Phase 1 Status:** ✅ Complete  
**Time to Phase 2:** Ready to start!

See [PROJECT_PROGRESS.md](../PROJECT_PROGRESS.md) for detailed phase tracking.
