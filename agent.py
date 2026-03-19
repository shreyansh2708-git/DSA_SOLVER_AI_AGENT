import os
from dotenv import load_dotenv

load_dotenv()

from typing import TypedDict, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from rag import get_retriever

# ── Keys — session state (deployed) or .env (local) ──────────────────────────
def get_llm(groq_key: str):
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=groq_key
    )

def get_search_tool(tavily_key: str):
    os.environ["TAVILY_API_KEY"] = tavily_key
    return TavilySearchResults(max_results=2)

# ── Retriever (built once at module load) ─────────────────────────────────────
retriever = get_retriever()

# ── System Prompts ────────────────────────────────────────────────────────────
ANALYSIS_PROMPT = """You are an elite competitive programming expert and DSA specialist.
You solve problems on LeetCode, Codeforces, CodeChef, HackerRank, and all major platforms.
You always produce the MOST OPTIMAL solution — not just a correct one.

Core expertise: Greedy, DP (all variants + space optimization), Arrays/Strings,
Math (primes, GCD, bit tricks), Graphs (BFS/DFS/Dijkstra/DSU), Backtracking,
Monotonic Stack, Segment Tree, Sparse Table, Binary Search on Answer.

You always find the best time complexity, minimize memory, and identify mathematical
shortcuts before reaching for heavy algorithms."""

CODING_PROMPT = """You are an elite C++17 competitive programmer.
Rules:
- #include <bits/stdc++.h> and using namespace std;
- Fast I/O: ios::sync_with_stdio(false); cin.tie(NULL);
- Use "\\n" never endl
- unordered_map over map when order not needed
- reserve() vectors when size is known
- Iterative over recursive for large N
- emplace_back over push_back for complex types
- In-place / rolling array for space optimization
- Brief inline comments on non-obvious steps only"""


# ── State ─────────────────────────────────────────────────────────────────────
class AgentState(TypedDict):
    problem: str
    problem_short: str
    retrieved_context: str
    context_summary: str
    pattern_analysis: str
    optimized_approach: str
    solution_code_competitive: str
    solution_code_leetcode: str
    final_answer: str
    steps_log: List[str]


# ── Nodes ─────────────────────────────────────────────────────────────────────
def retrieve_context(state: AgentState) -> AgentState:
    try:
        docs = retriever.invoke(state["problem"])
        chunks = [d.page_content[:1500] for d in docs[:3]]
        state["retrieved_context"] = "\n---\n".join(chunks)
        state["steps_log"].append("✅ Retrieved DSA patterns from knowledge base.")
    except Exception as e:
        state["retrieved_context"] = ""
        state["steps_log"].append(f"⚠️ Retrieval skipped: {str(e)}")
    return state


def search_similar(state: AgentState, search_tool) -> AgentState:
    try:
        results = search_tool.invoke(
            f"optimal algorithm approach: {state['problem_short']}"
        )
        if isinstance(results, list):
            snippets = [r.get("content", "")[:400] for r in results[:2]]
            state["retrieved_context"] += "\nWEB:\n" + "\n".join(snippets)
        state["steps_log"].append("✅ Searched for optimal approaches.")
    except Exception as e:
        state["steps_log"].append(f"⚠️ Web search skipped: {str(e)}")
    return state


def summarize_context(state: AgentState, llm) -> AgentState:
    if not state["retrieved_context"].strip():
        state["context_summary"] = ""
        state["steps_log"].append("⚠️ No context to summarize.")
        return state

    prompt = f"""Extract only the most relevant algorithmic insights for solving this problem.
Output a tight summary (max 200 words) covering:
- Most relevant algorithm/pattern
- Key implementation trick if any
- Complexity of best known approach

PROBLEM (brief): {state['problem_short']}

RAW CONTEXT:
{state['retrieved_context']}

Output the summary only. No preamble."""

    response = llm.invoke([HumanMessage(content=prompt)])
    state["context_summary"] = response.content.strip()
    state["steps_log"].append("✅ Compressed context to concise summary.")
    return state


def analyze_and_plan(state: AgentState, llm) -> AgentState:
    prompt = f"""Analyze this problem:

PROBLEM:
{state['problem']}

RELEVANT CONTEXT:
{state['context_summary']}

Provide:
1. Core pattern (Greedy/DP/Two Pointers/Math/Graph/Backtracking/Stack)
2. Key observations (2-3 lines max)
3. Step-by-step algorithm (numbered, concise)
4. Data structures needed
5. Time complexity: O(?)
6. Space complexity: O(?)
7. Edge cases (brief list)

Be concise. No filler."""

    response = llm.invoke([
        SystemMessage(content=ANALYSIS_PROMPT),
        HumanMessage(content=prompt)
    ])
    state["pattern_analysis"] = response.content
    state["steps_log"].append("✅ Identified pattern and planned approach.")
    return state


def optimize_approach(state: AgentState, llm) -> AgentState:
    prompt = f"""Optimize this approach aggressively.

PROBLEM (brief): {state['problem_short']}

INITIAL APPROACH:
{state['pattern_analysis']}

Answer concisely:
1. TIME: Can we beat initial complexity?
2. SPACE: Rolling array? In-place? O(1) possible?
3. CONSTANTS: unordered_map, reserve(), iterative, avoid endl?
4. FINAL OPTIMAL APPROACH: algorithm + final O(time) + O(space)

If already optimal, state why in one line."""

    response = llm.invoke([
        SystemMessage(content=ANALYSIS_PROMPT),
        HumanMessage(content=prompt)
    ])
    state["optimized_approach"] = response.content
    state["steps_log"].append("✅ Optimized for time and memory efficiency.")
    return state


def generate_both_solutions(state: AgentState, llm) -> AgentState:
    prompt = f"""Generate TWO C++17 solutions for this problem.

PROBLEM:
{state['problem']}

OPTIMIZED APPROACH:
{state['optimized_approach']}

Output EXACTLY in this format with no extra text outside the blocks:

===COMPETITIVE===
// Competitive programming style (Codeforces/CodeChef/HackerRank)
// Uses main() + cin/cout + fast I/O
<complete cpp code here>
===END_COMPETITIVE===

===LEETCODE===
// LeetCode style
// Uses class Solution with correct method signature, no main/cin/cout
<complete cpp code here>
===END_LEETCODE===

Apply ALL optimizations: unordered_map, reserve(), iterative, "\\n" not endl."""

    response = llm.invoke([
        SystemMessage(content=CODING_PROMPT),
        HumanMessage(content=prompt)
    ])

    raw = response.content

    try:
        comp = raw.split("===COMPETITIVE===")[1].split("===END_COMPETITIVE===")[0].strip()
        for fence in ["```cpp", "```c++", "```"]:
            if fence in comp:
                comp = comp.split(fence)[1].split("```")[0].strip()
                break
        state["solution_code_competitive"] = comp
    except Exception:
        state["solution_code_competitive"] = raw
        state["steps_log"].append("⚠️ Competitive parse fallback.")

    try:
        lc = raw.split("===LEETCODE===")[1].split("===END_LEETCODE===")[0].strip()
        for fence in ["```cpp", "```c++", "```"]:
            if fence in lc:
                lc = lc.split(fence)[1].split("```")[0].strip()
                break
        state["solution_code_leetcode"] = lc
    except Exception:
        state["solution_code_leetcode"] = ""
        state["steps_log"].append("⚠️ LeetCode parse fallback.")

    state["steps_log"].append("✅ Generated both solutions.")
    return state


def assemble_answer(state: AgentState) -> AgentState:
    state["final_answer"] = (
        f"## 🧩 Pattern & Initial Analysis\n{state['pattern_analysis']}\n\n"
        f"---\n\n"
        f"## ⚡ Optimization Analysis\n{state['optimized_approach']}\n\n"
        f"---\n\n"
        f"## 🏆 Competitive Style\n```cpp\n{state['solution_code_competitive']}\n```\n\n"
        f"---\n\n"
        f"## 💻 LeetCode Style\n```cpp\n{state['solution_code_leetcode']}\n```"
    )
    state["steps_log"].append("✅ Done.")
    return state


# ── Build Graph ───────────────────────────────────────────────────────────────
def build_agent(groq_key: str, tavily_key: str):
    try:
        from langgraph.graph import StateGraph, END
    except ImportError:
        from langgraph.graph import StateGraph
        from langgraph.graph.graph import END

    llm = get_llm(groq_key)
    search_tool = get_search_tool(tavily_key)

    def _retrieve(state): return retrieve_context(state)
    def _search(state): return search_similar(state, search_tool)
    def _summarize(state): return summarize_context(state, llm)
    def _analyze(state): return analyze_and_plan(state, llm)
    def _optimize(state): return optimize_approach(state, llm)
    def _generate(state): return generate_both_solutions(state, llm)
    def _assemble(state): return assemble_answer(state)

    graph = StateGraph(AgentState)
    graph.add_node("retrieve_context", _retrieve)
    graph.add_node("search_similar", _search)
    graph.add_node("summarize_context", _summarize)
    graph.add_node("analyze_and_plan", _analyze)
    graph.add_node("optimize_approach", _optimize)
    graph.add_node("generate_both_solutions", _generate)
    graph.add_node("assemble_answer", _assemble)

    graph.set_entry_point("retrieve_context")
    graph.add_edge("retrieve_context", "search_similar")
    graph.add_edge("search_similar", "summarize_context")
    graph.add_edge("summarize_context", "analyze_and_plan")
    graph.add_edge("analyze_and_plan", "optimize_approach")
    graph.add_edge("optimize_approach", "generate_both_solutions")
    graph.add_edge("generate_both_solutions", "assemble_answer")
    graph.add_edge("assemble_answer", END)

    return graph.compile()


# ── Public API ────────────────────────────────────────────────────────────────
def solve_problem(problem: str, groq_key: str, tavily_key: str) -> AgentState:
    agent = build_agent(groq_key, tavily_key)
    initial_state: AgentState = {
        "problem": problem,
        "problem_short": problem[:400],
        "retrieved_context": "",
        "context_summary": "",
        "pattern_analysis": "",
        "optimized_approach": "",
        "solution_code_competitive": "",
        "solution_code_leetcode": "",
        "final_answer": "",
        "steps_log": []
    }
    return agent.invoke(initial_state)