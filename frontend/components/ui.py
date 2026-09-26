import html

import streamlit as st


def brand() -> None:
    st.markdown(
        '<div class="le-brand"><span class="le-brand-icon" aria-hidden="true">L</span>'
        '<span>legal<span class="le-brand-ease">ease</span></span></div>',
        unsafe_allow_html=True,
    )


def page_header(eyebrow: str, title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="le-page-heading"><span class="le-eyebrow">{html.escape(eyebrow)}</span>'
        f'<h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',
        unsafe_allow_html=True,
    )


def disclaimer(compact: bool = False) -> None:
    class_name = "le-disclaimer le-disclaimer-compact" if compact else "le-disclaimer"
    st.markdown(
        f'<aside class="{class_name}" aria-label="Legal information disclaimer">'
        '<span aria-hidden="true">◇</span><p>LegalEase provides AI-generated drafts and information for informational purposes. '
        'It is not a substitute for advice from a qualified legal professional.</p></aside>',
        unsafe_allow_html=True,
    )


def show_error(message: str) -> None:
    st.error(message)
