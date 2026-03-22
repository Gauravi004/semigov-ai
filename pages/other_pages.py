import streamlit as st, re, random, string, io
from datetime import datetime
from utils.ai import run_agent, call_gemini
from utils.ui import page_header, show_citations, show_agent_steps, render_answer


# ═══════════════════════════════════════════════════
# RESOURCE OPTIMIZER
# ═══════════════════════════════════════════════════
def render_resource():
    lang = st.session_state.language
    page_header("🌊","Resource Optimizer","Water conservation, energy efficiency, and sustainability guidance for Taiwan semiconductor fabs.")

    c1,c2,c3,c4,c5 = st.columns(5)
    for col,(lbl,val,sub,color) in zip([c1,c2,c3,c4,c5],[
        ("Water Stress","HIGH","Hsinchu + Tainan","var(--orange)"),
        ("Energy Trend","↑ +18%","Q1 2025","var(--orange)"),
        ("Water/Wafer","~10 L","12-inch node","var(--accent)"),
        ("PFC Target","-30%","vs 2020","var(--green)"),
        ("Renewable Mix","~15%","Taiwan","var(--accent)"),
    ]):
        with col:
            st.markdown(f"""<div class="card card-orange" style="text-align:center;padding:14px;">
                <div class="section-label">{lbl}</div>
                <div style="font-size:1.2rem;font-weight:800;color:{color};margin:4px 0;">{val}</div>
                <div style="font-size:0.72rem;color:var(--dim);">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider"><div class="section-label">Quick Topics — Click to Ask Instantly</div>', unsafe_allow_html=True)
    topics = [
        ("💧","Water Recycling","How to improve DI water recycling rates in Taiwan semiconductor fabs to meet Taiwan EPA targets?"),
        ("⚡","Energy Efficiency","What are the best practices to reduce energy consumption in semiconductor manufacturing cleanrooms?"),
        ("🌡️","Heat Recovery","How can semiconductor fabs recover and reuse heat generated from manufacturing processes to reduce energy costs?"),
        ("☀️","Renewable Energy","What renewable energy options are available for Taiwan semiconductor fabs and what is the ROI and implementation timeline?"),
        ("🏭","TSMC Sustainability","What is TSMC's detailed sustainability roadmap and how can smaller fabs align with similar ESG standards?"),
        ("💨","PFC Emissions","How to reduce perfluorocarbon (PFC) emissions from semiconductor etching processes in compliance with Taiwan EPA regulations?"),
    ]
    cc = st.columns(3)
    for i,(ico,lbl,q) in enumerate(topics):
        with cc[i%3]:
            if st.button(f"{ico}  {lbl}", key=f"rt{i}", use_container_width=True):
                st.session_state["_rq"] = q
                st.session_state["_rq_submit"] = True
                st.rerun()

    st.markdown('<hr class="divider"><div class="section-label">Your Resource Question</div>', unsafe_allow_html=True)
    prefill = st.session_state.pop("_rq","")
    auto_submit = st.session_state.pop("_rq_submit", False)

    rq = st.text_area("rq", value=prefill, height=110,
                      placeholder="Ask about water reduction, energy savings, emissions, sustainability compliance...",
                      label_visibility="collapsed")
    focus = st.radio("Focus Area", ["All Resources","Water","Energy","Emissions","Sustainability"], horizontal=True)
    manual = st.button("Get Guidance", use_container_width=True, type="primary")

    if manual or auto_submit:
        q = (rq or prefill).strip()
        if q:
            with st.spinner("Researching..."):
                result = run_agent(f"[Focus: {focus}] {q}", lang)
            st.markdown(f"""<div class="card card-orange" style="padding:24px;margin-top:12px;">
                {render_answer(result['answer'])}</div>""", unsafe_allow_html=True)
            show_agent_steps(result.get("steps",[]))
            show_citations(result.get("citations",[]))
        else:
            st.warning("Please enter a question.")


# ═══════════════════════════════════════════════════
# SUPPLY CHAIN MONITOR
# ═══════════════════════════════════════════════════
def render_supply():
    lang = st.session_state.language
    page_header("📈","Supply Chain Monitor","Rising energy costs, raw material risks, and geopolitical risk analysis.")

    st.markdown('<div class="section-label">Current Risk Indicators</div>', unsafe_allow_html=True)
    risks = [("Energy Price Risk",82,"#ff7043"),("Raw Material Supply",65,"#ff7043"),
             ("Geopolitical Risk",88,"#ff5252"),("Logistics Risk",54,"#ffd740"),
             ("Currency Volatility",47,"#ffd740"),("Labor Availability",38,"#00e676")]
    cc = st.columns(3)
    for i,(lbl,score,color) in enumerate(risks):
        with cc[i%3]:
            st.markdown(f"""<div class="card" style="padding:14px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:0.85rem;">
                    <span style="color:var(--dim);">{lbl}</span>
                    <span style="font-weight:700;color:{color};">{score}/100</span>
                </div>
                <div style="background:#0d1526;border-radius:4px;height:7px;">
                    <div style="background:{color};width:{score}%;height:7px;border-radius:4px;"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider"><div class="section-label">Scenario Analysis — Click to Analyze Instantly</div>', unsafe_allow_html=True)
    scenarios = [
        ("🔴","Energy Price Crisis","Analyze the impact of rising global LNG and electricity prices on Taiwan semiconductor fab operating costs and what mitigation strategies exist"),
        ("🟠","Raw Material Shortage","Assess the risks from silicon wafer, rare earth, and specialty chemical supply constraints and Taiwan's current exposure level"),
        ("🔴","Geopolitical Escalation","Analyze how cross-strait tension escalation scenarios would impact global semiconductor supply chains and contingency measures Taiwan fabs should take"),
        ("🟡","Supply Chain Fragility","Evaluate Taiwan's semiconductor supply chain single points of failure, concentration risks, and best diversification strategies"),
        ("🟠","US-China Trade War","How do US-China semiconductor export controls and trade restrictions impact Taiwan's fab operations and market access?"),
        ("🟡","Logistics Disruption","Assess impact of Taiwan Strait shipping disruptions on semiconductor equipment and chemical supply chains"),
    ]
    cc2 = st.columns(2)
    for i,(sev,lbl,q) in enumerate(scenarios):
        with cc2[i%2]:
            if st.button(f"{sev}  {lbl}", key=f"sc{i}", use_container_width=True):
                st.session_state["_sq"] = q
                st.session_state["_sq_submit"] = True
                st.rerun()

    st.markdown('<hr class="divider"><div class="section-label">Custom Supply Chain Query</div>', unsafe_allow_html=True)
    prefill = st.session_state.pop("_sq","")
    auto_submit = st.session_state.pop("_sq_submit", False)

    sq = st.text_area("sq", value=prefill, height=110,
                      placeholder="Ask about rising costs, raw materials, geopolitical risks, resilience strategies...",
                      label_visibility="collapsed")
    vmode = st.radio("Mode", ["Current Status","Risk Assessment","Comparative","Forecast"], horizontal=True)
    manual = st.button("Analyze", use_container_width=True, type="primary")

    if manual or auto_submit:
        q = (sq or prefill).strip()
        if q:
            with st.spinner("Running intelligence..."):
                result = run_agent(f"[Mode: {vmode}] {q}", lang)
            t1,t2 = st.tabs(["📊  Analysis","📎  Sources"])
            with t1:
                st.markdown(f"""<div class="card card-green" style="padding:24px;">
                    {render_answer(result['answer'])}</div>""", unsafe_allow_html=True)
                show_agent_steps(result.get("steps",[]))
            with t2:
                show_citations(result.get("citations",[]))
        else:
            st.warning("Please enter a query.")


# ═══════════════════════════════════════════════════
# SMART REPORT GENERATOR
# ═══════════════════════════════════════════════════
def render_report():
    lang = st.session_state.language
    page_header("📊","Smart Report Generator","Generate comprehensive governance reports with executive summaries, risk matrices, and PDF export.")

    TEMPLATES = {
        "Custom":"",
        "Taiwan Water Crisis Impact":"Impact of Taiwan's water shortage crisis on semiconductor manufacturing — current situation, affected fabs, mitigation strategies, policy response, and 12-month outlook",
        "Supply Chain Resilience":"Comprehensive assessment of Taiwan semiconductor supply chain resilience — vulnerabilities, geopolitical exposure, and diversification strategies",
        "Energy Cost Optimization":"Rising energy costs impact on Taiwan semiconductor manufacturers — cost drivers, efficiency strategies, renewable transition, and compliance roadmap",
        "Export Control Compliance":"Taiwan semiconductor export control compliance landscape — US EAR, Taiwan SHTC, EU regulations, and best practices for fabs",
        "ESG Governance Framework":"ESG governance framework for Taiwan semiconductor industry — water, energy, emissions, social responsibility, and reporting standards",
        "Geopolitical Risk Assessment":"Geopolitical risk for Taiwan's semiconductor industry — cross-strait scenarios, contingency planning, and strategic recommendations",
    }

    col1,col2 = st.columns([3,1])
    with col1:
        st.markdown('<div class="section-label">Template</div>', unsafe_allow_html=True)
        tmpl = st.selectbox("t", list(TEMPLATES.keys()), label_visibility="collapsed")
        st.markdown('<div class="section-label" style="margin-top:10px;">Report Topic</div>', unsafe_allow_html=True)
        rq   = st.text_area("rq", value=TEMPLATES[tmpl], height=120,
                             placeholder="Describe the report scope...", label_visibility="collapsed")
        rtitle = st.text_input("Report Title", value="Semiconductor Governance Report")
        rdepth = st.selectbox("Depth", ["Standard","Executive Brief","Deep Dive"])
    with col2:
        st.markdown("""<div class="card card-blue" style="height:100%;">
            <div class="section-label">Includes</div>
            <ul style="font-size:0.85rem;color:var(--dim);line-height:2.2;padding-left:16px;margin:8px 0;">
                <li>Executive Summary</li><li>Background</li><li>Key Findings</li>
                <li>Policy Analysis</li><li>Risk Assessment</li><li>Recommendations</li>
                <li>Roadmap</li><li>Conclusion</li>
            </ul>
            <span class="badge badge-blue">PDF Export</span>
        </div>""", unsafe_allow_html=True)

    if st.button("Generate Report", use_container_width=True, type="primary"):
        if not rq.strip():
            st.warning("Please enter a report topic.")
            return
        depth_note = {"Executive Brief":"Keep concise, 2-3 pages.","Deep Dive":"Be extremely detailed.","Standard":""}
        prompt = f"""Generate a comprehensive semiconductor governance report.
Title: {rtitle}
Topic: {rq}
{depth_note.get(rdepth,'')}

Use these sections:
# EXECUTIVE SUMMARY
# 1. BACKGROUND & CONTEXT
# 2. KEY FINDINGS
# 3. POLICY ANALYSIS
# 4. RISK ASSESSMENT
# 5. STRATEGIC RECOMMENDATIONS
# 6. IMPLEMENTATION ROADMAP
# 7. CONCLUSION"""

        with st.spinner("Generating report..."):
            result = call_gemini(prompt, lang, "You are a senior semiconductor governance policy analyst.")

        t1,t2,t3 = st.tabs(["📄  Preview","📎  Sources","⬇️  Export"])
        with t1:
            st.markdown(f"""<div class="card card-blue" style="padding:32px;">
                <div style="text-align:center;padding-bottom:20px;margin-bottom:20px;border-bottom:1px solid var(--border);">
                    <div style="font-size:0.7rem;color:var(--dim);letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">SemiGov AI · Confidential</div>
                    <div style="font-size:1.5rem;font-weight:800;">{rtitle}</div>
                    <div style="font-size:0.82rem;color:var(--dim);margin-top:6px;">{datetime.now().strftime('%B %d, %Y')}</div>
                </div>
                {render_answer(result['answer'])}
            </div>""", unsafe_allow_html=True)
        with t2:
            show_citations(result.get("citations",[]))
        with t3:
            txt = f"{rtitle}\n{'='*60}\n{datetime.now().strftime('%Y-%m-%d')}\n\n{result['answer']}"
            st.download_button("⬇️ Download .TXT", data=txt,
                               file_name=f"{rtitle.lower().replace(' ','_')}.txt", mime="text/plain", use_container_width=True)
            try:
                from reportlab.lib.pagesizes import A4
                from reportlab.lib.styles import ParagraphStyle
                from reportlab.lib.units import mm
                from reportlab.lib import colors
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
                from reportlab.lib.enums import TA_CENTER
                buf = io.BytesIO()
                doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=22*mm, rightMargin=22*mm, topMargin=20*mm, bottomMargin=20*mm)
                acc = colors.HexColor('#3b9eff'); dim = colors.HexColor('#6b8aaa')
                h1s = ParagraphStyle('H1',fontName='Helvetica-Bold',fontSize=14,textColor=acc,spaceAfter=6,spaceBefore=14)
                bdy = ParagraphStyle('Bd',fontName='Helvetica',fontSize=10,textColor=colors.HexColor('#1a1a2e'),spaceAfter=5,leading=15)
                mts = ParagraphStyle('Mt',fontName='Helvetica',fontSize=8,textColor=dim,spaceAfter=4,alignment=TA_CENTER)
                story = [Paragraph("⬡ SemiGov AI", ParagraphStyle('L',fontName='Helvetica-Bold',fontSize=9,textColor=acc,alignment=TA_CENTER)),
                         HRFlowable(width="100%",thickness=1,color=acc),Spacer(1,4),
                         Paragraph(rtitle, ParagraphStyle('Ti',fontName='Helvetica-Bold',fontSize=18,textColor=colors.HexColor('#1a1a2e'),alignment=TA_CENTER,spaceAfter=4)),
                         Paragraph(datetime.now().strftime('%B %d, %Y'),mts),
                         HRFlowable(width="100%",thickness=0.5,color=dim),Spacer(1,10)]
                for line in result['answer'].split('\n'):
                    line=line.strip()
                    if not line: story.append(Spacer(1,4))
                    elif line.startswith('# '): story.append(Paragraph(line[2:],h1s)); story.append(HRFlowable(width="100%",thickness=0.5,color=acc))
                    elif line.startswith('- ') or line.startswith('* '): story.append(Paragraph(f"• {line[2:]}",bdy))
                    else:
                        clean = re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',line)
                        story.append(Paragraph(clean,bdy))
                story += [Spacer(1,16),HRFlowable(width="100%",thickness=1,color=acc),Paragraph("Confidential · SemiGov AI",mts)]
                doc.build(story)
                st.download_button("⬇️ Download PDF", data=buf.getvalue(),
                                   file_name=f"{rtitle.lower().replace(' ','_')}.pdf", mime="application/pdf", use_container_width=True)
            except ImportError:
                st.info("Install reportlab for PDF: pip install reportlab")
