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
- **Sentence-Transformers** — Vector embeddings for semantic search (Python 3.14 compatible)
- **Pydantic v2** — Data validation

## 📊 Current Status

Phase 1 — Environment & Foundation: ✅ Complete  
Phase 2 — RAG & Diagnosis: ✅ Complete  
Phase 3 — Cost & Taglish: ✅ Complete  
Phase 4 — Booking & Polish: ⬜ Not Started  

**What's Working Now (Competition-Ready):**
- ✅ 25 car problems with 89 Taglish terms
- ✅ Taglish normalization ("umiinit ang kotse" → "car is overheating")
- ✅ Semantic search with confidence scoring
- ✅ RAG-powered diagnosis (concise, 100-150 words)
- ✅ Cost estimation with Metro Manila pricing
- ✅ Urgency classification with visual indicators
- ✅ Natural code-switching responses
- ✅ Interactive chat mode with confidence bars

**Response Quality:** Optimized for competition demo (concise, actionable, engaging)

See [PHASE3_COMPLETE.md](PHASE3_COMPLETE.md) for detailed Phase 3 documentation.

## 🧪 Testing

```bash
# Test vector store
python -m app.rag.vector_store

# Test retriever
python -m app.rag.retriever

# Test diagnosis node
python -m app.nodes.diagnosis

# Run interactive mode
python app/main.py
```

**Try these test cases:**
- `my car won't start` → Dead battery diagnosis
- `umiinit ang engine ko` → Overheating (Taglish)
- `squeaky brakes when stopping` → Brake wear
- `kumakatok ang engine` → Engine knocking (Taglish)

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
