import streamlit as st, re, random, string
from utils.ai import run_agent, call_gemini, send_email
from utils.ui import page_header, show_citations, show_agent_steps, render_answer

EXAMPLES = [
    "Our Tainan fab faces water allocation cuts due to drought with no advance notice from the water authority.",
    "A supplier delayed photolithography chemicals by 6 weeks causing production line stoppages.",
    "Former employee took our proprietary process recipes to a competitor in mainland China.",
    "Energy bills increased 22% this quarter due to TPC tariff changes not communicated to us.",
    "Our fab received an EPA violation notice for exceeding PFC emission limits without prior warning.",
    "Critical EUV lithography tool shipment blocked by new export control regulation with no alternative supplier.",
]
AUTHORITIES = {
    "Taiwan EPA (Environmental)":     "epq@epa.gov.tw",
    "MOEA — Bureau of Foreign Trade": "boft@boft.gov.tw",
    "Water Resources Agency":         "wra@wra.gov.tw",
    "Fair Trade Commission":          "ftc@ftc.gov.tw",
    "Ministry of Labor":              "mol@mol.gov.tw",
    "Custom":                         "",
}

def render():
    lang = st.session_state.language
    page_header("🚨","Complaint Center","AI categorizes, analyzes root cause, suggests solutions, auto-drafts formal letters, and sends emails.")

    st.markdown('<div class="section-label">Example Complaints — Click to Analyze Instantly</div>', unsafe_allow_html=True)
    ex_cols = st.columns(2)
    for i,ex in enumerate(EXAMPLES):
        with ex_cols[i%2]:
            if st.button(f"📄  {ex[:70]}…", key=f"ex{i}", use_container_width=True):
                st.session_state["_cp"] = ex
                st.session_state["_cp_submit"] = True
                st.rerun()

    st.markdown('<hr class="divider"><div class="section-label">Describe Your Complaint</div>', unsafe_allow_html=True)
    prefill     = st.session_state.pop("_cp","")
    auto_submit = st.session_state.pop("_cp_submit", False)

    complaint = st.text_area("c", value=prefill, height=130,
                             placeholder="What happened? When? Who is involved? What is the impact?",
                             label_visibility="collapsed")
    c1,c2 = st.columns([1,3])
    with c1: manual = st.button("Analyze Complaint", use_container_width=True, type="primary")
    with c2: use_agent = st.checkbox("Agentic AI (searches regulations)", value=True)

    if manual or auto_submit:
        q = (complaint or prefill).strip()
        if not q:
            st.warning("Please describe your complaint.")
            return

        prompt = f"""Analyze this semiconductor industry complaint:
COMPLAINT: {q}

Provide:
1. CATEGORY: (Environmental / Supply Delay / IP Infringement / Labor / Regulatory / Export Control / Energy / Quality)
2. SEVERITY: (Low / Medium / High / Critical)
3. ROOT CAUSE ANALYSIS: Detailed analysis
4. SUGGESTED SOLUTIONS: 4-5 specific actionable steps
5. RELEVANT REGULATIONS: Which Taiwan laws apply

Then write a complete formal complaint letter:
---DRAFT START---
[formal complaint letter]
---DRAFT END---"""

        with st.spinner("Analyzing complaint..."):
            result = run_agent(prompt, lang) if use_agent else {**call_gemini(prompt, lang), "steps":[]}

        raw     = result["answer"]
        draft_m = re.search(r"---DRAFT START---\s*(.*?)\s*---DRAFT END---", raw, re.DOTALL)
        draft   = draft_m.group(1).strip() if draft_m else ""
        analysis= raw[:draft_m.start()].strip() if draft_m else raw

        cat_m    = re.search(r"CATEGORY[:\s]+([\w/\s\-]+)", analysis, re.IGNORECASE)
        sev_m    = re.search(r"SEVERITY[:\s]+(Low|Medium|High|Critical)", analysis, re.IGNORECASE)
        category = cat_m.group(1).strip().rstrip('.') if cat_m else "Regulatory Issue"
        severity = sev_m.group(1).strip() if sev_m else "Medium"
        cid      = ''.join(random.choices(string.ascii_uppercase+string.digits, k=8))
        sev_badge= {"Low":"badge-green","Medium":"badge-blue","High":"badge-orange","Critical":"badge-red"}

        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        cc1,cc2,cc3 = st.columns(3)
        with cc1:
            st.markdown(f"""<div class="card" style="text-align:center;padding:16px;">
                <div class="section-label">Category</div>
                <div style="font-weight:700;color:var(--accent);font-size:0.95rem;margin-top:4px;">{category}</div>
            </div>""", unsafe_allow_html=True)
        with cc2:
            st.markdown(f"""<div class="card" style="text-align:center;padding:16px;">
                <div class="section-label">Severity</div>
                <div style="margin-top:6px;"><span class="badge {sev_badge.get(severity,'badge-blue')}">{severity}</span></div>
            </div>""", unsafe_allow_html=True)
        with cc3:
            st.markdown(f"""<div class="card" style="text-align:center;padding:16px;">
                <div class="section-label">Case ID</div>
                <div style="font-family:'JetBrains Mono',monospace;color:var(--green);font-size:1rem;margin-top:4px;">SGC-{cid}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("")
        t1,t2,t3 = st.tabs(["📋  Analysis & Solutions","📄  Formal Draft","📧  Send Email"])
        with t1:
            st.markdown(f"""<div class="card card-blue" style="padding:24px;">{render_answer(analysis)}</div>""", unsafe_allow_html=True)
            show_agent_steps(result.get("steps",[]))
            show_citations(result.get("citations",[]))
        with t2:
            if draft:
                st.markdown(f"""<div class="card card-green" style="padding:24px;font-family:'JetBrains Mono',monospace;
                    font-size:0.85rem;line-height:1.8;white-space:pre-wrap;">
                    {draft.replace('<','&lt;').replace('>','&gt;')}</div>""", unsafe_allow_html=True)
                st.download_button("⬇️ Download Draft", data=draft,
                                   file_name=f"complaint_SGC-{cid}.txt", mime="text/plain")
            else:
                st.info("Enable Agentic AI to auto-generate the formal draft.")
        with t3:
            st.markdown("""<div class="alert-info">Send via Gmail SMTP. Get App Password: Gmail → Settings → Security → 2-Step → App Passwords → Create</div>""", unsafe_allow_html=True)
            auth = st.selectbox("Authority", list(AUTHORITIES.keys()))
            to   = st.text_input("Recipient Email", value=AUTHORITIES[auth])
            subj = st.text_input("Subject", value=f"Formal Complaint — {category} [SGC-{cid}]")
            ea,ep = st.columns(2)
            with ea: frm = st.text_input("Your Gmail", placeholder="you@gmail.com")
            with ep: pwd = st.text_input("App Password", type="password", placeholder="xxxx xxxx xxxx xxxx")
            if st.button("Send Email", use_container_width=True, type="primary"):
                if not all([to,frm,pwd,subj]):
                    st.warning("Fill in all email fields.")
                else:
                    with st.spinner("Sending..."):
                        r = send_email(to, subj, draft or analysis, frm, pwd)
                    if r=="ok": st.success(f"✅ Email sent to {to}")
                    elif r=="auth_error": st.error("Gmail authentication failed. Check App Password.")
                    else: st.error(f"Failed: {r}")
