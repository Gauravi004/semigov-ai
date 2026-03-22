import streamlit as st
from utils.ai import call_gemini
from utils.ui import page_header, show_citations, render_answer

PRESETS = {
    "Select a preset...": ("",""),
    "Taiwan vs US CHIPS Act": (
        "Taiwan Statute for Industrial Innovation — 25% R&D tax credit, land allocation priority, water/power guarantees for advanced fabs under MOEA",
        "US CHIPS and Science Act 2022 — $52.7B subsidies, 25% investment tax credit, 10-year China expansion restriction for recipients"
    ),
    "TSMC Water Policy vs Samsung": (
        "TSMC water management: 86% recycling rate target, rainwater harvesting, DI water recovery, drought contingency for all major fabs",
        "Samsung semiconductor: Zero Liquid Discharge goals, water intensity reduction targets, advanced purification at Korean fabs"
    ),
    "Taiwan Export Controls vs US EAR": (
        "Taiwan SHTC export control list — licensing for advanced semiconductor equipment to restricted destinations, BOFT/MOEA administered",
        "US Export Administration Regulations (EAR) — Entity List, Foreign Direct Product Rule, advanced chip export controls to China"
    ),
    "Taiwan ESG vs EU Chips Act ESG": (
        "Taiwan EPA regulations: water recycling mandates, carbon disclosure, ESG reporting for listed companies from 2023",
        "EU Chips Act 2023 sustainability: mandatory environmental impact assessment, supply chain due diligence, ESRS reporting"
    ),
    "Taiwan vs Japan Semiconductor Policy": (
        "Taiwan MOEA semiconductor cluster strategy: Hsinchu/Taichung/Tainan fabs, 25% R&D credit, water/power priority for advanced nodes",
        "Japan RAPIDUS program and TSMC Kumamoto: $13B government subsidy, 2nm fab by 2027, focus on advanced logic and power chips"
    ),
}

def render():
    lang = st.session_state.language
    page_header("⚖️","Policy Comparator","Compare any two semiconductor governance policies side-by-side with AI analysis.")

    st.markdown('<div class="section-label">Preset Comparisons — Click to Compare Instantly</div>', unsafe_allow_html=True)

    # Preset buttons — click = auto fill + auto submit
    preset_cols = st.columns(2)
    preset_list = [k for k in PRESETS if k != "Select a preset..."]
    for i, name in enumerate(preset_list):
        with preset_cols[i%2]:
            if st.button(f"⚡  {name}", key=f"preset_{i}", use_container_width=True):
                pa, pb = PRESETS[name]
                st.session_state["_cpa"] = pa
                st.session_state["_cpb"] = pb
                st.session_state["_cp_submit"] = True
                st.rerun()

    st.markdown('<hr class="divider"><div class="section-label">Or Enter Custom Policies</div>', unsafe_allow_html=True)

    pre_a = st.session_state.pop("_cpa","")
    pre_b = st.session_state.pop("_cpb","")
    auto_submit = st.session_state.pop("_cp_submit", False)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-label" style="color:var(--accent);">Policy A</div>', unsafe_allow_html=True)
        pa = st.text_area("pa", value=pre_a, height=140, placeholder="Describe Policy A...", label_visibility="collapsed")
    with col2:
        st.markdown('<div class="section-label" style="color:var(--orange);">Policy B</div>', unsafe_allow_html=True)
        pb = st.text_area("pb", value=pre_b, height=140, placeholder="Describe Policy B...", label_visibility="collapsed")

    manual = st.button("Compare Policies", use_container_width=True, type="primary")

    if manual or auto_submit:
        use_a = (pa or pre_a).strip()
        use_b = (pb or pre_b).strip()
        if use_a and use_b:
            with st.spinner("Comparing policies..."):
                prompt = f"""Compare these two semiconductor governance policies in detail:

POLICY A: {use_a}
POLICY B: {use_b}

Structure:
## Overview of Policy A
## Overview of Policy B
## Key Similarities
## Key Differences
## Strengths & Weaknesses of Each
## Verdict & Recommendation"""
                result = call_gemini(prompt, lang, "You are a senior semiconductor policy analyst.")

            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            ca,cvs,cb = st.columns([5,1,5])
            with ca:
                st.markdown('<div class="card card-blue" style="text-align:center;padding:14px;"><strong style="color:var(--accent);">Policy A</strong></div>', unsafe_allow_html=True)
            with cvs:
                st.markdown('<div style="text-align:center;padding-top:14px;font-size:1.3rem;font-weight:800;color:var(--dim);">VS</div>', unsafe_allow_html=True)
            with cb:
                st.markdown('<div class="card card-orange" style="text-align:center;padding:14px;"><strong style="color:var(--orange);">Policy B</strong></div>', unsafe_allow_html=True)

            st.markdown(f"""<div class="card card-blue" style="margin-top:12px;padding:24px;">
                {render_answer(result['answer'])}</div>""", unsafe_allow_html=True)
            show_citations(result.get("citations",[]))
        else:
            st.warning("Please fill in both policy fields.")
