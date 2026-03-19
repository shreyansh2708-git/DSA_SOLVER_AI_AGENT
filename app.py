import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="DSA Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0f1117; color: #e2e8f0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem; max-width: 1400px; }

.hero-banner {
    background: linear-gradient(135deg, #1a1f2e 0%, #162032 50%, #1a1f2e 100%);
    border: 1px solid #2d3748; border-radius: 16px;
    padding: 2rem 2.5rem; margin-bottom: 2rem;
    position: relative; overflow: hidden;
}
.hero-banner::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4);
}
.hero-title {
    font-size: 2rem; font-weight: 700;
    background: linear-gradient(135deg, #a5b4fc, #818cf8, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem 0;
}
.hero-subtitle { color: #94a3b8; font-size: 0.95rem; margin: 0; }
.hero-badges { display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap; }
.badge {
    background: #1e293b; border: 1px solid #334155; color: #94a3b8;
    padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 500;
}
.badge-highlight {
    background: #1e1f3a; border: 1px solid #6366f1; color: #a5b4fc;
    padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600;
}
.stTextArea textarea {
    background: #1e293b !important; border: 1px solid #334155 !important;
    border-radius: 12px !important; color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.85rem !important; padding: 1rem !important; resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    padding: 0.75rem 2rem !important; font-weight: 600 !important;
    font-size: 1rem !important; width: 100% !important; transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.4) !important;
}
.pipeline-step {
    background: #1e293b; border: 1px solid #2d3748; border-radius: 10px;
    padding: 0.75rem 1rem; margin-bottom: 0.5rem;
    display: flex; align-items: center; gap: 0.75rem;
    font-size: 0.875rem; color: #94a3b8;
}
.pipeline-step.done { border-color: #10b981; background: #0d2420; color: #6ee7b7; }
.result-card {
    background: #1e293b; border: 1px solid #2d3748;
    border-radius: 14px; padding: 1.5rem; margin-bottom: 1.5rem;
}
.result-card-header {
    font-size: 0.8rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 1px; color: #6366f1; margin-bottom: 1rem;
    padding-bottom: 0.75rem; border-bottom: 1px solid #2d3748;
}
.stTabs [data-baseweb="tab-list"] {
    background: #1e293b !important; border-radius: 10px !important;
    padding: 4px !important; gap: 4px !important; border: 1px solid #2d3748 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 8px !important;
    color: #94a3b8 !important; font-weight: 500 !important;
    font-size: 0.875rem !important; padding: 0.5rem 1.25rem !important; border: none !important;
}
.stTabs [aria-selected="true"] { background: #6366f1 !important; color: white !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 1.5rem 0 0 0 !important; }
section[data-testid="stSidebar"] {
    background: #0f1117 !important; border-right: 1px solid #1e293b !important;
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem !important; }
.sidebar-card {
    background: #1e293b; border: 1px solid #2d3748;
    border-radius: 10px; padding: 1rem; margin-bottom: 1rem;
}
.sidebar-card-title {
    font-size: 0.7rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: 1px; color: #6366f1; margin-bottom: 0.75rem;
}
.sidebar-item {
    display: flex; align-items: center; gap: 0.5rem;
    font-size: 0.8rem; color: #94a3b8; padding: 0.35rem 0;
}
.free-badge {
    background: linear-gradient(135deg, #064e3b, #065f46);
    border: 1px solid #10b981; border-radius: 10px;
    padding: 0.75rem 1rem; margin-bottom: 1rem; text-align: center;
}
.free-badge-title {
    color: #6ee7b7; font-size: 1rem; font-weight: 700; margin-bottom: 0.25rem;
}
.free-badge-sub { color: #a7f3d0; font-size: 0.75rem; }
.info-box {
    background: #1e1f3a; border: 1px solid #3730a3; border-radius: 10px;
    padding: 1rem 1.25rem; margin: 1rem 0; font-size: 0.875rem; color: #a5b4fc;
}
.progress-bar-wrap {
    background: #1e293b; border-radius: 8px; height: 6px;
    margin: 0.5rem 0 1rem; overflow: hidden;
}
.progress-bar-fill {
    height: 100%; border-radius: 8px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4);
}
.stDownloadButton > button {
    background: #1e293b !important; border: 1px solid #4f46e5 !important;
    color: #a5b4fc !important; border-radius: 8px !important;
    font-size: 0.875rem !important; padding: 0.5rem 1rem !important; width: auto !important;
}
hr { border-color: #2d3748 !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #1e293b; }
::-webkit-scrollbar-thumb { background: #4f46e5; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
if "groq_key" not in st.session_state:
    st.session_state.groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
if "tavily_key" not in st.session_state:
    st.session_state.tavily_key = st.secrets.get("TAVILY_API_KEY", os.getenv("TAVILY_API_KEY", ""))
if "kb_ready" not in st.session_state:
    st.session_state.kb_ready = False


# ── Knowledge base auto-build ─────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def init_knowledge_base():
    from rag import load_vectorstore
    load_vectorstore()
    return True

with st.spinner("⚙️ Loading knowledge base... (first run takes ~30 seconds)"):
    try:
        init_knowledge_base()
        st.session_state.kb_ready = True
    except Exception as e:
        st.error(f"Knowledge base error: {e}")


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem;">
        <div style="font-size:2.5rem;">⚡</div>
        <div style="font-weight:700; font-size:1rem; color:#a5b4fc; margin-top:0.5rem;">DSA Agent</div>
        <div style="font-size:0.75rem; color:#64748b;">Competitive Programming Solver</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="free-badge">
        <div class="free-badge-title">🆓 100% Free to Use</div>
        <div class="free-badge-sub">No sign up · No API key needed · No limits</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-card-title">⚙️ Pipeline</div>
        <div class="sidebar-item">🔍 <span>Retrieve DSA patterns</span></div>
        <div class="sidebar-item">🌐 <span>Search similar problems</span></div>
        <div class="sidebar-item">🗜️ <span>Compress context</span></div>
        <div class="sidebar-item">🧩 <span>Analyze & plan</span></div>
        <div class="sidebar-item">⚡ <span>Optimize approach</span></div>
        <div class="sidebar-item">💻 <span>Generate both solutions</span></div>
        <div class="sidebar-item">✅ <span>Assemble answer</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-card-title">🎯 Platforms</div>
        <div class="sidebar-item">💻 <span>LeetCode</span></div>
        <div class="sidebar-item">⚔️ <span>Codeforces</span></div>
        <div class="sidebar-item">🍳 <span>CodeChef</span></div>
        <div class="sidebar-item">💼 <span>HackerRank</span></div>
        <div class="sidebar-item">🏢 <span>Company OAs</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-card-title">🛠️ Stack</div>
        <div class="sidebar-item">🤖 <span>Llama 3.3 70B (Groq)</span></div>
        <div class="sidebar-item">🔗 <span>LangGraph</span></div>
        <div class="sidebar-item">🗄️ <span>ChromaDb RAG</span></div>
        <div class="sidebar-item">🌐 <span>Tavily Search</span></div>
        <div class="sidebar-item">💡 <span>C++17 Output</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <div class="sidebar-card-title">⚡ Optimizations</div>
        <div class="sidebar-item">🗜️ <span>Context compression</span></div>
        <div class="sidebar-item">✂️ <span>~55% less token usage</span></div>
        <div class="sidebar-item">🔀 <span>Merged code generation</span></div>
        <div class="sidebar-item">📐 <span>Split system prompts</span></div>
        <div class="sidebar-item">🚀 <span>3 LLM calls total</span></div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero Banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">⚡ DSA Agent</div>
    <p class="hero-subtitle">Elite competitive programming solver · Optimal time & memory complexity · C++17 solutions for every platform</p>
    <div class="hero-badges">
        <span class="badge-highlight">⚡ Optimal Solutions</span>
        <span class="badge-highlight">🏆 Beats 90%+ Runtime</span>
        <span class="badge-highlight">🆓 Free to Use</span>
        <span class="badge">💻 LeetCode</span>
        <span class="badge">⚔️ Codeforces</span>
        <span class="badge">🍳 CodeChef</span>
        <span class="badge">🔍 RAG-Powered</span>
        <span class="badge">✂️ Low Token Usage</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_info = st.columns([3, 1], gap="large")

with col_input:
    st.markdown("<p style='color:#94a3b8; font-size:0.875rem; margin-bottom:0.5rem;'>📝 <b style='color:#e2e8f0;'>Problem Statement</b></p>", unsafe_allow_html=True)
    problem_input = st.text_area(
        label="problem",
        label_visibility="collapsed",
        height=280,
        placeholder="""Paste any DSA or competitive programming problem here...

Works with: LeetCode · Codeforces · CodeChef · HackerRank · Company OAs

Example:
Given an array of N integers, find the maximum sum subarray.
Constraints: 1 <= N <= 10^5, -10^4 <= A[i] <= 10^4
Input: 8 / -2 1 -3 4 -1 2 1 -5
Output: 6"""
    )
    solve_btn = st.button("⚡ Solve & Optimize", type="primary")

with col_info:
    st.markdown("""
    <div class="sidebar-card" style="margin-top:1.6rem;">
        <div class="sidebar-card-title">💡 Tips</div>
        <div style="font-size:0.8rem; color:#94a3b8; line-height:1.8;">
            ✔ Include constraints<br>
            ✔ Include example I/O<br>
            ✔ Paste full statement<br>
            ✔ Mention input format<br><br>
            <span style="color:#64748b;">Better input = better solution</span>
        </div>
    </div>
    <div class="info-box" style="margin-top:0;">
        ℹ️ Runs <b>7 pipeline steps</b><br>
        Includes <b>optimization pass</b><br>
        Only <b>3 LLM calls</b> total<br>
        Avg time: <b>40–60 seconds</b>
    </div>
    """, unsafe_allow_html=True)


# ── Solve ─────────────────────────────────────────────────────────────────────
if solve_btn:
    if not problem_input.strip():
        st.warning("⚠️ Please paste a problem statement first.")
    else:
        from agent import solve_problem

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<p style='color:#94a3b8; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px; font-weight:600;'>⚙️ Agent Pipeline</p>", unsafe_allow_html=True)

        steps_config = [
            ("🔍", "Retrieving DSA patterns from knowledge base..."),
            ("🌐", "Searching for optimal approaches..."),
            ("🗜️", "Compressing context to key insights..."),
            ("🧩", "Analyzing pattern and planning approach..."),
            ("⚡", "Optimizing time and memory complexity..."),
            ("💻", "Generating both solutions in one pass..."),
            ("✅", "Assembling final answer..."),
        ]

        step_placeholders = []
        for icon, label in steps_config:
            ph = st.empty()
            ph.markdown(
                f'<div class="pipeline-step"><span>{icon}</span>{label}</div>',
                unsafe_allow_html=True
            )
            step_placeholders.append((ph, icon, label))

        progress_ph = st.empty()
        progress_ph.markdown(
            '<div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:0%"></div></div>',
            unsafe_allow_html=True
        )

        with st.spinner(""):
            result = solve_problem(
                problem_input.strip(),
                st.session_state.groq_key,
                st.session_state.tavily_key
            )

        for ph, icon, label in step_placeholders:
            ph.markdown(
                f'<div class="pipeline-step done"><span>✅</span>{label.replace("...", " — Done")}</div>',
                unsafe_allow_html=True
            )
        progress_ph.markdown(
            '<div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:100%"></div></div>',
            unsafe_allow_html=True
        )

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#94a3b8; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px; font-weight:600; margin-bottom:1rem;'>📊 Results</p>",
            unsafe_allow_html=True
        )

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🧩  Pattern & Plan",
            "⚡  Optimization",
            "🏆  Competitive",
            "💻  LeetCode",
            "📋  Full Answer"
        ])

        with tab1:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-card-header">🧩 Pattern Recognition & Initial Plan</div>', unsafe_allow_html=True)
            st.markdown(result["pattern_analysis"])
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-card-header">⚡ Optimization Analysis — Time & Memory</div>', unsafe_allow_html=True)
            st.markdown(result["optimized_approach"])
            st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-card-header">🏆 Competitive Style — Codeforces / CodeChef / HackerRank</div>', unsafe_allow_html=True)
            if result.get("solution_code_competitive"):
                st.code(result["solution_code_competitive"], language="cpp")
                st.download_button(
                    label="⬇️ Download .cpp",
                    data=result["solution_code_competitive"],
                    file_name="solution_competitive.cpp",
                    mime="text/plain",
                    key="dl_competitive"
                )
            st.markdown('</div>', unsafe_allow_html=True)

        with tab4:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-card-header">💻 LeetCode Style — class Solution</div>', unsafe_allow_html=True)
            if result.get("solution_code_leetcode"):
                st.code(result["solution_code_leetcode"], language="cpp")
                st.download_button(
                    label="⬇️ Download .cpp",
                    data=result["solution_code_leetcode"],
                    file_name="solution_leetcode.cpp",
                    mime="text/plain",
                    key="dl_leetcode"
                )
            st.markdown('</div>', unsafe_allow_html=True)

        with tab5:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-card-header">📋 Complete Analysis</div>', unsafe_allow_html=True)
            st.markdown(result["final_answer"])
            st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("🔍 Agent Steps Log"):
            for step in result["steps_log"]:
                st.markdown(
                    f"<div style='font-size:0.875rem; color:#94a3b8; padding:0.3rem 0;'>{step}</div>",
                    unsafe_allow_html=True
                )
