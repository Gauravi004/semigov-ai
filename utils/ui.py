import streamlit as st


def page_header(icon: str, title: str, subtitle: str):
    st.markdown(f"""
    <div style="padding:20px 0 16px 0;">
        <div style="font-size:0.7rem;font-weight:700;color:var(--dim);letter-spacing:2px;
                    text-transform:uppercase;margin-bottom:8px;">
            Taiwan Semiconductor Governance Platform
        </div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px;">
            <span style="font-size:2rem;">{icon}</span>
            <h2 style="margin:0;font-size:1.7rem;font-weight:800;">{title}</h2>
        </div>
        <div style="color:var(--dim);font-size:0.92rem;line-height:1.5;">{subtitle}</div>
    </div>
    <hr class="divider">
    """, unsafe_allow_html=True)


def show_citations(citations: list):
    if not citations:
        return
    with st.expander(f"📎 {len(citations)} Source(s)", expanded=False):
        for c in citations:
            url = c.get("url", "")
            link = f'<a href="{url}" target="_blank" style="color:var(--accent);">{url}</a>' if url else ""
            st.markdown(f"""
            <div class="citation">
                <strong style="color:var(--text);">{c.get("source","Source")}</strong><br>
                {link}<br>
                <span>{c.get("excerpt","")}</span>
            </div>""", unsafe_allow_html=True)


def show_agent_steps(steps: list):
    if not steps:
        return
    with st.expander(f"🔍 Agent reasoning ({len(steps)} steps)", expanded=False):
        for step in steps:
            st.markdown(f"""
            <div class="card" style="padding:12px 16px;margin:4px 0;font-size:0.85rem;">
                <strong style="color:var(--orange);">{step['step']}</strong><br>
                <span style="color:var(--dim);font-size:0.82rem;">{str(step['content'])[:500]}</span>
            </div>""", unsafe_allow_html=True)


def render_answer(answer: str):
    """Render AI answer with proper formatting."""
    # Convert markdown-like to HTML
    lines = answer.split('\n')
    html_parts = []
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            html_parts.append('<div style="height:8px;"></div>')
        elif line_stripped.startswith('## '):
            html_parts.append(f'<h4 style="color:var(--accent);margin:14px 0 6px 0;font-size:1rem;font-weight:700;">{line_stripped[3:]}</h4>')
        elif line_stripped.startswith('# '):
            html_parts.append(f'<h3 style="color:var(--accent);margin:16px 0 8px 0;font-size:1.1rem;font-weight:800;">{line_stripped[2:]}</h3>')
        elif line_stripped.startswith('**') and line_stripped.endswith('**'):
            html_parts.append(f'<p style="font-weight:700;color:var(--text);margin:6px 0;">{line_stripped[2:-2]}</p>')
        elif line_stripped.startswith('- ') or line_stripped.startswith('* '):
            html_parts.append(f'<div style="padding:3px 0 3px 16px;color:var(--text);font-size:0.95rem;">• {line_stripped[2:]}</div>')
        elif line_stripped.startswith('  - ') or line_stripped.startswith('  * '):
            html_parts.append(f'<div style="padding:2px 0 2px 32px;color:var(--dim);font-size:0.9rem;">◦ {line_stripped[4:]}</div>')
        else:
            # Inline bold
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line_stripped)
            formatted = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted)
            if formatted:
                html_parts.append(f'<p style="margin:5px 0;line-height:1.75;font-size:0.95rem;color:var(--text);">{formatted}</p>')

    return '\n'.join(html_parts)


import re
