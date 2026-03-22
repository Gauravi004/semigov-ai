GROQ_API_KEY = "gsk_dfJ###############################"  
GROQ_MODEL   = "llama-3.3-70b-versatile"
GROQ_URL     = "https://api.groq.com/openai/v1/chat/completions"

LANG_MAP = {
    "English":  "Respond in English.",
    "Mandarin": "请用普通话（简体中文）回复。",
    "German":   "Bitte antworten Sie auf Deutsch.",
}

SYSTEM_PROMPT = """You are SemiGov AI — expert assistant for Taiwan semiconductor industry governance.
You have deep expertise in:
- Taiwan semiconductor policies, TSMC regulations, MOEA directives
- US CHIPS Act, EU Chips Act, Japan RAPIDUS, export controls
- Environmental compliance: water, energy, carbon targets
- Supply chain resilience, geopolitical risk (Taiwan Strait)
- Raw material costs: silicon, rare earths, specialty chemicals
- Rising energy prices impact on fabs
Be precise, cite real sources, and give detailed comprehensive answers."""

BUILTIN_KB = [
    "Taiwan semiconductor water: TSMC uses 60,000-70,000 tonnes/day. 2021 drought caused 11% industrial cuts. Water Act (水利法) regulations apply. TSMC targets 60% water recycling by 2025. UMC and GlobalWafers also have EPA mandated water reduction agreements.",
    "Taiwan export controls: Strategic High-Tech Commodities (SHTC) list governed by BOFT/MOEA under Foreign Trade Act. EUV/DUV lithography tools need export license. Aligns with Wassenaar Arrangement. NT$30M fines and criminal prosecution for violations under Article 17.",
    "US CHIPS Act 2022: $52.7B total allocation. $39B manufacturing incentives. 25% investment tax credit for equipment. 10-year China expansion guardrail for recipients. TSMC investing $65B in Arizona fabs at N4, N3, N2 nodes.",
    "Taiwan energy policy: Taipower supplies 15-20% power to semiconductor sector. Industrial tariff +17% April 2024. TSMC RE100 commitment by 2050. Carbon fee NT$300/tonne CO2 from 2024 rising to NT$1200 by 2030. 20GW offshore wind target by 2035.",
    "Supply chain risks: Taiwan produces 92% of world advanced logic chips. ASML EUV monopoly for sub-7nm. 6-month critical chemical inventory buffer post-2022. Geopolitical risk score 8.2/10. Bloomberg estimates $2.5T GDP impact from full blockade.",
    "MOEA policies 2024-25: 25% R&D tax credit under Statute for Industrial Innovation. NT$100B smart machinery program. Hsinchu/Taichung/Tainan cluster development. Gold Card for foreign semiconductor engineers. ESG reporting mandatory for TWSE-listed companies 2025.",
    "Cross-strait geopolitical risk: PLA military exercises increased frequency post-2022. TSMC diversifying to Arizona/Japan Kumamoto/Germany Dresden. US-Taiwan TIFA trade talks include semiconductor supply security provisions.",
    "Environmental compliance: PFC emissions from etching down 32% vs 2020 baseline. Zero Liquid Discharge mandatory for new fabs above 10,000 wafer starts/month. ISO 14001 required for fabs with 500+ employees. NT$20M EPA fines. Carbon disclosure mandatory from FSC 2023.",
    "Raw material costs 2024-2025: Silicon wafers +15-20% YoY. EUV photoresist (JSR, TOK, Shin-Etsu) +25% since 2022. Helium prices tripled since 2021. TSMC long-term contracts cover 70% of critical materials 18-24 months forward.",
    "Taiwan semiconductor labor: 320,000+ workers in sector. 15,000 annual engineer deficit projected through 2027. NT$5B talent program from MOEA-NSTC. 3,500+ Gold Card engineers recruited since 2021. Salaries up 30% since 2020.",
]

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:      #0a0f1e;
    --bg2:     #0d1526;
    --panel:   #111d35;
    --border:  #1e3a5f;
    --accent:  #3b9eff;
    --orange:  #ff7043;
    --green:   #00e676;
    --text:    #e2eaf5;
    --dim:     #6b8aaa;
    --red:     #ff5252;
}
html, body, [class*="css"], .main { background: var(--bg) !important; color: var(--text) !important; font-family: 'Inter', sans-serif !important; }
section[data-testid="stSidebar"] { background: var(--bg2) !important; border-right: 1px solid var(--border) !important; }
section[data-testid="stSidebar"] * { color: var(--text) !important; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
.stButton > button { background: transparent !important; border: 1px solid var(--border) !important; color: var(--text) !important; font-family: 'Inter', sans-serif !important; font-size: 0.88rem !important; border-radius: 8px !important; transition: all 0.18s !important; padding: 9px 16px !important; text-align: left !important; }
.stButton > button:hover { background: rgba(59,158,255,0.1) !important; border-color: var(--accent) !important; color: #fff !important; }
.stButton > button[kind="primary"] { background: var(--accent) !important; border-color: var(--accent) !important; color: #fff !important; font-weight: 600 !important; }
.stButton > button[kind="primary"]:hover { background: #2d8fe8 !important; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div { background: var(--panel) !important; border: 1px solid var(--border) !important; color: var(--text) !important; border-radius: 8px !important; font-family: 'Inter', sans-serif !important; font-size: 0.95rem !important; }
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 2px rgba(59,158,255,0.15) !important; }
.stTabs [data-baseweb="tab-list"] { background: var(--bg2) !important; border-radius: 10px; gap: 4px; padding: 4px; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--dim) !important; border-radius: 7px !important; border: none !important; font-family: 'Inter', sans-serif !important; font-size: 0.87rem !important; font-weight: 500 !important; }
.stTabs [aria-selected="true"] { background: rgba(59,158,255,0.14) !important; color: var(--accent) !important; }
[data-testid="metric-container"] { background: var(--panel) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; padding: 16px !important; }
.streamlit-expanderHeader { background: var(--panel) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; color: var(--text) !important; font-size: 0.88rem !important; }
.stRadio label { color: var(--text) !important; font-size: 0.9rem !important; }
[data-testid="stFileUploader"] { background: var(--panel) !important; border: 1px dashed var(--border) !important; border-radius: 8px !important; }
label { color: var(--dim) !important; font-size: 0.82rem !important; font-weight: 600 !important; letter-spacing: 0.5px !important; }
.section-label { font-size: 0.72rem; font-weight: 700; color: var(--dim); letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px; margin-top: 4px; }
.card { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 20px; margin: 8px 0; }
.card-blue { border-left: 3px solid var(--accent); }
.card-orange { border-left: 3px solid var(--orange); }
.card-green { border-left: 3px solid var(--green); }
.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.3px; }
.badge-blue { background:rgba(59,158,255,0.12); color:var(--accent); border:1px solid rgba(59,158,255,0.3); }
.badge-orange { background:rgba(255,112,67,0.12); color:var(--orange); border:1px solid rgba(255,112,67,0.3); }
.badge-green { background:rgba(0,230,118,0.12); color:var(--green); border:1px solid rgba(0,230,118,0.3); }
.badge-red { background:rgba(255,82,82,0.12); color:var(--red); border:1px solid rgba(255,82,82,0.3); }
.divider { border: none; height: 1px; background: linear-gradient(90deg, transparent, var(--border), transparent); margin: 20px 0; }
.alert-info { background: rgba(59,158,255,0.07); border: 1px solid rgba(59,158,255,0.25); border-radius: 8px; padding: 12px 16px; font-size: 0.88rem; margin: 8px 0; line-height: 1.5; }
.alert-warn { background: rgba(255,112,67,0.07); border: 1px solid rgba(255,112,67,0.25); border-radius: 8px; padding: 12px 16px; font-size: 0.88rem; margin: 8px 0; }
.user-bubble { background: rgba(59,158,255,0.08); border: 1px solid rgba(59,158,255,0.2); border-radius: 14px 14px 4px 14px; padding: 14px 18px; max-width: 76%; margin-left: auto; font-size: 0.95rem; line-height: 1.65; color: var(--text); }
.ai-bubble { background: var(--panel); border: 1px solid var(--border); border-left: 3px solid var(--accent); border-radius: 14px 14px 14px 4px; padding: 18px 22px; max-width: 92%; font-size: 0.95rem; line-height: 1.8; color: var(--text); }
.ai-label { font-size: 0.72rem; font-weight: 700; color: var(--accent); letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px; }
.user-label { font-size: 0.72rem; font-weight: 600; color: var(--dim); margin-bottom: 5px; text-align: right; }
.citation { background: rgba(59,158,255,0.04); border: 1px dashed rgba(59,158,255,0.2); border-radius: 6px; padding: 10px 14px; margin: 5px 0; font-size: 0.83rem; color: var(--dim); }
</style>
"""
