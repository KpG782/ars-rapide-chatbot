# 🚀 Quick Start — Phase 2 Testing Guide

## What Phase 2 Delivers

A **fully functional car diagnostic AI** that:
- Takes user symptoms (in English or Taglish)
- Uses semantic search to find relevant car problems
- Generates accurate diagnosis using Google Gemini
- Provides urgency levels (EMERGENCY, DON'T DRIVE, etc.)

---

## ⚡ 5-Minute Test

### 1. Install Dependencies (First Time Only)

```bash
cd ars-langgraph-chatbot
python -m pip install sentence-transformers scikit-learn
```

These are the RAG dependencies using:
- **Sentence-Transformers** for semantic embeddings
- **Scikit-learn** for vector similarity

*Installation takes ~2 minutes.*

---

### 2. Verify Environment

Make sure you have a `.env` file with:
```
GOOGLE_API_KEY=your_key_here
```

---

### 3. Run Interactive Mode

```bash
python app/main.py
```

You'll see:
```
Phase 2 — RAG & Diagnosis: Interactive Mode
============================================================

Describe your car problem and get instant diagnosis!
Type 'quit' or 'exit' to stop.

You: _
```

---

## 🧪 Test Cases to Try

### Test Case 1: Dead Battery (English)
```
You: my car won't start, lights are dim, clicking sound

Expected Result:
✓ Classified intent: DIAGNOSIS
✓ Retrieved 3 relevant problems
✓ Diagnosis: Dead battery with urgency DON'T DRIVE
```

### Test Case 2: Engine Overheating (Taglish)
```
You: umiinit ang engine ko, may usok sa hood

Expected Result:
✓ Taglish symptoms recognized
✓ Diagnosis: Engine overheating
✓ Urgency: EMERGENCY
```

### Test Case 3: Brake Problems (English)
```
You: brakes making squeaking sound when I stop

Expected Result:
✓ Diagnosis: Worn brake pads
✓ Urgency: DRIVE CAREFULLY or DON'T DRIVE
```

### Test Case 4: Engine Knocking (Taglish)
```
You: kumakatok ang engine, malakas ang ingay

Expected Result:
✓ Diagnosis: Engine knocking issue
✓ Explanation in natural Taglish
✓ Urgency: DRIVE CAREFULLY
```

---

## 🔍 Behind-the-Scenes Testing

Want to see how the RAG system works?

### Test Vector Store
```bash
python -m app.rag.vector_store
```

**What you'll see:**
- Loading of 25 car problems
- Embedding generation (2 seconds)
- Test queries with similarity scores
- Top matches for each query

**Expected Output:**
```
Query: 'my car won't start and the lights are dim'
→ Dead or Weak Battery (63.8% match)
→ Starter Motor Not Working (56.1% match)
→ Alternator Failure (39.2% match)
```

---

### Test Retriever
```bash
python -m app.rag.retriever
```

**What you'll see:**
- How search results get formatted for the LLM
- Full diagnostic context including symptoms, causes, urgency

**Expected Output:**
```
Problem 1 (Relevance: 63.83%):
Category: electrical
Issue: Dead or Weak Battery
Diagnosis: Dead or discharged battery...
Symptoms: car won't start, no lights, clicking...
Taglish Symptoms: hindi gumagana, walang ilaw...
```

---

### Test Diagnosis Node
```bash
python -m app.nodes.diagnosis
```

**What you'll see:**
- 3 pre-loaded test cases
- RAG retrieval + Gemini diagnosis
- Urgency level extraction

**Expected Output:**
```
Symptoms: 'engine temperature gauge is in the red zone...'
→ Diagnosis with urgency: EMERGENCY
```

---

## ✅ Success Criteria

Phase 2 is working correctly if:

- [x] Vector store loads 25 problems without errors
- [x] Semantic search returns relevant matches (50%+ similarity)
- [x] Interactive mode responds to user input
- [x] Diagnosis includes urgency level
- [x] Taglish input is understood and processed
- [x] English input works equally well
- [x] Responses are natural (not robotic)

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: sentence_transformers"
**Solution:**
```bash
python -m pip install sentence-transformers scikit-learn
```

### "Missing required environment variables: GOOGLE_API_KEY"
**Solution:**
Check your `.env` file has:
```
GOOGLE_API_KEY=AIza...your_key_here
```

### Model downloads on first run (normal)
First run downloads `all-MiniLM-L6-v2` model (~80MB).  
This only happens once. Cached for future runs.

### Slow first query (normal)
First query loads the model into memory (~2 seconds).  
Subsequent queries are fast (<50ms).

---

## 📊 What to Show in Your Demo

### Demo Flow (Recommended Order)

**1. Dead Battery (English) — 30 seconds**
```
You: my car won't start, lights don't turn on, clicking sound
→ Shows: Basic diagnosis works
```

**2. Overheating (Taglish) — 30 seconds**
```
You: umiinit ang kotse ko, may usok sa hood
→ Shows: Taglish understanding + EMERGENCY urgency
```

**3. Multi-Symptom (English) — 30 seconds**
```
You: brakes squeaking, car vibrates, takes long to stop
→ Shows: Multi-symptom reasoning
```

**4. Explain RAG (Behind the scenes) — 1 minute**
- Show `python -m app.rag.vector_store` output
- Explain: "The system searches 25 car problems semantically"
- Show similarity scores

**Total demo time: 3-4 minutes**

---

## 🎯 Key Talking Points for Judges

1. **Semantic Search (not keyword matching)**
   - User says "hindi gumagana" → finds "car won't start"
   - Uses embeddings to understand meaning

2. **RAG = No Hallucinations**
   - LLM only uses retrieved knowledge base
   - All diagnosis grounded in actual data

3. **Urgency Classification**
   - Critical for safety
   - EMERGENCY | DON'T DRIVE | DRIVE CAREFULLY | CAN DRIVE

4. **Taglish Support**
   - Natural code-switching (realistic for PH market)
   - Both symptoms and responses in Taglish

5. **Python 3.14 Compatible**
   - Used Sentence-Transformers instead of ChromaDB
   - No external services needed

---

## 📁 Files You Should Know

| File | Purpose |
|------|---------|
| [PHASE2_COMPLETE.md](PHASE2_COMPLETE.md) | Full technical documentation |
| [README.md](README.md) | Project overview |
| [app/main.py](app/main.py) | Interactive entry point |
| [app/graph.py](app/graph.py) | LangGraph state machine |
| [app/nodes/diagnosis.py](app/nodes/diagnosis.py) | Core diagnosis logic |
| [app/rag/vector_store.py](app/rag/vector_store.py) | Semantic search engine |
| [app/knowledge_base/car_problems.json](app/knowledge_base/car_problems.json) | 25 car problems database |

---

## 🚀 Ready for Phase 3?

Once Phase 2 tests successfully, you're ready for:
- Cost estimation (₱ pricing from `pricing.json`)
- Enhanced Taglish handling
- Multi-turn conversation

See [master.md](../master.md) "Day 3" for Phase 3 build order.

---

**Phase 2 Complete!** 🎉  
**Time to test:** 5 minutes  
**Time to demo:** 3-4 minutes  
**Core diagnostic engine:** Fully operational ✅

---

*Last Updated: February 8, 2026*
