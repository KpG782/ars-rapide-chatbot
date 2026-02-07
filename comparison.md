import { useState } from "react";

const PIPELINE_STAGES = [
  {
    id: "data-collection",
    label: "01",
    title: "Data Collection",
    icon: "⬇",
    color: "#4ade80",
    description: "Where your knowledge base comes from. For ARS, this is car repair data, Filipino mechanic terminology, Metro Manila pricing. You are NOT training an LLM from scratch — you are building the RAG knowledge base that Gemini will pull from.",
    whatToCollect: [
      { item: "Car problem descriptions", source: "Manual research + mechanic interviews" },
      { item: "Symptom → diagnosis mappings", source: "Automotive repair manuals" },
      { item: "Metro Manila 2024 pricing", source: "Local shops, online quotes" },
      { item: "Taglish car terms", source: "Filipino mechanic forums, Reddit PH" },
      { item: "Service categories + descriptions", source: "ARS internal data" },
    ],
    tools: [
      { name: "Web Scraping (BeautifulSoup)", rank: 1, why: "Simple, fast, free. Scrape car forums and pricing sites. No API needed.", fits: true },
      { name: "Google Sheets", rank: 2, why: "Easiest way to manually curate and organize your 50-100 car problems before converting to JSON. Shareable with domain experts.", fits: true },
      { name: "Selenium", rank: 3, why: "If BeautifulSoup can't handle dynamic pages. Overkill for most of what you need here.", fits: false },
    ],
  },
  {
    id: "data-preprocessing",
    label: "02",
    title: "Data Preprocessing",
    icon: "⚙",
    color: "#60a5fa",
    description: "Cleaning and structuring your raw data into the format ChromaDB can ingest. This is where messy real-world data becomes clean, structured JSON that produces good vector embeddings.",
    whatToCollect: [
      { item: "Remove duplicates and contradictions", source: "Two sources saying different things about the same problem" },
      { item: "Standardize symptom language", source: "\"Knocking\" vs \"tapping\" vs \"clicking\" — group them" },
      { item: "Add Taglish synonyms", source: "Map Filipino terms to English equivalents" },
      { item: "Structure into consistent JSON schema", source: "id, category, symptoms[], diagnosis, urgency, taglish_symptoms[]" },
      { item: "Validate pricing ranges", source: "Cross-check with 2+ sources" },
    ],
    tools: [
      { name: "Python (pandas)", rank: 1, why: "Industry standard for data cleaning. Read CSVs, deduplicate, transform, export to JSON. You already know Python.", fits: true },
      { name: "JSON Schema Validator", rank: 2, why: "Ensures every entry in your knowledge base has the right structure before it hits ChromaDB. Catches bugs early.", fits: true },
      { name: "spaCy NLP", rank: 3, why: "Could auto-extract symptoms from raw text. Overkill for 50-100 entries. Do it manually or with pandas.", fits: false },
    ],
  },
  {
    id: "embeddings",
    label: "03",
    title: "Embedding Generation",
    icon: "◈",
    color: "#a78bfa",
    description: "Converting your text data into numerical vectors that capture semantic meaning. This is how ChromaDB understands that \"kumakatok\" and \"knocking engine\" are related. Google's embedding model handles this for you.",
    whatToCollect: [
      { item: "Each knowledge base entry → vector", source: "Google Generative AI Embeddings API" },
      { item: "Chunk size matters", source: "Each JSON entry should be 1 chunk. Don't split single problems across chunks." },
      { item: "Metadata attached to vectors", source: "category, urgency, pricing tier — for filtering later" },
    ],
    tools: [
      { name: "Google Generative AI Embeddings", rank: 1, why: "You're already using Gemini. Same ecosystem, same API key. models/embedding-001 is free tier friendly.", fits: true },
      { name: "Sentence-Transformers (HuggingFace)", rank: 2, why: "Runs locally, no API cost. Good backup if Google API has rate limits during dev.", fits: true },
      { name: "OpenAI Embeddings", rank: 3, why: "text-embedding-ada-002 is excellent but costs money per token. No reason to use two LLM providers.", fits: false },
    ],
  },
  {
    id: "vector-store",
    label: "04",
    title: "Vector Store (RAG)",
    icon: "▦",
    color: "#fb923c",
    description: "Where your embeddings live and where semantic search happens. When a user says \"my car won't start\", the retriever searches this store to find the 3 most similar problems from your knowledge base.",
    whatToCollect: [],
    isVectorDeepDive: true,
    tools: [
      { name: "ChromaDB", rank: 1, why: "Runs locally, zero infrastructure, Python-native API, built-in metadata filtering. Perfect for under 10M vectors. This is your pick.", fits: true },
      { name: "FAISS", rank: 2, why: "Faster raw search speed, but it's just a library — no database features. You'd have to build storage, APIs, metadata filtering yourself.", fits: false },
      { name: "Pinecone", rank: 3, why: "Fully managed cloud service. Great for production at scale. Overkill and costs money for a competition project with ~100 entries.", fits: false },
    ],
  },
  {
    id: "llm-inference",
    label: "05",
    title: "LLM Inference",
    icon: "⚡",
    color: "#f472b6",
    description: "The actual AI reasoning. Gemini receives the user's message + retrieved context from RAG, then generates the diagnosis, cost estimate, or response. This is where LangGraph orchestrates which node runs and what prompt to use.",
    whatToCollect: [
      { item: "Prompt engineering", source: "All prompts in prompts.py. Tune these iteratively." },
      { item: "Context window management", source: "Only send relevant retrieved docs, not everything." },
      { item: "Temperature setting", source: "Lower (0.2-0.4) for diagnosis accuracy. Higher (0.6-0.8) for conversational responses." },
    ],
    tools: [
      { name: "Google Gemini (gemini-1.5-pro)", rank: 1, why: "Already chosen. Free tier is generous. Low latency from PH to Google Asia servers.", fits: true },
      { name: "Groq (Llama 3)", rank: 2, why: "Extremely fast inference. Good backup if Gemini has issues. Free tier available.", fits: true },
      { name: "OpenAI GPT-4o", rank: 3, why: "Excellent model but costs more per token and has higher latency from Philippines.", fits: false },
    ],
  },
  {
    id: "orchestration",
    label: "06",
    title: "Orchestration",
    icon: "◇",
    color: "#34d399",
    description: "LangGraph is the brain that decides what happens next in the conversation. It manages the flow: classify intent → run diagnosis → estimate cost → optionally book. This is what makes it agentic — the graph reasons about the next step.",
    whatToCollect: [
      { item: "State management", source: "Pydantic ChatState flows through every node" },
      { item: "Conditional routing", source: "LLM decides: diagnose? estimate? book? or just chat?" },
      { item: "Error handling", source: "What if Gemini returns garbage? Catch it, ask again." },
    ],
    tools: [
      { name: "LangGraph", rank: 1, why: "Graph-based agentic flow control. Nodes are testable. Conditional edges are the agentic decision layer. This is your core.", fits: true },
      { name: "LangChain", rank: 2, why: "Used inside LangGraph for chains, prompts, and the retriever interface. They work together — LangChain is the toolkit, LangGraph is the orchestrator.", fits: true },
      { name: "CrewAI", rank: 3, why: "Multi-agent framework. Impressive but over-engineered for a single chatbot. Don't add complexity you don't need.", fits: false },
    ],
  },
  {
    id: "deployment",
    label: "07",
    title: "Deployment",
    icon: "☁",
    color: "#38bdf8",
    description: "Getting it from your laptop to somewhere users can actually hit it. For a competition, a clean API endpoint is the standard. For production later, containerize it.",
    whatToCollect: [
      { item: "REST API endpoint", source: "FastAPI wraps your LangGraph app. POST /chat, get response." },
      { item: "Environment variables", source: "GOOGLE_API_KEY never leaves .env" },
      { item: "Docker container (bonus)", source: "Shows judges you think about production. Not required for demo." },
    ],
    tools: [
      { name: "FastAPI", rank: 1, why: "Fastest Python web framework. Auto-generates docs. Async-capable but you don't have to use async. Industry standard.", fits: true },
      { name: "Railway / Render", rank: 2, why: "Free-tier cloud hosting. Deploy from GitHub in 5 minutes. No VPS management.", fits: true },
      { name: "AWS Lambda", rank: 3, why: "Serverless and scalable but cold starts kill chatbot latency. Overkill for this project.", fits: false },
    ],
  },
  {
    id: "monitoring",
    label: "08",
    title: "Monitoring & Observability",
    icon: "👁",
    color: "#fbbf24",
    description: "Watching your system in production. Are responses good? Are costs spiking? Is latency acceptable? For a competition this is bonus points. For production this is non-negotiable.",
    whatToCollect: [
      { item: "Trace every LLM call", source: "What prompt went in, what came out, how long it took" },
      { item: "Cost tracking", source: "How many tokens are you burning per conversation?" },
      { item: "User feedback", source: "Thumbs up/down on responses. Gold for improving prompts." },
    ],
    tools: [
      { name: "LangSmith", rank: 1, why: "Built by the LangChain team. Native LangGraph integration — one env variable and it traces everything. Best debugging experience for your stack.", fits: true },
      { name: "Langfuse", rank: 2, why: "Open source, self-hostable, framework agnostic. Generous free tier (50K events/mo). Great if you want data sovereignty.", fits: true },
      { name: "Helicone", rank: 3, why: "Proxy-based, minimal setup. Good for cost tracking but weaker on multi-step workflow tracing. Less ideal for LangGraph agents.", fits: false },
    ],
  },
];

const VECTOR_COMPARISON = {
  chromadb: {
    name: "ChromaDB",
    verdict: "✅ YOUR PICK",
    verdictColor: "#4ade80",
    points: [
      { label: "Setup", value: "5 lines of code. pip install chromadb. Done.", good: true },
      { label: "Storage", value: "Local filesystem. No cloud dependency. Works offline for demos.", good: true },
      { label: "API", value: "Full Python database API. Metadata filtering built in.", good: true },
      { label: "LangChain", value: "Native integration. as_retriever() works out of the box.", good: true },
      { label: "Scale limit", value: "~10M vectors. Your KB has ~100. Not a problem.", good: true },
      { label: "Cost", value: "$0. Open source Apache 2.0.", good: true },
    ],
  },
  faiss: {
    name: "FAISS",
    verdict: "⚠️ Not for this project",
    verdictColor: "#fb923c",
    points: [
      { label: "Setup", value: "pip install faiss-cpu. But then you build everything else yourself.", good: true },
      { label: "Speed", value: "~1000x faster than Pinecone for raw search. But irrelevant at 100 vectors.", good: false },
      { label: "Storage", value: "In-memory only by default. You must write your own persistence layer.", good: false },
      { label: "API", value: "Low-level C++ library with Python bindings. No REST API, no metadata filtering.", good: false },
      { label: "LangChain", value: "Works but requires more glue code than ChromaDB.", good: false },
      { label: "Use case", value: "Research labs. Image search at billions of vectors. Not chatbot RAG.", good: false },
    ],
  },
  pinecone: {
    name: "Pinecone",
    verdict: "❌ Overkill",
    verdictColor: "#f87171",
    points: [
      { label: "Setup", value: "Cloud account, API key, create index. Network-dependent.", good: false },
      { label: "Speed", value: "Good but network latency adds 28+ seconds to setup vs local.", good: false },
      { label: "Storage", value: "Fully managed cloud. Great for enterprise. Unnecessary for 100 vectors.", good: false },
      { label: "API", value: "REST + SDK. Well-documented. But why pay for an API when local works?", good: false },
      { label: "Cost", value: "Free tier is limited. Paid plans start at $70/month for basic usage.", good: false },
      { label: "Use case", value: "Production apps with millions of vectors and multiple teams.", good: false },
    ],
  },
};

const INFERENCE_FRAMEWORKS = {
  title: "Why NOT ONNX, TFLite, or OpenVINO?",
  explanation: "These are model inference optimization frameworks. They optimize how a trained model runs on specific hardware. But here's the key thing you need to understand about your project:",
  keyInsight: "You are NOT running a local model. You are calling Gemini via API. ONNX, TFLite, and OpenVINO are irrelevant to your architecture.",
  frameworks: [
    {
      name: "ONNX Runtime",
      what: "A universal model format + inference engine. Converts models from PyTorch/TensorFlow into a portable format that runs fast on any hardware.",
      whenToUse: "You train your OWN model locally and need to deploy it on different hardware (CPU, GPU, mobile). Cross-platform portability is the goal.",
      whyNotYours: "You're not training a model. You're calling Google's Gemini API over HTTP. There's no local model to optimize. ONNX has nothing to do here.",
      color: "#60a5fa",
    },
    {
      name: "TensorFlow Lite",
      what: "Google's framework for running ML models on mobile and edge devices. Compresses models, quantizes weights, makes them tiny and fast.",
      whenToUse: "Mobile apps (Android/iOS) that need on-device AI. Image classification on a phone. Wake word detection. No internet required.",
      whyNotYours: "Your chatbot needs Gemini's full reasoning power. No mobile-sized model can diagnose car problems with the accuracy Gemini provides. And you need internet anyway for the API call.",
      color: "#34d399",
    },
    {
      name: "OpenVINO",
      what: "Intel's toolkit for optimizing AI inference specifically on Intel hardware (CPUs, GPUs, VPUs). Massive speedups on Intel chips.",
      whenToUse: "You have Intel hardware and a trained model you're running locally. Computer vision on security cameras. Industrial IoT on Intel edge devices.",
      whyNotYours: "Intel-specific optimization. Your bottleneck is not CPU speed — it's Gemini's API response time (network latency). Optimizing local inference won't help.",
      color: "#fb923c",
    },
  ],
  whenYOUWouldUseThese: "If ARS later builds a LOCAL model for quick pre-screening (e.g., a small classifier that categorizes symptoms before hitting Gemini), THEN you'd consider these. Specifically: ONNX if you want cross-platform, TFLite if you're putting it on a mobile Flutter app, OpenVINO if your server runs Intel.",
};

// ─── COMPONENTS ───────────────────────────────────────────────

function PipelineHeader() {
  return (
    <div style={{ textAlign: "center", marginBottom: 40, paddingBottom: 32, borderBottom: "1px solid #2a2a2a" }}>
      <div style={{ fontSize: 11, letterSpacing: 4, color: "#666", textTransform: "uppercase", marginBottom: 10 }}>ARS Rapide — Full System Pipeline</div>
      <h1 style={{ fontSize: 28, fontFamily: "'Courier New', monospace", color: "#fff", margin: 0, fontWeight: 400 }}>
        Data → Embeddings → RAG → Inference → Deploy → Monitor
      </h1>
      <div style={{ fontSize: 13, color: "#666", marginTop: 10 }}>Click any stage. Top 3 tools are ranked. ✅ = use it. ❌ = skip it.</div>
    </div>
  );
}

function StageSelector({ stages, activeId, onSelect }) {
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 28, justifyContent: "center" }}>
      {stages.map((s) => (
        <button
          key={s.id}
          onClick={() => onSelect(s.id)}
          style={{
            background: activeId === s.id ? s.color : "transparent",
            color: activeId === s.id ? "#000" : "#aaa",
            border: `1px solid ${activeId === s.id ? s.color : "#333"}`,
            borderRadius: 6,
            padding: "7px 14px",
            cursor: "pointer",
            fontFamily: "'Courier New', monospace",
            fontSize: 13,
            fontWeight: activeId === s.id ? 700 : 400,
            transition: "all 0.2s",
          }}
        >
          <span style={{ opacity: 0.6, marginRight: 6 }}>{s.label}</span>{s.title}
        </button>
      ))}
    </div>
  );
}

function StageCard({ stage }) {
  return (
    <div style={{ background: "#1a1a1a", borderRadius: 12, border: "1px solid #2a2a2a", overflow: "hidden" }}>
      {/* Header */}
      <div style={{ background: "#111", padding: "18px 24px", borderBottom: "1px solid #2a2a2a", display: "flex", alignItems: "center", gap: 16 }}>
        <div style={{
          width: 44, height: 44, borderRadius: 10,
          background: stage.color + "18", border: `1px solid ${stage.color}44`,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 20, color: stage.color, flexShrink: 0
        }}>{stage.icon}</div>
        <div>
          <div style={{ fontSize: 11, color: stage.color, letterSpacing: 2, textTransform: "uppercase", fontFamily: "'Courier New', monospace" }}>{stage.label} — Stage</div>
          <div style={{ fontSize: 20, color: "#fff", fontFamily: "'Courier New', monospace", fontWeight: 400 }}>{stage.title}</div>
        </div>
      </div>

      <div style={{ padding: 24 }}>
        {/* Description */}
        <p style={{ color: "#aaa", fontSize: 14, lineHeight: 1.7, margin: "0 0 24px", maxWidth: 680 }}>{stage.description}</p>

        {/* What to collect / do */}
        {stage.whatToCollect && stage.whatToCollect.length > 0 && (
          <div style={{ marginBottom: 28 }}>
            <div style={{ fontSize: 11, color: "#555", letterSpacing: 2, textTransform: "uppercase", marginBottom: 12, fontFamily: "'Courier New', monospace" }}>What to do here</div>
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {stage.whatToCollect.map((w, i) => (
                <div key={i} style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
                  <div style={{ color: stage.color, fontSize: 12, marginTop: 2, flexShrink: 0 }}>›</div>
                  <div>
                    <span style={{ color: "#ddd", fontSize: 14 }}>{w.item}</span>
                    <span style={{ color: "#555", fontSize: 13, marginLeft: 8 }}>— {w.source}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Vector deep dive link */}
        {stage.isVectorDeepDive && (
          <div style={{ background: "#fb923c11", border: "1px solid #fb923c33", borderRadius: 8, padding: "12px 16px", marginBottom: 24 }}>
            <div style={{ color: "#fb923c", fontSize: 13, fontFamily: "'Courier New', monospace" }}>↓ See "ChromaDB vs FAISS vs Pinecone" deep dive below the tool cards</div>
          </div>
        )}

        {/* Top 3 Tools */}
        <div>
          <div style={{ fontSize: 11, color: "#555", letterSpacing: 2, textTransform: "uppercase", marginBottom: 12, fontFamily: "'Courier New', monospace" }}>Top 3 Tools — Ranked</div>
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {stage.tools.map((t, i) => (
              <div key={i} style={{
                display: "flex", alignItems: "flex-start", gap: 14,
                background: t.fits ? "#1e2a1e" : "#1f1f1f",
                border: `1px solid ${t.fits ? "#4ade8033" : "#2a2a2a"}`,
                borderRadius: 8, padding: "14px 16px",
              }}>
                <div style={{
                  width: 28, height: 28, borderRadius: 6, flexShrink: 0,
                  background: t.fits ? "#4ade8022" : "#33333344",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  color: t.fits ? "#4ade80" : "#666",
                  fontSize: 13, fontFamily: "'Courier New', monospace", fontWeight: 700,
                }}>{t.rank}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    <span style={{ color: "#fff", fontSize: 15, fontWeight: 600 }}>{t.name}</span>
                    <span style={{
                      fontSize: 10, padding: "2px 8px", borderRadius: 10,
                      background: t.fits ? "#4ade8022" : "#f8717133",
                      color: t.fits ? "#4ade80" : "#f87171",
                      fontFamily: "'Courier New', monospace", letterSpacing: 1,
                    }}>{t.fits ? "USE THIS" : "SKIP"}</span>
                  </div>
                  <p style={{ color: "#888", fontSize: 13, margin: "4px 0 0", lineHeight: 1.5 }}>{t.why}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function VectorDeepDive() {
  const [active, setActive] = useState("chromadb");
  const db = VECTOR_COMPARISON[active];
  return (
    <div style={{ background: "#111", border: "1px solid #fb923c44", borderRadius: 12, overflow: "hidden", marginTop: 28 }}>
      <div style={{ padding: "16px 24px", borderBottom: "1px solid #2a2a2a", background: "#0d0d0d" }}>
        <div style={{ fontSize: 11, color: "#fb923c", letterSpacing: 2, textTransform: "uppercase", fontFamily: "'Courier New', monospace", marginBottom: 4 }}>Deep Dive</div>
        <div style={{ color: "#fff", fontSize: 17, fontFamily: "'Courier New', monospace" }}>ChromaDB vs FAISS vs Pinecone — Why ChromaDB wins here</div>
      </div>
      {/* Selector tabs */}
      <div style={{ display: "flex", borderBottom: "1px solid #2a2a2a" }}>
        {Object.entries(VECTOR_COMPARISON).map(([key, val]) => (
          <button key={key} onClick={() => setActive(key)} style={{
            flex: 1, padding: "12px 0", background: active === key ? "#1a1a1a" : "transparent",
            border: "none", borderBottom: active === key ? "2px solid #fb923c" : "2px solid transparent",
            color: active === key ? "#fff" : "#666", cursor: "pointer", fontSize: 14, fontFamily: "'Courier New', monospace",
            transition: "all 0.2s",
          }}>{val.name}</button>
        ))}
      </div>
      <div style={{ padding: 24 }}>
        <div style={{
          display: "inline-block", padding: "4px 12px", borderRadius: 20,
          background: db.verdictColor + "22", border: `1px solid ${db.verdictColor}44`,
          color: db.verdictColor, fontSize: 13, fontFamily: "'Courier New', monospace", fontWeight: 700, marginBottom: 16,
        }}>{db.verdict}</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {db.points.map((p, i) => (
            <div key={i} style={{ display: "flex", gap: 12, alignItems: "flex-start" }}>
              <div style={{ color: p.good ? "#4ade80" : "#f87171", fontSize: 14, flexShrink: 0, marginTop: 1 }}>{p.good ? "✓" : "✗"}</div>
              <div>
                <span style={{ color: "#aaa", fontSize: 13, fontFamily: "'Courier New', monospace" }}>{p.label}: </span>
                <span style={{ color: "#ddd", fontSize: 13 }}>{p.value}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function InferenceFrameworksPanel() {
  const [expanded, setExpanded] = useState(null);
  const f = INFERENCE_FRAMEWORKS;
  return (
    <div style={{ background: "#111", border: "1px solid #a78bfa44", borderRadius: 12, overflow: "hidden", marginTop: 32 }}>
      <div style={{ padding: "16px 24px", borderBottom: "1px solid #2a2a2a", background: "#0d0d0d" }}>
        <div style={{ fontSize: 11, color: "#a78bfa", letterSpacing: 2, textTransform: "uppercase", fontFamily: "'Courier New', monospace", marginBottom: 4 }}>Explainer</div>
        <div style={{ color: "#fff", fontSize: 17, fontFamily: "'Courier New', monospace" }}>{f.title}</div>
      </div>
      <div style={{ padding: 24 }}>
        <p style={{ color: "#aaa", fontSize: 14, lineHeight: 1.7, margin: "0 0 12px" }}>{f.explanation}</p>
        <div style={{ background: "#a78bfa18", border: "1px solid #a78bfa33", borderRadius: 8, padding: "14px 18px", marginBottom: 24 }}>
          <div style={{ color: "#a78bfa", fontSize: 14, fontWeight: 700 }}>💡 Key insight</div>
          <p style={{ color: "#ddd", fontSize: 14, margin: "6px 0 0", lineHeight: 1.6 }}>{f.keyInsight}</p>
        </div>
        {/* Framework cards */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {f.frameworks.map((fw, i) => (
            <div key={i} style={{ border: "1px solid #2a2a2a", borderRadius: 8, overflow: "hidden" }}>
              <button onClick={() => setExpanded(expanded === i ? null : i)} style={{
                width: "100%", textAlign: "left", background: expanded === i ? "#1a1a1a" : "#151515",
                border: "none", padding: "14px 18px", cursor: "pointer", display: "flex", alignItems: "center", gap: 12,
              }}>
                <div style={{ width: 10, height: 10, borderRadius: "50%", background: fw.color, flexShrink: 0 }} />
                <span style={{ color: "#fff", fontSize: 15, fontFamily: "'Courier New', monospace", fontWeight: 600, flex: 1 }}>{fw.name}</span>
                <span style={{ color: "#555", fontSize: 18 }}>{expanded === i ? "−" : "+"}</span>
              </button>
              {expanded === i && (
                <div style={{ padding: "0 18px 18px", background: "#1a1a1a" }}>
                  <div style={{ marginBottom: 10 }}>
                    <div style={{ fontSize: 11, color: "#555", letterSpacing: 1, textTransform: "uppercase", marginBottom: 4, fontFamily: "'Courier New', monospace" }}>What it does</div>
                    <p style={{ color: "#aaa", fontSize: 13, margin: 0, lineHeight: 1.6 }}>{fw.what}</p>
                  </div>
                  <div style={{ marginBottom: 10 }}>
                    <div style={{ fontSize: 11, color: "#4ade80", letterSpacing: 1, textTransform: "uppercase", marginBottom: 4, fontFamily: "'Courier New', monospace" }}>When you'd actually use it</div>
                    <p style={{ color: "#aaa", fontSize: 13, margin: 0, lineHeight: 1.6 }}>{fw.whenToUse}</p>
                  </div>
                  <div style={{ background: "#f8717122", borderRadius: 6, padding: "10px 14px" }}>
                    <div style={{ fontSize: 11, color: "#f87171", letterSpacing: 1, textTransform: "uppercase", marginBottom: 4, fontFamily: "'Courier New', monospace" }}>Why it doesn't apply to ARS</div>
                    <p style={{ color: "#ddd", fontSize: 13, margin: 0, lineHeight: 1.6 }}>{fw.whyNotYours}</p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
        {/* When you WOULD use them */}
        <div style={{ marginTop: 20, background: "#1e2a1e", border: "1px solid #4ade8033", borderRadius: 8, padding: "14px 18px" }}>
          <div style={{ color: "#4ade80", fontSize: 13, fontWeight: 700, marginBottom: 6 }}>↳ When ARS WOULD use these (future)</div>
          <p style={{ color: "#aaa", fontSize: 13, margin: 0, lineHeight: 1.6 }}>{f.whenYOUWouldUseThese}</p>
        </div>
      </div>
    </div>
  );
}

function PipelineFlow() {
  return (
    <div style={{ display: "flex", alignItems: "center", justifyContent: "center", flexWrap: "wrap", gap: 4, marginBottom: 32 }}>
      {["Data\nCollect", "Preprocess", "Embed", "RAG\nStore", "LLM\nInfer", "Orchestrate", "Deploy", "Monitor"].map((label, i) => (
        <div key={i} style={{ display: "flex", alignItems: "center" }}>
          <div style={{
            background: "#1a1a1a", border: "1px solid #333", borderRadius: 6,
            padding: "6px 12px", minWidth: 72, textAlign: "center",
          }}>
            {label.split("\n").map((l, j) => (
              <div key={j} style={{ color: "#ccc", fontSize: 11, fontFamily: "'Courier New', monospace", lineHeight: 1.4 }}>{l}</div>
            ))}
          </div>
          {i < 7 && <div style={{ color: "#444", fontSize: 16, margin: "0 2px" }}>→</div>}
        </div>
      ))}
    </div>
  );
}

// ─── MAIN ─────────────────────────────────────────────────────

export default function App() {
  const [activeStage, setActiveStage] = useState("data-collection");
  const stage = PIPELINE_STAGES.find((s) => s.id === activeStage);

  return (
    <div style={{
      minHeight: "100vh", background: "#0f0f0f", color: "#fff",
      fontFamily: "'Segoe UI', system-ui, sans-serif", padding: "32px 20px",
    }}>
      <div style={{ maxWidth: 760, margin: "0 auto" }}>
        <PipelineHeader />
        <PipelineFlow />
        <StageSelector stages={PIPELINE_STAGES} activeId={activeStage} onSelect={setActiveStage} />
        {stage && <StageCard stage={stage} />}
        {activeStage === "vector-store" && <VectorDeepDive />}
        <InferenceFrameworksPanel />
      </div>
    </div>
  );
}