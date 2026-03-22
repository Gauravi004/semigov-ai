import streamlit as st

def nav_to(page):
    st.session_state.page = page
    st.rerun()

def render():
    st.markdown("""
    <div style="text-align:center;padding:40px 0 28px 0;">
        <div style="font-size:0.75rem;font-weight:700;color:var(--dim);letter-spacing:3px;text-transform:uppercase;margin-bottom:12px;">
            Taiwan Semiconductor Governance Intelligence
        </div>
        <div style="font-size:3.2rem;font-weight:900;letter-spacing:-1px;margin-bottom:10px;line-height:1.1;">
            Semi<span style="color:#3b9eff;">Gov</span> <span style="color:#3b9eff;">AI</span>
        </div>
        <div style="font-size:1.05rem;color:var(--dim);max-width:580px;margin:0 auto 22px auto;line-height:1.6;">
            AI-powered governance intelligence for Taiwan's semiconductor ecosystem.
        </div>
        <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;">
            <span class="badge badge-blue">Multilingual</span>
            <span class="badge badge-blue">Agentic AI + RAG</span>
            <span class="badge badge-green">Live Web Search</span>
            <span class="badge badge-orange">PDF Upload</span>
        </div>
    </div>
    <hr class="divider">
    """, unsafe_allow_html=True)

    k1,k2,k3,k4 = st.columns(4)
    with k1: st.metric("Policies Indexed","2,847","+12 this week")
    with k2: st.metric("Active Complaints","134","-8 resolved")
    with k3: st.metric("Water Risk","HIGH","Drought alert")
    with k4: st.metric("Supply Chain Index","67.4","-2.1 MoM")

    st.markdown('<hr class="divider"><div class="section-label">Platform Modules — Click to Open</div>', unsafe_allow_html=True)
    st.markdown("")

    # Row 1
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="card card-blue" style="cursor:pointer;">
            <div style="font-size:1.8rem;margin-bottom:10px;">💬</div>
            <div style="font-size:1.05rem;font-weight:700;margin-bottom:6px;">AI Policy Assistant</div>
            <div style="font-size:0.88rem;color:var(--dim);line-height:1.55;margin-bottom:12px;">
                Ask any semiconductor governance question in English, Mandarin, or German. Agentic AI with RAG and live web search.</div>
            <span class="badge badge-blue">Multilingual</span>
            <span class="badge badge-blue" style="margin-left:6px;">RAG + Web</span>
        </div>""", unsafe_allow_html=True)
        if st.button("Open AI Policy Assistant →", key="hbtn_assistant", use_container_width=True):
            nav_to("assistant")

    with c2:
        st.markdown("""<div class="card card-green" style="cursor:pointer;">
            <div style="font-size:1.8rem;margin-bottom:10px;">⚖️</div>
            <div style="font-size:1.05rem;font-weight:700;margin-bottom:6px;">Policy Comparator</div>
            <div style="font-size:0.88rem;color:var(--dim);line-height:1.55;margin-bottom:12px;">
                Compare policies side-by-side — Taiwan vs US CHIPS Act, EU Chips Act, Japan strategies.</div>
            <span class="badge badge-green">Compare</span>
            <span class="badge badge-green" style="margin-left:6px;">Analyze</span>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Policy Comparator →", key="hbtn_compare", use_container_width=True):
            nav_to("compare")

    with c3:
        st.markdown("""<div class="card card-orange" style="cursor:pointer;">
            <div style="font-size:1.8rem;margin-bottom:10px;">🚨</div>
            <div style="font-size:1.05rem;font-weight:700;margin-bottom:6px;">Complaint Center</div>
            <div style="font-size:0.88rem;color:var(--dim);line-height:1.55;margin-bottom:12px;">
                AI categorizes complaints, suggests solutions, drafts formal letters, and sends emails.</div>
            <span class="badge badge-orange">Auto-Draft</span>
            <span class="badge badge-orange" style="margin-left:6px;">Email</span>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Complaint Center →", key="hbtn_complaint", use_container_width=True):
            nav_to("complaint")

    st.markdown("")
    # Row 2
    c4,c5,c6 = st.columns(3)
    with c4:
        st.markdown("""<div class="card card-orange" style="cursor:pointer;">
            <div style="font-size:1.8rem;margin-bottom:10px;">🌊</div>
            <div style="font-size:1.05rem;font-weight:700;margin-bottom:6px;">Resource Optimizer</div>
            <div style="font-size:0.88rem;color:var(--dim);line-height:1.55;margin-bottom:12px;">
                Water conservation, energy efficiency, and sustainability guidance for Taiwan fabs.</div>
            <span class="badge badge-orange">Water</span>
            <span class="badge badge-orange" style="margin-left:6px;">Energy</span>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Resource Optimizer →", key="hbtn_resource", use_container_width=True):
            nav_to("resource")

    with c5:
        st.markdown("""<div class="card card-blue" style="cursor:pointer;">
            <div style="font-size:1.8rem;margin-bottom:10px;">📊</div>
            <div style="font-size:1.05rem;font-weight:700;margin-bottom:6px;">Smart Report Generator</div>
            <div style="font-size:0.88rem;color:var(--dim);line-height:1.55;margin-bottom:12px;">
                Query-driven reports with executive summaries, risk matrices, and PDF export.</div>
            <span class="badge badge-blue">PDF Export</span>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Report Generator →", key="hbtn_report", use_container_width=True):
            nav_to("report")

    with c6:
        st.markdown("""<div class="card card-green" style="cursor:pointer;">
            <div style="font-size:1.8rem;margin-bottom:10px;">📈</div>
            <div style="font-size:1.05rem;font-weight:700;margin-bottom:6px;">Supply Chain Monitor</div>
            <div style="font-size:0.88rem;color:var(--dim);line-height:1.55;margin-bottom:12px;">
                Rising costs, raw material risks, and geopolitical risk analysis with live data.</div>
            <span class="badge badge-green">Geopolitical</span>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Supply Chain Monitor →", key="hbtn_supply", use_container_width=True):
            nav_to("supply")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-label">Active Alerts</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="alert-warn">⚠️ <strong>Water Shortage</strong> — Central Taiwan reservoir at 38%. Fab water restrictions in effect. <span class="badge badge-orange">High</span></div>
        <div class="alert-warn">⚠️ <strong>Energy Price Surge</strong> — Industrial tariff +18% Q1 2025. <span class="badge badge-orange">Medium</span></div>
        <div class="alert-info">ℹ️ <strong>Policy Update</strong> — MOEA released new ESG guidelines Feb 2025. <span class="badge badge-blue">Info</span></div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="section-label">Taiwan Semiconductor Snapshot</div>', unsafe_allow_html=True)
        for k,v in [("Global Market Share (Logic)","92%"),("Advanced Node (<7nm)","100%"),
                    ("Annual Water Consumption","156M tonnes"),("Energy as % of OPEX","15–20%"),
                    ("Geopolitical Risk Score","8.2 / 10"),("Export Control Categories","23")]:
            st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;
                padding:10px 12px;border-bottom:1px solid var(--border);font-size:0.88rem;">
                <span style="color:var(--dim);">{k}</span>
                <span style="color:var(--accent);font-weight:700;">{v}</span>
            </div>""", unsafe_allow_html=True)
