# ARS Rapide LangGraph Chatbot

AI-powered automotive diagnostic chatbot for the Philippine market, built with LangGraph and Google Gemini.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Google API key
# Get your key at: https://makersuite.google.com/app/apikey
```

### 3. Run the Application

```bash
python app/main.py
```

## 📁 Project Structure

```
ars-langgraph-chatbot/
├── .env                    # Your API keys (DO NOT COMMIT)
├── requirements.txt        # Python dependencies
├── app/
│   ├── main.py            # Entry point
│   ├── graph.py           # LangGraph state machine
│   ├── nodes/             # Graph nodes (classifier, diagnosis, etc.)
│   ├── rag/               # RAG components (vector store, retriever)
│   ├── knowledge_base/    # Car repair data (JSON)
│   └── utils/             # Prompts and utilities
└── tests/                 # Unit tests
```

## 🛠 Tech Stack

- **LangChain** — Orchestration and chains
- **LangGraph** — Agentic graph-based flow control
- **Google Gemini** — LLM inference
- **ChromaDB** — Vector database for RAG
- **Pydantic v2** — Data validation

## 📊 Current Status

Phase 1 — Environment & Foundation: ✅ Complete  
Phase 2 — RAG & Diagnosis: ⏳ In Progress  
Phase 3 — Cost & Taglish: ⬜ Not Started  
Phase 4 — Booking & Polish: ⬜ Not Started

See [PROJECT_PROGRESS.md](../PROJECT_PROGRESS.md) for detailed tracking.

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Test specific module
python -m pytest tests/test_diagnosis.py -v
```

## 📝 Development Notes

- Keep files under 150 lines
- All prompts go in `app/utils/prompts.py`
- Use Pydantic BaseModel for all data structures
- No async (keeping it synchronous for clarity)
- API keys always in `.env`, never hardcoded

## 🎯 Competition Demo

Four demo scenarios prepared:
1. English symptom diagnosis
2. Taglish input handling
3. Multi-symptom reasoning
4. Full booking flow

## 📚 Documentation

- [Master Guide](../master.md) — Complete development guide
- [Technical Spec](../spec.md) — Architecture and build order
- [Pipeline Comparison](../comparison.md) — Tool selection rationale

---

**Built for ARS Rapide | February 2026**
