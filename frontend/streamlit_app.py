from __future__ import annotations

import hashlib
import html
import os
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Any

import streamlit as st
from dotenv import load_dotenv

from api.client import APIError, assist, export_document, generate_document, get_ai_provider, set_ai_provider
from components.document_preview import render_document
from components.ui import brand, disclaimer, page_header, show_error


ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DOCUMENTS = [
    ("Employment contract", "Define the terms of a new working relationship.", "Employment"),
    ("Non-disclosure agreement", "Set clear expectations for confidential information.", "Business"),
    ("Lease agreement", "Outline the responsibilities of a rental arrangement.", "Property"),
    ("Freelance services", "Clarify project scope, payment, and delivery.", "Freelance"),
    ("Service agreement", "Document the terms of a professional service.", "Business"),
    ("Offer letter", "Present role, compensation, and start date.", "Employment"),
    ("Business agreement", "Record shared obligations and commercial terms.", "Business"),
    ("Custom document", "Start with a flexible draft tailored to your needs.", "Custom"),
]
PAGES = ["Overview", "Create document", "My documents", "Templates", "AI assistant", "Settings"]
NAV_ICONS = {
    "Overview": "⌂",
    "Create document": "✧",
    "My documents": "▤",
    "Templates": "◇",
    "AI assistant": "◌",
    "Settings": "⚙",
}

st.set_page_config(
    page_title="LegalEase — Your AI Legal Document Workspace",
    page_icon="L",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_state() -> None:
    defaults: dict[str, Any] = {
        "page": "Landing",
        "workspace_navigation": "Overview",
        "last_sidebar_navigation": "Overview",
        "theme": "Dark",
        "documents": [],
        "document_type": DOCUMENTS[0][0],
        "party_one": "",
        "party_two": "",
        "effective_date": date.today(),
        "key_terms": "",
        "generated_document": "",
        "generated_type": DOCUMENTS[0][0],
        "generated_id": "",
        "create_mode": "Preview",
        "create_summary": "",
        "create_error": "",
        "assistant_messages": [],
        "selected_document_id": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def inject_styles() -> None:
    css = (ROOT / "frontend" / "styles" / "main.css").read_text(encoding="utf-8")
    if st.session_state.theme == "Light":
        variables = """<style>.stApp{--le-bg:#f6f6f8;--le-surface:#fff;--le-surface2:#f0f0f4;--le-hover:#e9e8ef;--le-field:#fbfbfd;--le-line:rgba(25,26,34,.12);--le-text:#202126;--le-muted:#5e6471;--le-accent:#6351c9;--le-accent-soft:rgba(99,81,201,.1);--le-accent-border:rgba(99,81,201,.3);--le-accent-start:#806ee2;--le-accent-end:#6351c9;--le-accent-ink:#fff;--le-nav-text:#484c57}</style>"""
    else:
        variables = """<style>.stApp{--le-bg:#0a0c10;--le-surface:#101318;--le-surface2:#151922;--le-hover:#1a1e27;--le-field:#0d1015;--le-line:rgba(255,255,255,.1);--le-text:#f0eff4;--le-muted:#a5a8b3;--le-accent:#a994ff;--le-accent-soft:rgba(169,148,255,.12);--le-accent-border:rgba(169,148,255,.36);--le-accent-start:#a58eff;--le-accent-end:#8271e8;--le-accent-ink:#171420;--le-nav-text:#c2c4ce}</style>"""
    st.markdown(f"<style>{css}</style>{variables}", unsafe_allow_html=True)


def goto(page: str) -> None:
    st.session_state.page = page
    st.session_state.nav_target = page if page in PAGES else ("My documents" if page == "Workspace" else "Overview")


def sidebar() -> None:
    with st.sidebar:
        brand()
        st.markdown('<div class="le-side-kicker">WORKSPACE</div>', unsafe_allow_html=True)
        current = st.session_state.page if st.session_state.page in PAGES else ("My documents" if st.session_state.page == "Workspace" else "Overview")
        if st.session_state.workspace_navigation not in PAGES:
            st.session_state.workspace_navigation = current
        selected = st.radio(
            "Workspace navigation",
            PAGES,
            format_func=lambda page: f"{NAV_ICONS[page]}\u2003{page}",
            label_visibility="collapsed",
            key="workspace_navigation",
        )
        if selected != st.session_state.last_sidebar_navigation:
            st.session_state.last_sidebar_navigation = selected
            st.session_state.page = selected
        st.markdown('<div class="le-side-kicker le-side-actions-title">QUICK ACTIONS</div>', unsafe_allow_html=True)
        if st.button("←  LegalEase home", key="sidebar_home", use_container_width=True):
            goto("Landing")
            st.rerun()
        if st.button("＋  Create document", key="sidebar_create", type="primary", use_container_width=True):
            goto("Create document")
        st.markdown(
            f'<div class="le-sidebar-session"><span class="le-session-count">{len(st.session_state.documents)}</span>'
            f'<span>saved in this session</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="le-profile"><span class="le-avatar" aria-hidden="true">L</span>'
            '<span>LegalEase user<small>Personal workspace</small></span></div>',
            unsafe_allow_html=True,
        )


def topbar() -> None:
    left, right = st.columns([5, 1])
    with left:
        st.markdown(
            f'<div class="le-topbar"><span>Workspace&nbsp; / &nbsp;<b>{html.escape(st.session_state.page)}</b></span></div>',
            unsafe_allow_html=True,
        )
    with right:
        label = "Light theme" if st.session_state.theme == "Dark" else "Dark theme"
        if st.button(label, key="theme_toggle_top", use_container_width=True):
            st.session_state.theme = "Light" if st.session_state.theme == "Dark" else "Dark"
            st.rerun()


def landing() -> None:
    nav_left, nav_links, nav_actions = st.columns([1.2, 2.2, 1.75], vertical_alignment="center")
    with nav_left:
        brand()
    with nav_links:
        st.markdown(
            '<nav class="le-landing-links" aria-label="Main navigation">'
            '<a href="#templates">Templates</a><a href="#features">Features</a>'
            '<a href="#how">How it works</a></nav>',
            unsafe_allow_html=True,
        )
    with nav_actions:
        workspace_action, start_action = st.columns(2, gap="small")
        with workspace_action:
            if st.button("Workspace", key="landing_workspace", use_container_width=True):
                goto("Overview")
                st.rerun()
        with start_action:
            if st.button("Get started  →", type="primary", key="landing_start", use_container_width=True):
                goto("Create document")
                st.rerun()

    hero_left, hero_right = st.columns([1.05, 1], gap="large", vertical_alignment="center")
    with hero_left:
        st.markdown(
            '<section class="le-hero"><span class="le-eyebrow">◉ &nbsp; YOUR AI LEGAL DOCUMENT WORKSPACE</span>'
            '<h1>Legal documents,<br><em>made effortless.</em></h1>'
            '<p class="le-hero-copy">Thoughtful drafting for the moments that matter. Create, refine, and understand your legal documents in one calm workspace.</p>'
            '<p class="le-trust-line">Provider keys stay server-side &nbsp;·&nbsp; Editable drafts &nbsp;·&nbsp; Export ready</p></section>',
            unsafe_allow_html=True,
        )
        create_col, templates_col = st.columns([1.25, 1])
        with create_col:
            if st.button("✧  Create a document  →", type="primary", key="landing_create", use_container_width=True):
                goto("Create document")
                st.rerun()
        with templates_col:
            if st.button("Explore templates", key="landing_templates_button", use_container_width=True):
                goto("Templates")
                st.rerun()
    with hero_right:
        st.markdown(
            '<div class="le-hero-art" role="img" aria-label="Preview of an employment agreement draft">'
            '<article class="le-hero-paper"><div class="le-hero-paper-top"><span>LEGAL EASE · WORKSPACE</span><span>DRAFT</span></div>'
            '<div class="le-hero-paper-kicker">EMPLOYMENT AGREEMENT</div><h3>Employment<br>Agreement</h3>'
            '<p><b>BETWEEN</b><br>Northstar Studio &nbsp; and &nbsp; Jordan Lee</p><div class="le-paper-rule"></div>'
            '<p><b>01 &nbsp; Scope of work</b><br>Role, responsibilities &amp; expectations</p>'
            '<p><b>02 &nbsp; Compensation</b><br>Payment terms &amp; review cycle</p>'
            '<p><b>03 &nbsp; Confidentiality</b><br>Information &amp; permitted use</p>'
            '<div class="le-paper-footer"><span>Prepared with LegalEase AI</span><span>01 / 04</span></div></article>'
            '<span class="le-chip">✧ &nbsp; AI-assisted draft</span></div>',
            unsafe_allow_html=True,
        )
    st.markdown(
        '<div class="le-trust-strip" aria-label="Product features"><span><i></i> AI-assisted drafting</span>'
        '<span><i></i> Editable from the first word</span><span><i></i> Export in your format</span>'
        '<span><i></i> Keys stay server-side</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown('<section id="features" class="le-section"><span class="le-eyebrow">A WORKSPACE FOR YOUR WORK</span><h2 class="le-section-title">From first draft to<br><em>final details.</em></h2></section>', unsafe_allow_html=True)
    feature_items = [
        ("✧", "Draft with intention", "Turn your context and terms into a structured first draft with your chosen AI provider."),
        ("✎", "Make it your own", "Edit the document directly, refine language, and keep your latest version close."),
        ("◇", "Understand the details", "Ask for a plain language summary or explanation of a clause in your document."),
        ("↓", "Ready when you are", "Download the draft as PDF, DOCX, or plain text whenever you need it."),
    ]
    feature_columns = st.columns(4, gap="medium")
    for col, (symbol, title, description) in zip(feature_columns, feature_items):
        with col:
            st.markdown(
                f'<div class="le-feature-mark" aria-hidden="true">{symbol}</div><div class="le-feature-title">{title}</div>'
                f'<p class="le-feature-copy">{description}</p>',
                unsafe_allow_html=True,
            )

    how_left, how_right = st.columns([1, 1], gap="large")
    with how_left:
        st.markdown(
            '<section id="how" class="le-section"><span class="le-eyebrow">A MORE CONSIDERED PROCESS</span>'
            '<h2 class="le-section-title">Good work begins<br>with <em>clarity.</em></h2>'
            '<p class="le-feature-copy">Start with the details you know. Shape them into a document you can review, refine, and share.</p></section>',
            unsafe_allow_html=True,
        )
        if st.button("Start a draft  →", type="primary", key="landing_start_draft"):
            goto("Create document")
            st.rerun()
    with how_right:
        for number, title, description in [
            ("01", "Share the essentials", "Choose a document and enter parties, dates, and key terms."),
            ("02", "Generate and review", "Receive a draft, then edit it with your context in mind."),
            ("03", "Export your version", "Keep the final copy in the format that fits your workflow."),
        ]:
            st.markdown(f'<div class="le-step"><b>{number}</b><span><strong>{title}</strong><small>{description}</small></span></div>', unsafe_allow_html=True)

    st.markdown('<section id="templates" class="le-section"><span class="le-eyebrow">A THOUGHTFUL PLACE TO START</span><h2 class="le-section-title">Templates for the<br><em>work ahead.</em></h2></section>', unsafe_allow_html=True)
    template_columns = st.columns(4, gap="small")
    for col, (title, desc, category) in zip(template_columns, DOCUMENTS[:4]):
        with col:
            st.markdown(f'<div class="le-template-card"><span class="le-template-category">{category}</span><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
    disclaimer()
    st.markdown('<footer class="le-footer"><span class="le-brand">legal<span class="le-brand-ease">ease</span></span><span>Your AI legal document workspace.</span><span>© 2026 LegalEase</span></footer>', unsafe_allow_html=True)


def page_header_with_action(eyebrow: str, title: str, subtitle: str, action_label: str | None = None, action_key: str | None = None) -> None:
    left, right = st.columns([4, 1.25], vertical_alignment="bottom")
    with left:
        page_header(eyebrow, title, subtitle)
    if action_label and action_key:
        with right:
            if st.button(action_label, type="primary", key=action_key, use_container_width=True):
                goto("Create document")
                st.rerun()


def open_document(document_id: str) -> None:
    st.session_state.selected_document_id = document_id
    goto("Workspace")
    st.rerun()


def document_rows(documents: list[dict[str, str]], key_prefix: str) -> None:
    for document in documents:
        left, status, action = st.columns([5, 1, 1.3], vertical_alignment="center")
        with left:
            st.markdown(
                f'<div class="le-doc-row"><span class="le-doc-icon" aria-hidden="true">▤</span>'
                f'<span><span class="le-doc-title">{html.escape(document["title"])}</span><br>'
                f'<span class="le-doc-sub">{html.escape(document["type"])} · Edited {html.escape(document.get("updated", "recently"))}</span></span></div>',
                unsafe_allow_html=True,
            )
        with status:
            st.markdown('<span class="le-status">Draft</span>', unsafe_allow_html=True)
        with action:
            if st.button("Open document", key=f"{key_prefix}_open_{document['id']}", use_container_width=True):
                open_document(document["id"])


def dashboard() -> None:
    page_header_with_action("YOUR WORKSPACE", "Good morning.", "A clear place to begin your next draft.", "＋  New document", "dashboard_create")
    st.markdown(
        '<section class="le-welcome"><span class="le-eyebrow">LEGAL EASE · AI WORKSPACE</span>'
        '<h2>Make room for<br><em>the important details.</em></h2>'
        '<p>Bring your terms together. Start with a document that fits the work ahead.</p></section>',
        unsafe_allow_html=True,
    )
    st.markdown('<h2 class="le-section-heading">Recent documents</h2><p class="le-subheading">Your drafts, saved in this session.</p>', unsafe_allow_html=True)
    docs = st.session_state.documents[:4]
    if docs:
        document_rows(docs, "dashboard")
    else:
        st.markdown('<div class="le-empty"><h3>Your workspace is ready</h3><p>Start a draft and it will be saved here for easy access.</p></div>', unsafe_allow_html=True)
        if st.button("Create your first document →", key="dashboard_empty_create"):
            goto("Create document")
            st.rerun()
    disclaimer(compact=True)


def save_document(title: str, document_type: str, content: str, document_id: str = "") -> str:
    docs: list[dict[str, str]] = st.session_state.documents
    document_id = document_id or str(uuid.uuid4())
    now = datetime.now().strftime("%d %b %Y, %H:%M")
    updated = {"id": document_id, "title": title, "type": document_type, "content": content, "updated": now}
    existing = next((i for i, item in enumerate(docs) if item["id"] == document_id), None)
    if existing is None:
        docs.insert(0, updated)
    else:
        docs[existing] = updated
    st.session_state.documents = docs
    return document_id


def create_document() -> None:
    page_header("DOCUMENT STUDIO", "Start with the essentials.", "A few details give your first draft a more useful shape.")
    form_col, preview_col = st.columns([.9, 1.1], gap="medium")
    with form_col:
        with st.form("create_document_form", clear_on_submit=False):
            st.markdown('<div class="le-panel-heading le-form-section">01 &nbsp; Document details</div>', unsafe_allow_html=True)
            selected_type = st.selectbox("Document type", [item[0] for item in DOCUMENTS], key="document_type")
            party_a, party_b = st.columns(2)
            with party_a:
                party_one = st.text_input("First party", key="party_one", placeholder="Person or organization")
            with party_b:
                party_two = st.text_input("Second party", key="party_two", placeholder="Person or organization")
            effective_date = st.date_input("Effective date", key="effective_date")
            st.markdown('<div class="le-panel-heading">02 &nbsp; Key terms</div>', unsafe_allow_html=True)
            key_terms = st.text_area("Terms & conditions", key="key_terms", height=150, placeholder="Scope, payment, timelines, responsibilities, confidentiality…")
            submitted = st.form_submit_button("✧  Generate with AI", type="primary", use_container_width=True)

        if submitted:
            missing = []
            if not party_one.strip():
                missing.append("First party")
            if not party_two.strip():
                missing.append("Second party")
            if len(key_terms.strip()) < 5:
                missing.append("Key terms (at least 5 characters)")
            if missing:
                st.error("Please complete: " + ", ".join(missing) + ".")
            else:
                try:
                    with st.spinner("Preparing your draft with AI… Please keep this page open."):
                        result = generate_document(
                            selected_type,
                            party_one.strip(),
                            party_two.strip(),
                            effective_date.isoformat(),
                            key_terms.strip(),
                        )
                    st.session_state.generated_document = result["document"]
                    st.session_state.generated_type = selected_type
                    st.session_state.generated_id = ""
                    st.session_state.create_mode = "Preview"
                    st.session_state.create_summary = ""
                    st.session_state.create_error = ""
                    st.session_state["create_document_editor"] = result["document"]
                    st.success("Your draft is ready for review.")
                except APIError as exc:
                    st.session_state.create_error = str(exc)
                except Exception:
                    st.session_state.create_error = "Something went wrong while creating the draft. Please try again."

        if st.session_state.create_error:
            show_error(st.session_state.create_error)

    with preview_col:
        content = st.session_state.generated_document
        with st.container(border=True):
            st.markdown('<div class="le-panel-heading le-preview-heading">LIVE DOCUMENT</div>', unsafe_allow_html=True)
            if content:
                mode = st.radio("Document view", ["Preview", "Edit text"], horizontal=True, key="create_mode")
                if mode == "Edit text":
                    edited = st.text_area("Edit generated document", key="create_document_editor", height=470, label_visibility="visible")
                    st.session_state.generated_document = edited
                    content = edited
                else:
                    render_document(st.session_state.generated_type, content)
                action_cols = st.columns(2)
                with action_cols[0]:
                    if st.button("Save draft", key="create_save_draft", type="primary", use_container_width=True):
                        doc_id = save_document(
                            st.session_state.generated_type,
                            st.session_state.generated_type,
                            st.session_state.generated_document,
                            st.session_state.generated_id,
                        )
                        st.session_state.generated_id = doc_id
                        st.session_state.selected_document_id = doc_id
                        goto("Workspace")
                        st.rerun()
                with action_cols[1]:
                    if st.button("Summarize draft", key="create_summary_button", use_container_width=True):
                        try:
                            with st.spinner("Summarizing the draft…"):
                                st.session_state.create_summary = assist("summary", content)
                        except APIError as exc:
                            st.session_state.create_error = str(exc)
                        st.rerun()
                if st.session_state.create_summary:
                    st.info(f"Document summary\n\n{st.session_state.create_summary}")
                export_controls(content, "create")
            else:
                st.markdown('<div class="le-empty"><h3>A considered first draft</h3><p>Complete the details and generate a real draft with your configured AI provider.</p></div>', unsafe_allow_html=True)
    disclaimer(compact=True)


def export_controls(text: str, slot: str) -> None:
    if not text.strip():
        return
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    format_key = f"{slot}_export_format"
    cache_key = f"{slot}_export_cache"
    cache = st.session_state.get(cache_key)
    if cache and cache.get("digest") != digest:
        st.session_state[cache_key] = None
        cache = None
    formats = ["PDF", "DOCX", "TXT"]
    selected = st.selectbox("Export format", formats, key=format_key)
    if st.button(f"Prepare {selected} download", key=f"{slot}_prepare_{selected.lower()}", use_container_width=True):
        try:
            with st.spinner(f"Preparing {selected}…"):
                data, mime = export_document(selected.lower(), text)
            st.session_state[cache_key] = {
                "digest": digest,
                "format": selected.lower(),
                "data": data,
                "mime": mime,
            }
            st.rerun()
        except APIError as exc:
            show_error(str(exc))
    cache = st.session_state.get(cache_key)
    if cache and cache.get("digest") == digest and cache.get("format") == selected.lower():
        st.download_button(
            f"Download {selected}",
            data=cache["data"],
            file_name=f"legalease-document.{cache['format']}",
            mime=cache["mime"],
            key=f"{slot}_download_{cache['format']}",
            use_container_width=True,
        )


def templates_page() -> None:
    page_header("LIBRARY", "Find your starting point.", "Choose a document type and shape it around your needs.")
    categories = ["All", "Business", "Employment", "Property", "Freelance", "Custom"]
    category = st.segmented_control(
        "Template category",
        categories,
        selection_mode="single",
        required=True,
        default="All",
        key="template_category_filter",
        label_visibility="collapsed",
        width="stretch",
        wrap=True,
    ) or "All"
    results = [doc for doc in DOCUMENTS if category == "All" or doc[2] == category]
    st.markdown(
        f'<div class="le-template-results"><span>Curated starting points</span>'
        f'<span>{len(results)} {"templates" if len(results) != 1 else "template"}</span></div>',
        unsafe_allow_html=True,
    )
    cards = st.columns(3, gap="small")
    for i, (title, description, group) in enumerate(results):
        with cards[i % len(cards)]:
            st.markdown(f'<div class="le-template-card"><span class="le-template-category">{group}</span><h3>{title}</h3><p>{description}</p></div>', unsafe_allow_html=True)
            if st.button("Use template →", key=f"use_template_{title}", use_container_width=True):
                st.session_state.document_type = title
                goto("Create document")
                st.rerun()


def documents_page() -> None:
    page_header_with_action("YOUR LIBRARY", "Documents.", "All drafts saved in this Streamlit session.", "＋  New document", "documents_new")
    query = st.text_input("Search documents", placeholder="Search documents…", key="documents_search")
    docs = [doc for doc in st.session_state.documents if query.lower() in doc["title"].lower()]
    if docs:
        document_rows(docs, "documents")
    else:
        title = "No matching documents" if st.session_state.documents else "Your library is empty"
        body = "Try a different search term." if st.session_state.documents else "Create a draft to start building your library."
        st.markdown(f'<div class="le-empty"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)
        if not st.session_state.documents and st.button("Create a document →", key="documents_empty_create"):
            goto("Create document")
            st.rerun()


def workspace_page() -> None:
    docs = st.session_state.documents
    doc = next((item for item in docs if item["id"] == st.session_state.selected_document_id), None)
    if doc is None:
        page_header("DOCUMENT WORKSPACE", "No document selected.", "Choose a draft from your document library.")
        if st.button("Go to documents", key="workspace_back"):
            goto("My documents")
            st.rerun()
        return

    page_header("DOCUMENT WORKSPACE", doc["title"], "Review and refine your draft before you export.")
    editor, assistant_col = st.columns([1.5, .7], gap="medium")
    with editor:
        with st.container(border=True):
            st.markdown('<div class="le-panel-heading le-preview-heading">DOCUMENT EDITOR</div>', unsafe_allow_html=True)
            mode_key = f"workspace_mode_{doc['id']}"
            mode = st.radio("Document view", ["Preview", "Edit text"], horizontal=True, key=mode_key)
            text_key = f"workspace_edit_{doc['id']}"
            if text_key not in st.session_state:
                st.session_state[text_key] = doc["content"]
            if mode == "Edit text":
                content = st.text_area("Edit document text", key=text_key, height=520)
            else:
                content = st.session_state[text_key]
                render_document(doc["title"], content)
            doc["content"] = content
            if st.button("Save changes", key=f"save_{doc['id']}", type="primary", use_container_width=True):
                save_document(doc["title"], doc["type"], content, doc["id"])
                st.success("Changes saved in this session.")
            export_controls(content, f"workspace_{doc['id']}")
    with assistant_col:
        with st.container(border=True):
            st.markdown('<div class="le-panel-heading le-preview-heading">✧ &nbsp; LegalEase AI</div><p class="le-feature-copy">Document companion. Ask for a summary or a plain-language explanation of a clause.</p>', unsafe_allow_html=True)
            if st.button("Summarize document", key=f"summary_{doc['id']}", use_container_width=True):
                try:
                    with st.spinner("Summarizing the document…"):
                        st.session_state[f"summary_{doc['id']}"] = assist("summary", content)
                except APIError as exc:
                    show_error(str(exc))
                st.rerun()
            summary = st.session_state.get(f"summary_{doc['id']}")
            if summary:
                st.info(summary)
            clause = st.text_area("Clause to explain", height=130, key=f"clause_{doc['id']}", placeholder="Paste a clause from your document…")
            if st.button("Explain clause", key=f"explain_{doc['id']}", use_container_width=True):
                if not clause.strip():
                    st.error("Paste a clause before requesting an explanation.")
                else:
                    try:
                        with st.spinner("Explaining the clause…"):
                            st.session_state[f"explanation_{doc['id']}"] = assist("explain", clause)
                    except APIError as exc:
                        show_error(str(exc))
                    st.rerun()
            explanation = st.session_state.get(f"explanation_{doc['id']}")
            if explanation:
                st.info(explanation)
            st.caption("AI responses are informational. Review important terms with a qualified professional.")
    disclaimer(compact=True)


def assistant_page() -> None:
    page_header("AI COMPANION", "A little more clarity.", "Ask for a plain-language explanation of a legal clause.")
    with st.form("assistant_form", clear_on_submit=True):
        clause = st.text_area("Clause to understand", height=180, placeholder="Paste the clause you would like explained…")
        submitted = st.form_submit_button("Explain clause", type="primary")
    if submitted:
        if not clause.strip():
            st.error("Paste a clause before requesting an explanation.")
        else:
            st.session_state.assistant_messages.append({"role": "user", "content": clause.strip()})
            try:
                with st.spinner("Reviewing the clause…"):
                    answer = assist("explain", clause.strip())
                st.session_state.assistant_messages.append({"role": "assistant", "content": answer})
            except APIError as exc:
                st.session_state.assistant_messages.append({"role": "assistant", "content": f"Error: {exc}"})
    for message in st.session_state.assistant_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    disclaimer(compact=True)


def settings_page() -> None:
    page_header("PREFERENCES", "Settings.", "Make your workspace feel like yours.")
    try:
        provider_status = get_ai_provider()
    except APIError as exc:
        provider_status = None
        show_error(f"Could not load AI provider settings: {exc}")

    if provider_status:
        active_provider = provider_status.get("provider", "groq")
        providers = provider_status.get("providers", {})
        active_info = providers.get(active_provider, {})
        next_provider = "gemini" if active_provider == "groq" else "groq"
        next_info = providers.get(next_provider, {})
        with st.container(border=True):
            provider_details, provider_action = st.columns([2.2, 1], vertical_alignment="center")
            with provider_details:
                st.markdown('<div class="le-panel-heading">AI MODEL</div>', unsafe_allow_html=True)
                model_name = html.escape(str(active_info.get("model", "")))
                provider_name = html.escape(active_provider.title())
                st.markdown(
                    f'<div class="le-provider-current">{provider_name} '
                    f'<span>{model_name}</span></div>',
                    unsafe_allow_html=True,
                )
                if not active_info.get("configured", False):
                    required_key = "GROQ_API_KEY" if active_provider == "groq" else "GEMINI_API_KEY"
                    st.warning(f"Configure {required_key} in the backend .env to use this provider.")
            with provider_action:
                if next_info.get("configured", False):
                    if st.button(
                        f"Switch to {next_provider.title()}",
                        key="ai_provider_toggle",
                        type="primary",
                        use_container_width=True,
                    ):
                        try:
                            set_ai_provider(next_provider)
                            st.rerun()
                        except APIError as exc:
                            show_error(str(exc))
                else:
                    st.button(
                        f"{next_provider.title()} unavailable",
                        key="ai_provider_toggle_unavailable",
                        disabled=True,
                        use_container_width=True,
                    )
                    required_key = "GROQ_API_KEY" if next_provider == "groq" else "GEMINI_API_KEY"
                    st.caption(f"Add {required_key} to enable switching.")
            st.caption("Applies to future AI requests. Restarting the backend restores AI_PROVIDER from .env.")

    st.markdown('<div class="le-workspace-card"><div class="le-panel-heading">Appearance</div><p class="le-feature-copy">Choose a comfortable workspace theme.</p></div>', unsafe_allow_html=True)
    st.session_state.setdefault("settings_theme", st.session_state.theme)
    current = st.radio("Workspace theme", ["Dark", "Light"], horizontal=True, key="settings_theme")
    if current != st.session_state.theme:
        st.session_state.theme = current
        st.rerun()
    st.markdown('<div class="le-workspace-card"><div class="le-panel-heading">Data &amp; privacy</div><p class="le-feature-copy">Your saved drafts are kept in this Streamlit session. AI requests are sent to the provider configured on the backend.</p></div>', unsafe_allow_html=True)
    disclaimer(compact=True)


def main() -> None:
    init_state()
    nav_target = st.session_state.pop("nav_target", None)
    if nav_target:
        st.session_state.workspace_navigation = nav_target
        st.session_state.last_sidebar_navigation = nav_target
    inject_styles()
    if st.session_state.page == "Landing":
        landing()
        return

    sidebar()
    topbar()
    page = st.session_state.page
    if page == "Overview":
        dashboard()
    elif page == "Create document":
        create_document()
    elif page == "My documents":
        documents_page()
    elif page == "Templates":
        templates_page()
    elif page == "Workspace":
        workspace_page()
    elif page == "AI assistant":
        assistant_page()
    elif page == "Settings":
        settings_page()
    else:
        page_header("404", "This page could not be found.", "Return to your LegalEase workspace.")
        if st.button("Back to workspace"):
            goto("Overview")
            st.rerun()


init_state()
inject_styles()
main()
