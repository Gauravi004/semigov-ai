import streamlit as st
from utils.config import GLOBAL_CSS

st.set_page_config(page_title="SemiGov AI", page_icon="⬡", layout="wide", initial_sidebar_state="expanded")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
st.markdown('<style>[data-testid="stSidebarNav"]{display:none!important;}</style>', unsafe_allow_html=True)

# Session defaults
for k,v in {"page":"home","language":"English","chat_history":[],"uploaded_chunks":[],"pdf_names":[]}.items():
    if k not in st.session_state: st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:20px 0 14px 0;text-align:center;">
        <div style="font-size:2.2rem;margin-bottom:2px;">⬡</div>
        <div style="font-size:1.35rem;font-weight:800;">SemiGov AI</div>
        <div style="font-size:0.75rem;color:var(--dim);margin-top:4px;line-height:1.4;">Taiwan Semiconductor<br>Governance Platform</div>
        <div style="margin-top:12px;"><span class="badge badge-green">● System Online</span></div>
    </div><hr class="divider">""", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Language</div>', unsafe_allow_html=True)
    opts = ["English", "Mandarin", "German"]
    prev_lang = st.session_state.language
    lang = st.selectbox("lang", opts, index=opts.index(prev_lang), label_visibility="collapsed")

    # If language changed — update session state and clear response cache
    if lang != prev_lang:
        st.session_state.language = lang
        # Clear all cached Gemini responses so new language is used
        keys_to_del = [k for k in st.session_state if k.startswith("_cache_")]
        for k in keys_to_del:
            del st.session_state[k]
        st.rerun()

    st.session_state.language = lang

    st.markdown('<hr class="divider"><div class="section-label">Navigation</div>', unsafe_allow_html=True)
    for key,icon,label in [
        ("home","🏠","Home"),
        ("assistant","💬","AI Policy Assistant"),
        ("compare","⚖️","Policy Comparator"),
        ("complaint","🚨","Complaint Center"),
        ("resource","🌊","Resource Optimizer"),
        ("supply","📈","Supply Chain Monitor"),
        ("report","📊","Smart Report Generator"),
    ]:
        if st.session_state.page == key:
            st.markdown(f'<div style="background:rgba(59,158,255,0.13);border:1px solid rgba(59,158,255,0.3);border-radius:8px;padding:10px 14px;margin:3px 0;color:#3b9eff;font-size:0.88rem;font-weight:600;">{icon} {label}</div>', unsafe_allow_html=True)
        else:
            if st.button(f"{icon} {label}", key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

    st.markdown('<hr class="divider"><div style="font-size:0.68rem;color:var(--dim);text-align:center;line-height:1.8;">v3.1 · RAG + Agentic AI<br>Gemini 2.0 Flash</div>', unsafe_allow_html=True)

# ── Router ────────────────────────────────────────────────────────────────────
page = st.session_state.page
if   page == "home":      from pages import home;      home.render()
elif page == "assistant": from pages import assistant; assistant.render()
elif page == "compare":   from pages import compare;   compare.render()
elif page == "complaint": from pages import complaint; complaint.render()
elif page == "resource":  from pages import resource;  resource.render()
elif page == "supply":    from pages import supply;    supply.render()
elif page == "report":    from pages import report;    report.render()
else: st.session_state.page = "home"; st.rerun()
