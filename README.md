# ⬡ SemiGov AI
### AI-Powered Semiconductor Governance Intelligence Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red?style=for-the-badge&logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-Enabled-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Multilingual · Agentic AI · RAG · Live Web Search · PDF Export**

</div>

---

## 🌏 Overview

Taiwan controls **92% of the world's advanced semiconductor manufacturing** — yet governance, compliance, and policy intelligence remain fragmented and inaccessible.

**SemiGov AI** bridges that gap.

Built as a full-stack AI governance assistant, SemiGov AI combines **Retrieval-Augmented Generation (RAG)**, **Agentic AI**, and **live web search** to deliver real-time semiconductor policy intelligence — in three languages, across six intelligent modules.

> *"The most advanced chips in the world deserve the most intelligent governance platform."*

---

## ✨ Features

| Module | Description |
|--------|-------------|
| 💬 **AI Policy Assistant** | Multilingual Q&A (EN / 中文 / DE) with RAG + live web search + citations |
| ⚖️ **Policy Comparator** | Side-by-side AI analysis — Taiwan vs US CHIPS Act, EU Chips Act, Japan RAPIDUS |
| 🚨 **Complaint Center** | Auto-categorize → root cause → solutions → formal draft → send email |
| 🌊 **Resource Optimizer** | Water conservation, energy efficiency, sustainability guidance for fabs |
| 📈 **Supply Chain Monitor** | Geopolitical risk, rising costs, raw material analysis with live data |
| 📊 **Smart Report Generator** | Full governance reports with risk matrices — export to PDF |

---

## 🧠 AI Architecture

```
User Query
    │
    ├──► RAG Search (Built-in Taiwan Semiconductor KB)
    │         └── 10 curated knowledge documents
    │              (water policy, export controls, CHIPS Act, ESG, supply chain...)
    │
    ├──► Live Web Search (DuckDuckGo — no API needed)
    │         └── Real-time news & policy updates
    │
    └──► Groq LLM (Llama 3.3 70B)
              └── Synthesizes RAG + Web → Structured answer + Citations
```

**Why Agentic?** The AI doesn't just answer — it *thinks*. It decides which tools to use, retrieves relevant context, and synthesizes a comprehensive response — all in one call.

---

## 🛠️ Tech Stack

- **Frontend & Backend** — Streamlit
- **LLM** — Groq API (Llama 3.3 70B) — free, fast, powerful
- **RAG** — Custom keyword-based retrieval over curated KB
- **Web Search** — DuckDuckGo Search (free, no API key)
- **PDF Generation** — ReportLab
- **Email** — Gmail SMTP
- **Languages** — English, 中文 (Mandarin), Deutsch (German)

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/Gauravi004/semigov-ai.git
cd semigov-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
```bash
# Copy the example config
cp utils/config_example.py utils/config.py
```
Open `utils/config.py` and add your **free** Groq API key:
```python
GROQ_API_KEY = "gsk_your_key_here"
```
Get your free key at 👉 [console.groq.com](https://console.groq.com)

### 4. Run the app
```bash
streamlit run app.py
```

Open `http://localhost:8501` 🎉

---

## 📁 Project Structure

```
semigov-ai/
│
├── app.py                    # Main entry point + sidebar + routing
│
├── pages/
│   ├── home.py               # Dashboard with KPIs and alerts
│   ├── assistant.py          # AI Policy Assistant (multilingual)
│   ├── compare.py            # Policy Comparator
│   ├── complaint.py          # Complaint Center + Email
│   ├── resource.py           # Resource Optimizer
│   ├── supply.py             # Supply Chain Monitor
│   ├── report.py             # Smart Report Generator
│   └── other_pages.py        # Shared page logic
│
├── utils/
│   ├── ai.py                 # Groq API + RAG + Web Search + Agent
│   ├── config.py             # API keys & configuration (gitignored)
│   ├── config_example.py     # Template for configuration
│   └── ui.py                 # Shared UI components
│
└── requirements.txt
```

---

## 🌐 Domain Knowledge

SemiGov AI is pre-loaded with curated knowledge on:

- 💧 Taiwan water regulations & TSMC conservation targets
- 🔒 Export controls — SHTC list, Wassenaar Arrangement, US EAR
- 🇺🇸 US CHIPS Act 2022 — subsidies, guardrails, impact on Taiwan
- ⚡ Energy policy — Taipower tariffs, carbon fees, RE100
- 🌏 Geopolitical risk — cross-strait tensions, supply chain resilience
- 🏭 ESG compliance — PFC emissions, water recycling, ISO 14001
- 📦 Raw material costs — silicon wafers, EUV photoresist, helium
- 👷 Labor market — talent shortage, Gold Card program, salary trends

---

## 📸 Screenshots

> *Coming soon — add screenshots of your running app here!*

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

<div align="center">

**Built with ❤️ for Taiwan's semiconductor ecosystem**

⬡ *SemiGov AI — Where Policy Meets Intelligence*

</div>
