# ✅ PHASE 1 TESTING CHECKLIST

Use this checklist to verify Phase 1 is working before starting Phase 2.

---

## 📋 Pre-Testing Checklist

### 1. File Verification

Open Windows Explorer and navigate to:  
`c:\Users\kpg78\Downloads\ARS\ARS_Lang\ars-langgraph-chatbot`

Verify these files exist:

- [ ] `README.md`
- [ ] `PHASE1_COMPLETE.md`
- [ ] `requirements.txt`
- [ ] `.env.example`
- [ ] `.gitignore`
- [ ] `.cursorrules`
- [ ] `setup.bat`
- [ ] `setup.sh`

### 2. Folder Verification

Verify these folders exist:

- [ ] `app/`
- [ ] `app/nodes/`
- [ ] `app/rag/`
- [ ] `app/knowledge_base/`
- [ ] `app/utils/`
- [ ] `tests/`

### 3. Code Files Verification

Verify these Python files exist:

- [ ] `app/main.py`
- [ ] `app/graph.py`
- [ ] `app/utils/prompts.py`
- [ ] `app/__init__.py`
- [ ] `app/nodes/__init__.py`
- [ ] `app/rag/__init__.py`
- [ ] `app/utils/__init__.py`
- [ ] `tests/test_diagnosis.py`

---

## 🚀 Installation Test

### Step 1: Open Terminal

Open Command Prompt or PowerShell in Windows.

Navigate to project:
```bash
cd "c:\Users\kpg78\Downloads\ARS\ARS_Lang\ars-langgraph-chatbot"
```

- [ ] Terminal is in correct directory
- [ ] Can see project files with `dir` command

### Step 2: Check Python

```bash
python --version
```

**Expected:** `Python 3.10.x` or higher

- [ ] Python version is 3.10 or higher
- [ ] Python command works

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected:** Installation completes without errors  
**Time:** 2-3 minutes

- [ ] Installation started
- [ ] No error messages
- [ ] Installation completed successfully
- [ ] See messages like "Successfully installed langchain-0.2.16 ..." etc.

---

## 🔑 Environment Configuration Test

### Step 1: Create .env File

```bash
copy .env.example .env
```

- [ ] `.env` file created
- [ ] Can open `.env` in text editor

### Step 2: Get API Key

Visit: https://makersuite.google.com/app/apikey

- [ ] Created/logged into Google account
- [ ] Generated API key
- [ ] Copied API key to clipboard

### Step 3: Edit .env

Open `.env` in Notepad/VS Code/Cursor

Replace:
```
GOOGLE_API_KEY=your_google_api_key_here
```

With:
```
GOOGLE_API_KEY=AIzaSyC_your_actual_key_here
```

- [ ] Opened .env file
- [ ] Pasted actual API key
- [ ] Saved file

---

## ✅ Application Test

### Step 1: Run Main Application

```bash
python app/main.py
```

### Expected Output:

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

### Verification:

- [ ] Script runs without errors
- [ ] See "✓ Environment validated"
- [ ] See "✓ ARS Rapide Chatbot ready"
- [ ] See "Phase 1 — Environment & Foundation: Complete"
- [ ] No Python errors or tracebacks

---

## 🧪 Import Test

Verify all dependencies are correctly installed:

```bash
python -c "import langchain; print('✓ LangChain OK')"
```

```bash
python -c "import langgraph; print('✓ LangGraph OK')"
```

```bash
python -c "import langchain_google_genai; print('✓ Google GenAI OK')"
```

```bash
python -c "import chromadb; print('✓ ChromaDB OK')"
```

```bash
python -c "import pydantic; print('✓ Pydantic OK')"
```

### Verification:

- [ ] LangChain imports successfully
- [ ] LangGraph imports successfully
- [ ] Google GenAI imports successfully
- [ ] ChromaDB imports successfully
- [ ] Pydantic imports successfully
- [ ] No import errors

---

## 🎯 Code Quality Test

### Test 1: ChatState Model

Open `app/graph.py` and verify:

- [ ] ChatState class exists
- [ ] Has all expected fields (user_message, symptoms, diagnosis, etc.)
- [ ] Uses Pydantic BaseModel
- [ ] No syntax errors

### Test 2: Environment Validation

Open `app/main.py` and verify:

- [ ] validate_environment() function exists
- [ ] Checks for GOOGLE_API_KEY
- [ ] Provides helpful error messages
- [ ] No syntax errors

### Test 3: Prompt Templates

Open `app/utils/prompts.py` and verify:

- [ ] Multiple prompt templates defined
- [ ] Uses ChatPromptTemplate from langchain
- [ ] Prompts include system and human messages
- [ ] No syntax errors

---

## 🐛 Troubleshooting Checklist

If something fails, check these:

### "ModuleNotFoundError: No module named 'pydantic'"

- [ ] Did you run `pip install -r requirements.txt`?
- [ ] Are you in the correct directory?
- [ ] Try: `pip list` to see installed packages

### "Missing required environment variables: GOOGLE_API_KEY"

- [ ] Does `.env` file exist?
- [ ] Did you copy from `.env.example`?
- [ ] Did you add your actual API key?
- [ ] Is the key on the correct line (GOOGLE_API_KEY=...)?

### "python is not recognized"

- [ ] Is Python installed? Download from python.org
- [ ] Is Python in your PATH?
- [ ] Try: `py --version` instead of `python --version`

### "Permission denied" (on Linux/Mac)

- [ ] Did you run `chmod +x setup.sh`?
- [ ] Try running with sudo: `sudo bash setup.sh`

### Dependencies fail to install

- [ ] Try upgrading pip: `python -m pip install --upgrade pip`
- [ ] Try with explicit python: `python -m pip install -r requirements.txt`
- [ ] Check internet connection

---

## ✅ FINAL VERIFICATION

All checks must pass before Phase 2:

### Structure
- [ ] All folders created
- [ ] All files created
- [ ] Project structure matches spec

### Installation
- [ ] Python 3.10+ installed
- [ ] Dependencies installed
- [ ] No installation errors

### Configuration
- [ ] .env file created
- [ ] GOOGLE_API_KEY added
- [ ] API key is valid (not expired)

### Testing
- [ ] `python app/main.py` runs successfully
- [ ] See success messages
- [ ] No Python errors
- [ ] All imports work

### Documentation
- [ ] Read START_HERE.md
- [ ] Read PHASE1_COMPLETE.md
- [ ] Understand PROJECT_PROGRESS.md
- [ ] Know what Phase 2 will build

---

## 🎉 SUCCESS CRITERIA

**Phase 1 is complete when:**

1. ✅ You run `python app/main.py`
2. ✅ You see "ARS Rapide Chatbot ready"
3. ✅ No errors appear
4. ✅ All imports work
5. ✅ You understand the project structure

---

## 📝 Post-Test Notes

### Working? Write down:
- Date/time completed: ________________
- Python version: ________________
- Any warnings (if any): ________________

### Issues? Write down:
- What failed: ________________
- Error message: ________________
- What you tried: ________________

---

## 🚀 NEXT STEPS

If all checks pass:

1. ✅ Mark Phase 1 as complete
2. 📖 Review Phase 2 plan in PROJECT_PROGRESS.md
3. 🛠️ Start Phase 2: Knowledge base + RAG implementation
4. 🔄 Keep checking PROJECT_PROGRESS.md for updates

**Phase 2 Preview:**
- Create car_problems.json with 10+ car issues
- Set up ChromaDB vector store
- Implement semantic search retriever
- Build intent classifier node
- Build diagnosis node with Gemini
- Test end-to-end diagnosis flow

---

**Ready to move forward?** Check off all items above, then start Phase 2! 🚀
