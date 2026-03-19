# ⚡ DSA Agent — Competitive Programming Solver

An AI-powered DSA solver that produces optimal C++17 solutions for competitive
programming platforms and LeetCode. Built with LangGraph, RAG, and Groq.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41-red)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Live Demo
[dsa-agent.streamlit.app](https://dsa-agent.streamlit.app)

## ✨ Features
- 7-node LangGraph agentic pipeline
- RAG knowledge base with DSA patterns, algorithms, and solved problems
- Real-time web search via Tavily
- Dedicated optimization pass targeting best time and space complexity
- Two output styles: competitive (main + cin) and LeetCode (class Solution)
- Fully free — Groq + Tavily both have generous free tiers

## 🛠️ Tech Stack
| Component | Technology |
|-----------|-----------|
| LLM | Llama 3.3 70B via Groq |
| Orchestration | LangGraph |
| Vector Store | ChromaDB |
| Embeddings | HuggingFace all-MiniLM-L6-v2 |
| Web Search | Tavily API |
| Frontend | Streamlit |
| Language Output | C++17 |

## ⚙️ Pipeline
```
retrieve → search → compress → analyze → optimize → generate → assemble
```

## 🔑 Get Free API Keys
- Groq: https://console.groq.com
- Tavily: https://app.tavily.com

## 💻 Run Locally
```bash
git clone https://github.com/yourusername/dsa-agent.git
cd dsa-agent
pip install -r requirements.txt
cp .env.example .env  # add your keys
python ingest.py
streamlit run app.py
```

## 📁 Project Structure
```
dsa-agent/
├── app.py              # Streamlit UI
├── agent.py            # LangGraph 7-node pipeline
├── rag.py              # ChromaDB RAG pipeline
├── ingest.py           # Knowledge base builder
├── requirements.txt
└── knowledge/
    ├── patterns.txt    # DSA patterns with C++ hints
    ├── algorithms.txt  # Algorithm implementations
    ├── hwi_problems.txt # Solved problems
    └── optimizations.txt # Optimization techniques
```

## 🧠 Architecture
The agent chains 7 focused LLM operations instead of one mega-prompt:
1. **Retrieve** — ChromaDB semantic search on DSA knowledge base
2. **Search** — Tavily web search for similar problems
3. **Compress** — Summarize retrieved context to 200 words
4. **Analyze** — Identify algorithmic pattern and plan approach
5. **Optimize** — Find best time/space complexity
6. **Generate** — Single LLM call producing both solution styles
7. **Assemble** — Format final output

Token optimization reduces usage by ~55% vs naive implementation.
