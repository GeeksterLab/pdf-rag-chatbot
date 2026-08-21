from pathlib import Path


import httpx
import streamlit as st
from pypdf import PdfReader

# ╔════════════════════════════════════════════════════════════╗
# ║ ⚙️ CONFIG
# ╚════════════════════════════════════════════════════════════╝

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

API_URL = "http://127.0.0.1:8003"
MEDICAL_QUESTION_ENDPOINT = f"{API_URL}/medicalquestion"
HEALTH_ENDPOINT = f"{API_URL}/health"

st.set_page_config(
    page_title="Medical RAG Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ╔════════════════════════════════════════════════════════════╗
# ║ 🎨 DARK MEDICAL AI THEME
# ╚════════════════════════════════════════════════════════════╝

st.markdown(
    """
    <style>
        :root {
            --bg: #020914;
            --bg-soft: #061321;
            --panel: rgba(7, 25, 42, 0.86);
            --panel-2: rgba(8, 32, 52, 0.78);
            --cyan: #19e7f7;
            --cyan-soft: #7af7ff;
            --blue: #168bff;
            --green: #64ff8f;
            --text: #edfaff;
            --muted: #8ea8ba;
            --border: rgba(25, 231, 247, 0.25);
            --border-strong: rgba(25, 231, 247, 0.55);
            --shadow: 0 0 25px rgba(25, 231, 247, 0.07);
        }

        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 85% 5%, rgba(0, 198, 255, 0.08), transparent 28%),
                radial-gradient(circle at 10% 90%, rgba(0, 102, 255, 0.07), transparent 30%),
                linear-gradient(145deg, #020914 0%, #03111d 48%, #020914 100%);
            color: var(--text);
        }

        [data-testid="stHeader"] {
            background: rgba(2, 9, 20, 0.70);
            backdrop-filter: blur(12px);
        }

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(4, 20, 35, 0.98), rgba(2, 12, 23, 0.98));
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.35rem;
        }

        .block-container {
            max-width: 1380px;
            padding-top: 1.4rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: #f4fdff !important;
        }

        p, label, .stMarkdown {
            color: var(--text);
        }

        /* ---------- Header ---------- */

        .hero {
            position: relative;
            overflow: hidden;
            border: 1px solid var(--border);
            background:
                linear-gradient(120deg, rgba(6, 27, 45, 0.95), rgba(3, 14, 27, 0.88));
            border-radius: 22px;
            padding: 1.35rem 1.55rem;
            box-shadow: var(--shadow);
            margin-bottom: 1rem;
        }

        .hero::after {
            content: "";
            position: absolute;
            right: -60px;
            top: -80px;
            width: 260px;
            height: 260px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(25, 231, 247, 0.12), transparent 68%);
            pointer-events: none;
        }

        .hero-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }

        .hero-brand {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .hero-icon {
            width: 62px;
            height: 62px;
            display: grid;
            place-items: center;
            border-radius: 18px;
            border: 1px solid rgba(25, 231, 247, 0.65);
            color: var(--cyan);
            font-size: 1.8rem;
            background: linear-gradient(145deg, rgba(0, 174, 255, 0.17), rgba(25, 231, 247, 0.05));
            box-shadow: 0 0 24px rgba(25, 231, 247, 0.16);
        }

        .hero-title {
            font-size: 1.65rem;
            line-height: 1.1;
            font-weight: 800;
            color: #ffffff;
        }

        .hero-subtitle {
            color: var(--muted);
            margin-top: 0.35rem;
            font-size: 0.93rem;
        }

        .online-badge,
        .offline-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            border-radius: 999px;
            padding: 0.5rem 0.85rem;
            font-size: 0.82rem;
            font-weight: 700;
            white-space: nowrap;
        }

        .online-badge {
            color: var(--green);
            border: 1px solid rgba(100, 255, 143, 0.35);
            background: rgba(39, 161, 80, 0.09);
        }

        .offline-badge {
            color: #ff9f9f;
            border: 1px solid rgba(255, 100, 100, 0.35);
            background: rgba(255, 80, 80, 0.08);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: currentColor;
            box-shadow: 0 0 10px currentColor;
        }

        /* ---------- Sidebar ---------- */

        .sidebar-brand {
            margin: 0.1rem 0 1.2rem 0;
        }

        .sidebar-brand-title {
            color: var(--cyan);
            font-weight: 800;
            letter-spacing: 0.02em;
            font-size: 1.05rem;
        }

        .sidebar-brand-sub {
            color: var(--muted);
            font-size: 0.78rem;
            margin-top: 0.2rem;
        }

        .sidebar-section {
            border: 1px solid var(--border);
            background: rgba(5, 24, 40, 0.76);
            border-radius: 16px;
            padding: 0.85rem 0.9rem;
            margin-bottom: 0.85rem;
            box-shadow: var(--shadow);
        }

        .sidebar-title {
            color: var(--cyan);
            font-size: 0.73rem;
            font-weight: 800;
            letter-spacing: 0.10em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
        }

        .status-row,
        .config-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.7rem;
            padding: 0.38rem 0;
            color: #cfe8f3;
            font-size: 0.82rem;
        }

        .status-value {
            color: var(--green);
            font-weight: 700;
        }

        .config-value {
            color: #ffffff;
            font-weight: 700;
            text-align: right;
        }

        /* ---------- Tabs ---------- */

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.4rem;
            padding: 0.35rem;
            border: 1px solid var(--border);
            border-radius: 14px;
            background: rgba(4, 18, 31, 0.72);
        }

        .stTabs [data-baseweb="tab"] {
            height: 44px;
            border-radius: 10px;
            padding: 0 1.2rem;
            color: var(--muted);
        }

        .stTabs [aria-selected="true"] {
            color: var(--cyan) !important;
            background: linear-gradient(90deg, rgba(14, 124, 225, 0.20), rgba(25, 231, 247, 0.09)) !important;
            border: 1px solid rgba(25, 231, 247, 0.22);
        }

        /* ---------- Chat ---------- */

        [data-testid="stChatMessage"] {
            border: 1px solid rgba(25, 231, 247, 0.15);
            border-radius: 16px;
            padding: 0.7rem 0.85rem;
            background: rgba(5, 24, 40, 0.74);
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
            margin-bottom: 0.7rem;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: linear-gradient(135deg, rgba(14, 73, 137, 0.44), rgba(6, 36, 65, 0.72));
            border-color: rgba(22, 139, 255, 0.28);
        }

        [data-testid="stChatInput"] {
            border: 1px solid var(--border-strong);
            border-radius: 15px;
            background: rgba(5, 24, 40, 0.92);
            box-shadow: 0 0 22px rgba(25, 231, 247, 0.06);
        }

        .source-box {
            border: 1px solid rgba(25, 231, 247, 0.22);
            background: rgba(2, 15, 27, 0.70);
            border-radius: 13px;
            padding: 0.75rem 0.85rem;
            margin-top: 0.75rem;
        }

        .source-title {
            color: var(--cyan-soft);
            font-size: 0.79rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.55rem;
        }

        .source-chip {
            display: inline-block;
            margin: 0.15rem 0.25rem 0.15rem 0;
            padding: 0.32rem 0.6rem;
            border-radius: 999px;
            color: var(--cyan-soft);
            background: rgba(25, 231, 247, 0.08);
            border: 1px solid rgba(25, 231, 247, 0.38);
            font-size: 0.78rem;
            box-shadow: inset 0 0 12px rgba(25, 231, 247, 0.04);
        }

        /* ---------- Metrics / cards ---------- */

        [data-testid="stMetric"] {
            border: 1px solid var(--border);
            background:
                linear-gradient(145deg, rgba(7, 29, 48, 0.88), rgba(4, 19, 33, 0.88));
            border-radius: 16px;
            padding: 0.95rem 1rem;
            box-shadow: var(--shadow);
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        [data-testid="stMetricValue"] {
            color: var(--cyan);
        }

        .section-card {
            border: 1px solid var(--border);
            border-radius: 17px;
            background: rgba(5, 23, 39, 0.73);
            padding: 1rem 1.05rem;
            box-shadow: var(--shadow);
            margin-top: 0.75rem;
        }

        .section-heading {
            font-weight: 800;
            color: #f4fdff;
            margin-bottom: 0.2rem;
        }

        .section-caption {
            color: var(--muted);
            font-size: 0.84rem;
            margin-bottom: 0.75rem;
        }

        .kb-card {
            border: 1px solid var(--border);
            background: linear-gradient(145deg, rgba(7, 30, 49, 0.82), rgba(3, 17, 29, 0.82));
            border-radius: 15px;
            padding: 0.95rem;
            min-height: 110px;
            box-shadow: var(--shadow);
        }

        .kb-icon {
            color: var(--cyan);
            font-size: 1.05rem;
            margin-bottom: 0.45rem;
        }

        .kb-label {
            font-size: 0.72rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.07em;
        }

        .kb-value {
            color: #ffffff;
            font-size: 1.02rem;
            font-weight: 800;
            margin-top: 0.35rem;
            word-break: break-word;
        }

        /* ---------- Dataframe ---------- */

        [data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 14px;
            overflow: hidden;
            background: rgba(4, 18, 31, 0.78);
        }

        /* ---------- Buttons ---------- */

        .stButton > button {
            border-radius: 10px;
            border: 1px solid rgba(25, 231, 247, 0.32);
            background: rgba(25, 231, 247, 0.07);
            color: var(--cyan-soft);
            font-weight: 700;
        }

        .stButton > button:hover {
            border-color: var(--cyan);
            color: #ffffff;
            box-shadow: 0 0 16px rgba(25, 231, 247, 0.10);
        }

        [data-testid="stAlert"] {
            border-radius: 12px;
            border: 1px solid var(--border);
            background: rgba(5, 24, 40, 0.82);
        }

        hr {
            border-color: rgba(25, 231, 247, 0.15) !important;
        }

        @media (max-width: 850px) {
            .hero-row {
                align-items: flex-start;
                flex-direction: column;
            }

            .hero-title {
                font-size: 1.35rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ╔════════════════════════════════════════════════════════════╗
# ║ 🧰 HELPERS
# ╚════════════════════════════════════════════════════════════╝


def get_api_status() -> bool:
    """Return True when the FastAPI backend is reachable."""
    try:
        response = httpx.get(HEALTH_ENDPOINT, timeout=3.0)
        return response.status_code == 200
    except httpx.HTTPError:
        return False


def get_pdf_info() -> list[dict]:
    """Read PDF metadata directly from the local data directory."""
    pdf_files = sorted(DATA_DIR.glob("*.pdf"))
    documents = []

    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
            page_count = len(reader.pages)
            status = "Indexed"
        except Exception:
            page_count = 0
            status = "Unreadable"

        documents.append(
            {
                "Document": pdf_path.stem,
                "Pages": page_count,
                "Type": pdf_path.suffix.replace(".", "").upper(),
                "Status": status,
            }
        )

    return documents


def format_sources(sources: list[str], pages: list[int]) -> dict[str, list[int]]:
    """Group retrieved pages by document name for a cleaner UI."""
    grouped: dict[str, list[int]] = {}

    for source, page in zip(sources, pages):
        # Path handles the file path, and .stem returns only the filename
        # without the directory or extension.
        document_name = Path(source).stem if source else "Unknown source"
        grouped.setdefault(document_name, [])

        if page not in grouped[document_name]:
            grouped[document_name].append(page)

    for document_name in grouped:
        grouped[document_name] = sorted(grouped[document_name])

    return grouped


def ask_medical_api(question: str) -> dict:
    """Send the user's question to the FastAPI RAG endpoint."""
    response = httpx.post(
        MEDICAL_QUESTION_ENDPOINT,
        json={"text": question},
        timeout=60.0,
    )
    response.raise_for_status()
    return response.json()


def display_sources(sources: dict[str, list[int]]) -> None:
    """Render retrieved documents and pages as neon source chips."""
    if not sources:
        return

    chips = []
    for document, pages in sources.items():
        if pages:
            chips.extend(
                f'<span class="source-chip">▣ {document} · p.{page}</span>'
                for page in pages
            )
        else:
            chips.append(f'<span class="source-chip">▣ {document}</span>')

    st.markdown(
        f"""
        <div class="source-box">
            <div class="source-title">Retrieved sources</div>
            {"".join(chips)}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ╔════════════════════════════════════════════════════════════╗
# ║ 💾 SESSION STATE
# ╚════════════════════════════════════════════════════════════╝

if "messages" not in st.session_state:
    st.session_state.messages = []


# ╔════════════════════════════════════════════════════════════╗
# ║ 🔌 STATUS + DOCUMENT DATA
# ╚════════════════════════════════════════════════════════════╝

api_online = get_api_status()
pdf_info = get_pdf_info()
file_count = len(pdf_info)
total_pages = sum(document["Pages"] for document in pdf_info)


# ╔════════════════════════════════════════════════════════════╗
# ║ 🧬 SIDEBAR
# ╚════════════════════════════════════════════════════════════╝

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">⌁ MEDICAL RAG</div>
            <div class="sidebar-brand-sub">Document-grounded clinical AI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    api_state = "Online" if api_online else "Offline"
    api_state_class = "status-value" if api_online else ""

    st.markdown(
        f"""
        <div class="sidebar-section">
            <div class="sidebar-title">System status</div>
            <div class="status-row">
                <span>◉ FastAPI</span>
                <span class="{api_state_class}">{api_state}</span>
            </div>
            <div class="status-row">
                <span>◇ Vector DB</span>
                <span class="status-value">Pinecone</span>
            </div>
            <div class="status-row">
                <span>✦ LLM</span>
                <span class="status-value">OpenAI</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-section">
            <div class="sidebar-title">RAG configuration</div>
            <div class="config-row"><span>Embedding</span><span class="config-value">all-MiniLM-L6-v2</span></div>
            <div class="config-row"><span>Chunk size</span><span class="config-value">500</span></div>
            <div class="config-row"><span>Overlap</span><span class="config-value">30</span></div>
            <div class="config-row"><span>Top-k</span><span class="config-value">3</span></div>
            <div class="config-row"><span>Similarity</span><span class="config-value">cosine</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="sidebar-section">
            <div class="sidebar-title">Knowledge base</div>
            <div class="config-row"><span>Documents</span><span class="config-value">{file_count}</span></div>
            <div class="config-row"><span>PDF pages</span><span class="config-value">{total_pages}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ╔════════════════════════════════════════════════════════════╗
# ║ 🩺 HEADER
# ╚════════════════════════════════════════════════════════════╝

status_html = (
    '<span class="online-badge"><span class="status-dot"></span>API Online</span>'
    if api_online
    else '<span class="offline-badge"><span class="status-dot"></span>API Offline</span>'
)

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-row">
            <div class="hero-brand">
                <div class="hero-icon">♡✚</div>
                <div>
                    <div class="hero-title">Medical RAG Assistant</div>
                    <div class="hero-subtitle">
                        Document-grounded clinical AI · Evidence retrieved from the indexed knowledge base
                    </div>
                </div>
            </div>
            {status_html}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not api_online:
    st.warning(
        "The FastAPI backend is offline. Start it with "
        "`uv run uvicorn api.app:app --port 8003 --reload`."
    )


# ╔════════════════════════════════════════════════════════════╗
# ║ 📑 TABS
# ╚════════════════════════════════════════════════════════════╝

chat_tab, knowledge_tab = st.tabs(["💬  Chatbot", "📚  Knowledge Base"])


# ╔════════════════════════════════════════════════════════════╗
# ║ 💬 CHATBOT
# ╚════════════════════════════════════════════════════════════╝

with chat_tab:
    title_col, clear_col = st.columns([6, 1])

    with title_col:
        st.markdown(
            """
            <div class="section-card">
                <div class="section-heading">Ask the medical knowledge base</div>
                <div class="section-caption">
                    Responses are constrained to the retrieved document context.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with clear_col:
        st.write("")
        if st.button("Clear chat", width="stretch"):
            st.session_state.messages = []
            st.rerun()

    if not st.session_state.messages:
        st.info(
            "Try **What is acne?** The assistant will retrieve evidence from the indexed PDF before answering."
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant":
                display_sources(message.get("sources", {}))

    question = st.chat_input(
        "Ask a medical question...",
        disabled=not api_online,
    )

    if question:
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving medical evidence..."):
                try:
                    result = ask_medical_api(question)

                    answer = result.get(
                        "answer",
                        "The API returned no answer.",
                    )

                    grouped_sources = format_sources(
                        result.get("source", []),
                        result.get("pages", []),
                    )

                    st.markdown(answer)
                    display_sources(grouped_sources)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": grouped_sources,
                        }
                    )

                except httpx.HTTPStatusError as exc:
                    st.error(
                        f"The API returned HTTP {exc.response.status_code}. "
                        "Check the FastAPI terminal for the traceback."
                    )

                except httpx.HTTPError:
                    st.error("Unable to reach the FastAPI backend on port 8003.")


# ╔════════════════════════════════════════════════════════════╗
# ║ 📚 KNOWLEDGE BASE
# ╚════════════════════════════════════════════════════════════╝

with knowledge_tab:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-heading">Knowledge Base Overview</div>
            <div class="section-caption">
                These values are read directly from the PDF files currently present in the project's data directory.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    with metric_1:
        st.metric("Documents", file_count)

    with metric_2:
        st.metric("Total pages", total_pages)

    with metric_3:
        st.metric("File type", "PDF" if file_count else "—")

    with metric_4:
        st.metric("Vector DB", "Pinecone")

    st.markdown("### Indexed documents")

    if pdf_info:
        st.dataframe(
            pdf_info,
            width="stretch",
            hide_index=True,
        )
    else:
        st.warning(f"No PDF files found in `{DATA_DIR}`.")

    st.markdown("### RAG configuration")

    cfg_1, cfg_2, cfg_3, cfg_4 = st.columns(4)

    cards = [
        ("◈", "Embedding model", "all-MiniLM-L6-v2"),
        ("▦", "Chunk size", "500"),
        ("≋", "Chunk overlap", "30"),
        ("⌕", "Retrieval", "Similarity · top-k 3"),
    ]

    for column, (icon, label, value) in zip(
        [cfg_1, cfg_2, cfg_3, cfg_4],
        cards,
    ):
        with column:
            st.markdown(
                f"""
                <div class="kb-card">
                    <div class="kb-icon">{icon}</div>
                    <div class="kb-label">{label}</div>
                    <div class="kb-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.caption(
        "Document counts and page totals are calculated from the local `data/` directory, "
        "not hardcoded values."
    )
