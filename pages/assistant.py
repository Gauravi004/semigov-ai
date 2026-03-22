import streamlit as st
from utils.ai import call_gemini, run_agent, extract_pdf
from utils.ui import page_header, show_citations, show_agent_steps, render_answer

SUGGESTIONS = {
    "English": [
        "What are Taiwan's current semiconductor water usage regulations and compliance requirements?",
        "Explain TSMC's ESG commitments and environmental compliance framework in detail",
        "What is Taiwan's policy on advanced chip export controls and what penalties apply?",
        "Analyze the impact of rising energy costs on Taiwan semiconductor fabs in 2024-2025",
    ],
    "Mandarin": [
        "台灣目前的半導體出口管制法規和合規要求是什麼？",
        "詳細說明台積電的ESG承諾和環境合規框架",
        "台灣水資源短缺對半導體製造的影響和緩解策略",
        "台灣能源價格上漲對晶圓廠運營成本的影響分析",
    ],
    "German": [
        "Was sind Taiwans aktuelle Halbleiter-Exportkontrollvorschriften und Compliance-Anforderungen?",
        "Erklären Sie TSMCs ESG-Verpflichtungen und Umwelt-Compliance-Rahmen im Detail",
        "Wie wirkt sich der Wassermangel in Taiwan auf die Halbleiterfertigung aus?",
        "Analyse der steigenden Energiekosten für taiwanische Halbleiterfabriken 2024-2025",
    ],
}


def render():
    lang = st.session_state.language
    page_header("💬", "AI Policy Assistant",
                "Ask any semiconductor governance question. Agentic AI with RAG knowledge base and live web search.")

    # ── Mode + PDF upload ─────────────────────────────────────────────────────
    col_mode, col_pdf = st.columns([1, 1])
    with col_mode:
        st.markdown('<div class="section-label">AI Mode</div>', unsafe_allow_html=True)
        mode = st.radio("mode", ["🤖 Agentic AI — RAG + Web Search", "⚡ Direct AI — Fast Response"],
                        label_visibility="collapsed")
        is_agentic = "Agentic" in mode
        cap_color = "#00e676" if is_agentic else "#ff7043"
        st.markdown(f"""<div style="font-size:0.8rem;color:{cap_color};margin-top:6px;font-weight:500;">
            {"● Knowledge Base + Web Search + Citations" if is_agentic else "● Direct Gemini Answer + Citations"}
        </div>""", unsafe_allow_html=True)

    with col_pdf:
        st.markdown('<div class="section-label">Upload PDF to Knowledge Base</div>', unsafe_allow_html=True)
        pdf = st.file_uploader("pdf", type=["pdf"], label_visibility="collapsed",
                               help="Upload policy documents, reports, or regulations to enhance AI answers")
        if pdf:
            if st.button("Index PDF", key="idx_pdf"):
                with st.spinner("Reading PDF..."):
                    chunks = extract_pdf(pdf)
                    if chunks:
                        st.session_state.uploaded_chunks.extend(chunks)
                        st.session_state.pdf_names.append(pdf.name)
                        st.success(f"✅ Added {len(chunks)} chunks from '{pdf.name}'")
                    else:
                        st.error("Could not extract text from PDF.")
        if st.session_state.pdf_names:
            st.markdown(f"""<div style="font-size:0.78rem;color:var(--green);margin-top:6px;font-weight:500;">
                ✅ Indexed: {', '.join(st.session_state.pdf_names)}</div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Suggested questions — click = auto fill + auto submit ─────────────────
    st.markdown('<div class="section-label">Suggested Questions — Click to Ask Instantly</div>',
                unsafe_allow_html=True)

    sugg = SUGGESTIONS.get(lang, SUGGESTIONS["English"])
    c1, c2 = st.columns(2)
    for i, s in enumerate(sugg):
        with (c1 if i % 2 == 0 else c2):
            if st.button(f"⚡  {s}", key=f"sugg_{i}", use_container_width=True):
                # Set query AND mark for immediate submission
                st.session_state["_query_text"]  = s
                st.session_state["_auto_submit"] = True
                st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ── Chat history ──────────────────────────────────────────────────────────
    if st.session_state.chat_history:
        st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)

        for entry in st.session_state.chat_history:
            # User bubble
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-end;margin:10px 0 6px 0;">
                <div class="user-bubble">
                    <div class="user-label">You</div>
                    {entry['query']}
                </div>
            </div>""", unsafe_allow_html=True)

            # Tools used
            if entry.get("tools_used"):
                badges = "".join([
                    f'<span class="badge badge-blue" style="margin-left:4px;">{t}</span>'
                    for t in entry["tools_used"]
                ])
                st.markdown(f'<div style="text-align:right;margin-bottom:6px;">{badges}</div>',
                            unsafe_allow_html=True)

            # AI answer — properly formatted
            formatted = render_answer(entry["answer"])
            st.markdown(f"""
            <div style="margin:4px 0 10px 0;">
                <div class="ai-bubble">
                    <div class="ai-label">⬡ SemiGov AI</div>
                    {formatted}
                </div>
            </div>""", unsafe_allow_html=True)

            show_agent_steps(entry.get("steps", []))
            show_citations(entry.get("citations", []))

        if st.button("🗑️  Clear conversation", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

    # ── Input area ────────────────────────────────────────────────────────────
    st.markdown('<hr class="divider"><div class="section-label">Your Question</div>',
                unsafe_allow_html=True)

    # Pre-fill from suggested question click
    prefill_val = st.session_state.pop("_query_text", "")
    auto_submit = st.session_state.pop("_auto_submit", False)

    query = st.text_area("q", value=prefill_val, height=110,
                         placeholder="Ask about Taiwan semiconductor policies, regulations, compliance, water, energy, supply chain...",
                         label_visibility="collapsed", key="chat_input")

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        manual_submit = st.button("Ask SemiGov AI", use_container_width=True, type="primary")
    with col_info:
        st.markdown(f"""
        <div style="padding-top:10px;font-size:0.82rem;color:var(--dim);">
            Language: <strong style="color:var(--accent);">{lang}</strong> ·
            Mode: <strong style="color:{'#00e676' if is_agentic else '#ff7043'};">
            {"Agentic AI" if is_agentic else "Direct AI"}</strong>
        </div>""", unsafe_allow_html=True)

    # Submit on button click OR auto-submit from suggested question
    should_submit = manual_submit or auto_submit

    if should_submit:
        submit_query = query.strip() or prefill_val.strip()
        if submit_query:
            with st.spinner("Thinking..." if not is_agentic else "Searching knowledge base and web..."):
                if is_agentic:
                    result = run_agent(submit_query, lang)
                else:
                    result = call_gemini(submit_query, lang)
                    result["steps"] = []
                    result["tools_used"] = []

            st.session_state.chat_history.append({
                "query":      submit_query,
                "answer":     result["answer"],
                "citations":  result.get("citations", []),
                "steps":      result.get("steps", []),
                "tools_used": result.get("tools_used", []),
            })
            st.rerun()
        else:
            st.warning("Please enter a question.")
