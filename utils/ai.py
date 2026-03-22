import re, json, requests, smtplib, time, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from utils.config import LANG_MAP, SYSTEM_PROMPT, BUILTIN_KB

GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"


def _get_key() -> str:
    """Read GROQ_API_KEY directly from config.py file — bypasses import cache."""
    try:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.search(r'GROQ_API_KEY\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1).strip()
    except:
        pass
    return ""


def call_gemini(user_prompt: str, language: str = "English", system_extra: str = "") -> dict:
    """Main AI call — now uses Groq instead of Gemini."""
    key = _get_key()

    if not key or key == "YOUR_GROQ_KEY_HERE":
        return {"answer": "⚠️ API key missing. Open utils/config.py and set:\nGROQ_API_KEY = \"gsk_your_key_here\"", "citations": []}

    # Language ALWAYS from session_state — fixes all pages
    lang = st.session_state.get("language", "English")
    lang_instr = LANG_MAP.get(lang, "Respond in English.")

    system = f"{SYSTEM_PROMPT}\n\n{lang_instr}\n\n{system_extra}"
    system += "\n\nGive detailed comprehensive answers (minimum 300 words). Use clear sections and bullet points.\n\nAfter your answer add sources as:\n<citations>\n[{\"source\":\"Name\",\"url\":\"https://...\",\"excerpt\":\"brief description\"}]\n</citations>"

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user_prompt},
        ],
        "max_tokens": 2048,
        "temperature": 0.7,
    }

    for attempt in range(3):
        try:
            r = requests.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=60
            )

            if r.status_code == 429:
                if attempt < 2:
                    time.sleep(10)
                    continue
                return {"answer": "⚠️ Rate limit hit. Please wait a moment and try again.", "citations": []}

            if r.status_code == 401:
                return {"answer": "⚠️ Invalid Groq API key. Check your key in utils/config.py", "citations": []}

            if r.status_code != 200:
                return {"answer": f"⚠️ API Error {r.status_code}: {r.text[:200]}", "citations": []}

            raw = r.json()["choices"][0]["message"]["content"]

            citations = []
            match = re.search(r"<citations>(.*?)</citations>", raw, re.DOTALL)
            if match:
                try: citations = json.loads(match.group(1).strip())
                except: pass
                answer = raw[:match.start()].strip()
            else:
                answer = raw.strip()

            return {"answer": answer, "citations": citations}

        except requests.exceptions.Timeout:
            if attempt < 2: time.sleep(5); continue
            return {"answer": "⚠️ Request timed out. Please try again.", "citations": []}
        except Exception as e:
            if attempt < 2: time.sleep(5); continue
            return {"answer": f"⚠️ Error: {str(e)}", "citations": []}

    return {"answer": "⚠️ Request failed after retries.", "citations": []}


def rag_search(query: str) -> str:
    keywords = [w for w in query.lower().split() if len(w) > 3]
    all_docs = BUILTIN_KB + st.session_state.get("uploaded_chunks", [])
    scored = [(sum(1 for kw in keywords if kw in d.lower()), d) for d in all_docs]
    scored = [(s, d) for s, d in scored if s > 0]
    scored.sort(reverse=True)
    return "\n\n---\n\n".join(d for _, d in scored[:3])


def web_search(query: str) -> str:
    try:
        from duckduckgo_search import DDGS
        results = []
        with DDGS() as d:
            for r in d.text(query + " Taiwan semiconductor 2024 2025", max_results=3):
                results.append(f"**{r.get('title','')}**\n{r.get('body','')[:250]}")
        return "\n\n".join(results) if results else ""
    except:
        return ""


def run_agent(query: str, language: str = "English") -> dict:
    steps = []

    rag = rag_search(query)
    if rag:
        steps.append({"step": "Knowledge Base", "content": rag[:300] + "..."})

    web = web_search(query)
    if web:
        steps.append({"step": "Web Search", "content": web[:300] + "..."})

    context_parts = []
    if rag: context_parts.append("[Internal Knowledge Base]\n" + rag)
    if web: context_parts.append("[Live Web Results]\n" + web)

    full_prompt = query
    if context_parts:
        full_prompt = query + "\n\nUse this context:\n\n" + "\n\n---\n\n".join(context_parts)

    result = call_gemini(full_prompt)
    result["steps"] = steps
    result["tools_used"] = [s["step"] for s in steps]
    return result


def extract_pdf(pdf_file) -> list:
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_file)
        chunks = []
        for page in reader.pages:
            text = (page.extract_text() or "").strip()
            for i in range(0, len(text), 500):
                chunk = text[i:i+500].strip()
                if len(chunk) > 60:
                    chunks.append(chunk)
        return chunks
    except:
        return []


def send_email(to, subject, body, from_email, password) -> str:
    try:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to
        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(from_email, password)
            s.sendmail(from_email, to, msg.as_string())
        return "ok"
    except smtplib.SMTPAuthenticationError:
        return "auth_error"
    except Exception as e:
        return str(e)
