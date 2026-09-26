import html
import re

import streamlit as st


def _clean(line: str) -> str:
    return re.sub(r"^#{1,6}\s+", "", line.strip()).replace("**", "").replace("__", "")


def _is_heading(line: str) -> bool:
    return len(line) < 100 and bool(
        re.match(r"^\d+(?:\.\d+)*[.)]?\s+\S", line)
        or re.match(r"^(?:section|article|clause)\s+[\w.-]+\b", line, re.I)
        or re.match(r"^[A-Z][A-Z\s&—–:,-]{5,}$", line)
    )


def document_html(title: str, text: str) -> str:
    blocks: list[str] = []
    first_content = True
    for source in text.splitlines():
        if source.strip().startswith("```"):
            continue
        line = _clean(source)
        if not line:
            blocks.append('<div class="le-paragraph-space" aria-hidden="true"></div>')
            continue
        if first_content and (
            line.casefold() == title.casefold()
            or re.fullmatch(r"[A-Z][A-Z\s&—–:,-]{5,}", line)
        ):
            first_content = False
            continue
        first_content = False
        escaped = html.escape(line)
        if re.match(r"^[-*•]\s+", line):
            item = html.escape(re.sub(r"^[-*•]\s+", "", line))
            blocks.append(f'<div class="le-list-item"><span aria-hidden="true">•</span><p>{item}</p></div>')
        elif _is_heading(line):
            blocks.append(f"<h2>{escaped}</h2>")
        elif re.match(r"^(effective date|date|parties|between)\s*:", line, re.I):
            blocks.append(f'<p class="le-meta-line">{escaped}</p>')
        else:
            blocks.append(f"<p>{escaped}</p>")

    safe_title = html.escape(title)
    body = "\n".join(blocks) or '<p class="le-muted">No document text is available.</p>'
    return f'''<section class="le-document-wrap" aria-label="Document preview">
      <article class="le-document" aria-labelledby="le-document-title">
        <header class="le-document-header"><span class="le-document-mark" aria-hidden="true">L</span><span>LEGALEASE <i>·</i> AI-ASSISTED DRAFT</span></header>
        <div class="le-document-kicker">{safe_title.upper()}</div>
        <h1 id="le-document-title">{safe_title}</h1>
        <div class="le-document-rule" aria-hidden="true"></div>
        <div class="le-document-body">{body}</div>
        <footer class="le-document-footer"><span>Prepared in LegalEase</span><span>Draft for review</span></footer>
      </article>
    </section>'''


def render_document(title: str, text: str) -> None:
    st.markdown(document_html(title, text), unsafe_allow_html=True)
