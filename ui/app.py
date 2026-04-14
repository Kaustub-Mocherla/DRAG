from __future__ import annotations

import time

import requests
import streamlit as st


st.set_page_config(
    page_title="DRAG",
    page_icon="D",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            color-scheme: dark;
            --bg-main: #030305;
            --bg-elev: #0b0b12;
            --text-main: #eaf2ff;
            --text-soft: rgba(226, 232, 240, 0.76);
            --accent: #32e3ff;
            --accent-soft: #b7f5ff;
        }
        html, body, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 5% -8%, rgba(50, 227, 255, 0.17), transparent 34%),
                radial-gradient(circle at 96% 0%, rgba(50, 227, 255, 0.12), transparent 36%),
                radial-gradient(circle at 50% 120%, rgba(50, 227, 255, 0.08), transparent 45%),
                var(--bg-main);
            color: var(--text-main);
        }
        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #080810 0%, #05050a 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.16);
            box-shadow: inset -1px 0 0 rgba(255, 255, 255, 0.03);
        }
        [data-testid="stSidebar"] * {
            color: #dbe6ff;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        .hero {
            position: relative;
            padding: 2rem 1.7rem;
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 1.4rem;
            background:
                linear-gradient(135deg, rgba(18, 20, 31, 0.95), rgba(8, 9, 15, 0.98));
            margin-bottom: 1.35rem;
            box-shadow:
                0 0 0 1px rgba(255, 255, 255, 0.03),
                0 20px 42px rgba(0, 0, 0, 0.55),
                0 0 60px rgba(50, 227, 255, 0.14);
            overflow: hidden;
        }
        .hero::before {
            content: "";
            position: absolute;
            top: -40%;
            right: -20%;
            width: 320px;
            height: 320px;
            background: radial-gradient(circle, rgba(50, 227, 255, 0.2), transparent 60%);
            pointer-events: none;
        }
        .hero h1 {
            margin: 0;
            font-size: 2.45rem;
            font-weight: 800;
            letter-spacing: 0.01em;
            background: linear-gradient(90deg, #ffffff 0%, #dffbff 50%, #95f2ff 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 24px rgba(50, 227, 255, 0.22);
        }
        .hero p {
            margin: 0.5rem 0 0;
            color: var(--text-soft);
            font-size: 1.02rem;
        }
        .metric-card {
            padding: 1rem 1.1rem;
            border-radius: 1rem;
            background: #0e0f17;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        .source-chip {
            display: inline-block;
            padding: 0.37rem 0.74rem;
            margin: 0.2rem 0.35rem 0.2rem 0;
            border-radius: 999px;
            background: linear-gradient(135deg, rgba(50, 227, 255, 0.24), rgba(50, 227, 255, 0.14));
            border: 1px solid rgba(161, 196, 253, 0.35);
            color: #f2f8ff;
            font-size: 0.85rem;
            box-shadow: 0 4px 16px rgba(50, 227, 255, 0.14);
        }
        .muted {
            color: rgba(226, 232, 240, 0.58);
        }
        h3 {
            color: #f3f8ff;
            letter-spacing: 0.01em;
        }
        [data-testid="stForm"] {
            padding: 0.5rem;
            border-radius: 1rem;
            background: linear-gradient(180deg, rgba(14, 16, 24, 0.72), rgba(8, 10, 16, 0.72));
            border: 1px solid rgba(148, 163, 184, 0.14);
        }
        .stButton button {
            background: linear-gradient(90deg, #b7f5ff 0%, #73ebff 50%, #32e3ff 100%);
            color: #0b1020;
            border: 0;
            border-radius: 0.85rem;
            padding: 0.58rem 1.08rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            box-shadow:
                0 12px 24px rgba(50, 227, 255, 0.26),
                0 0 22px rgba(50, 227, 255, 0.22);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }
        .stButton button:hover {
            background: linear-gradient(90deg, #d3fbff 0%, #99f2ff 50%, #4ce7ff 100%);
            color: #050814;
            border: 0;
            transform: translateY(-1px);
            box-shadow:
                0 16px 28px rgba(50, 227, 255, 0.32),
                0 0 26px rgba(50, 227, 255, 0.24);
        }
        .stTextInput input {
            background: linear-gradient(180deg, #10121b 0%, #0a0b12 100%);
            color: #f5f7fa;
            border: none;
            border-radius: 1rem;
            box-shadow: inset 0 0 0 1px rgba(161, 196, 253, 0.22),
                        0 0 0 1px rgba(255, 255, 255, 0.02);
        }
        .stTextInput input:focus,
        .stTextInput input:focus-visible {
            outline: none;
            border: none;
            box-shadow: inset 0 0 0 1px rgba(161, 196, 253, 0.34),
                        0 0 20px rgba(50, 227, 255, 0.24);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>DRAG</h1>
        <p>Distributed Retrieval-Augmented Generation for fast, source-aware knowledge search.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Search Workflow")
    st.write("1. Ask a question.")
    st.write("2. The coordinator queries all retrieval nodes.")
    st.write("3. Ollama generates a grounded answer with sources.")
    st.divider()
    st.caption("Coordinator: `http://localhost:9000/search`")
    st.caption("Built for local document collections and PDF-based knowledge bases.")

left, right = st.columns([2, 1])

with left:
    st.markdown("### Ask a question")
    st.caption("Search your organization's knowledge base with a single query.")

    with st.form("search_form", clear_on_submit=False):
        query = st.text_input(
            "Search query",
            placeholder="Search your organization's knowledge base...",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("Search")

if submitted:
    query = query.strip()
    if not query:
        st.warning("Please enter a question before searching.")
    else:
        start = time.time()
        try:
            with st.spinner("Searching nodes and generating an answer..."):
                response = requests.post(
                    "http://localhost:9000/search",
                    json={"query": query},
                    stream=True,
                    timeout=120,
                )
                response.raise_for_status()

                sources = [source for source in response.headers.get("X-Sources", "").split(",") if source]
                st.write_stream(response.iter_content(chunk_size=None, decode_unicode=True))

            elapsed = time.time() - start
            st.caption(f"⏱ answered in {elapsed:.1f}s")

            if sources:
                st.markdown("**Sources:** " + " ".join(f"`{source}`" for source in sources))
        except requests.RequestException as exc:
            st.error(f"Search failed: {exc}")