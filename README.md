<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,50:312e81,100:7c3aed&height=230&section=header&text=LegalEase&fontSize=72&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=AI-Powered%20Legal%20Document%20Workspace&descAlignY=58&descSize=20"/>

<br>

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=600&size=22&duration=3000&pause=900&color=8B5CF6&center=true&vCenter=true&width=760&lines=Draft+Legal+Documents+with+AI;Understand+Complex+Clauses;Summarize+Legal+Documents;Edit+%7C+Analyze+%7C+Export;Built+for+Modern+Legal+Workflows"/>

<br><br>

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)](https://streamlit.io/)
[![Groq](https://img.shields.io/badge/Groq-AI-F55036?style=for-the-badge)](https://groq.com/)
[![Gemini](https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge\&logo=google)](https://ai.google.dev/)

<br>

[![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/LegalEase?style=flat-square\&logo=github\&color=8B5CF6)](https://github.com/YOUR_USERNAME/LegalEase/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/YOUR_USERNAME/LegalEase?style=flat-square\&logo=github\&color=6366F1)](https://github.com/YOUR_USERNAME/LegalEase/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/YOUR_USERNAME/LegalEase?style=flat-square\&color=EC4899)](https://github.com/YOUR_USERNAME/LegalEase/issues)
[![GitHub License](https://img.shields.io/github/license/YOUR_USERNAME/LegalEase?style=flat-square\&color=22C55E)](https://github.com/YOUR_USERNAME/LegalEase/blob/main/LICENSE)

<br><br>

**Draft smarter. Understand better. Review carefully.**

</div>

---

# ⚖️ LegalEase

### AI-Powered Legal Document Workspace

LegalEase is a modern AI-powered legal document workspace designed to make working with legal documents **simpler, faster, and more accessible**.

It brings document generation, editing, AI explanations, summarization, and exporting into one unified workspace.

```text
                 ┌───────────────────────────────┐
                 │           LegalEase            │
                 │                               │
                 │     AI Legal Document Hub     │
                 └───────────────┬───────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
           ✍️ Draft           🧠 Understand       📄 Export
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 ▼
                         🔍 Review & Edit
```

> **LegalEase is an AI-assisted document tool, not a substitute for qualified legal advice.**

---

# ✨ What Can LegalEase Do?

<table>
<tr>
<td width="50%">

## ✍️ AI Document Generation

Generate structured legal document drafts from natural-language requirements.

**Supported document types:**

* Employment Contract
* NDA
* Lease Agreement
* Freelance Contract
* Service Agreement
* Custom Agreement

</td>

<td width="50%">

## 🧠 AI Understanding

Turn complex legal language into easier-to-understand explanations.

**Capabilities:**

* Document summaries
* Clause explanations
* Key information
* Obligations
* Important provisions
* Simplified explanations

</td>
</tr>

<tr>
<td width="50%">

## 📝 Document Editing

Generate a document and refine it inside the workspace.

```text
Generate
   ↓
Review
   ↓
Edit
   ↓
Analyze
```

</td>

<td width="50%">

## 📄 Multi-Format Export

Export your edited document as:

```text
TXT
DOCX
PDF
```

Powered by `python-docx` and `ReportLab`.

</td>
</tr>
</table>

---

# 🎬 Product Demo

<div align="center">

### 🚀 Full LegalEase Workflow

<!-- Replace this image with your actual demo GIF -->

<img src="docs/demo/legalease-demo.gif" width="90%" alt="LegalEase Demo">

</div>

> 💡 **Tip:** Record a short 10–20 second GIF showing:
>
> `Create Document → AI Generation → Edit → Explain Clause → Export PDF`

---

# 🖼️ Interface Preview

<div align="center">

### 🏠 Dashboard

<img src="docs/screenshots/dashboard.png" width="90%" alt="LegalEase Dashboard">

<br><br>

### ✍️ Document Workspace

<img src="docs/screenshots/editor.png" width="90%" alt="LegalEase Editor">

<br><br>

### 🧠 AI Assistant

<img src="docs/screenshots/assistant.png" width="90%" alt="LegalEase AI Assistant">

</div>

> If you don't have screenshots yet, create:
>
> ```text
> docs/
> ├── screenshots/
> │   ├── dashboard.png
> │   ├── editor.png
> │   └── assistant.png
> │
> └── demo/
>     └── legalease-demo.gif
> ```

---

# 🧠 How LegalEase Works

```mermaid
flowchart TD

    USER["👤 User"]

    UI["⚖️ LegalEase<br/>Streamlit UI"]

    API["⚡ FastAPI<br/>Backend"]

    AI{"🤖 AI Provider"}

    GROQ["🟠 Groq"]
    GEMINI["🔵 Gemini"]

    DOC["📄 Document Engine"]

    SUMMARY["🧠 Summary"]
    EXPLAIN["🔍 Clause Explanation"]
    GENERATE["✍️ Document Generation"]

    EXPORT{"📤 Export"}

    TXT["📃 TXT"]
    DOCX["📘 DOCX"]
    PDF["📕 PDF"]

    USER --> UI
    UI --> API

    API --> AI

    AI --> GROQ
    AI --> GEMINI

    API --> GENERATE
    API --> SUMMARY
    API --> EXPLAIN

    GENERATE --> DOC
    DOC --> EXPORT

    EXPORT --> TXT
    EXPORT --> DOCX
    EXPORT --> PDF
```

---

# 🏗️ System Architecture

```mermaid
graph LR

    A["Browser"] --> B["Streamlit"]

    B --> C["FastAPI"]

    C --> D["AI Service"]

    D --> E["Groq"]
    D --> F["Gemini"]

    C --> G["Document Processing"]

    G --> H["python-docx"]
    G --> I["ReportLab"]

    H --> J["DOCX"]
    I --> K["PDF"]

    G --> L["TXT"]
```

---

# 🔄 Complete Workflow

<div align="center">

```text
┌────────────────────┐
│    👤 Describe     │
│     Your Need      │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│   🤖 AI Generate   │
│     Draft          │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│   ✏️ Edit Draft    │
│   Inside Workspace │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ 🧠 Understand      │
│ Summary / Clauses  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│   🔍 Review         │
│   Carefully         │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│   📄 Export         │
│ TXT / DOCX / PDF   │
└────────────────────┘
```

</div>

---

# 🛠️ Technology Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,fastapi,html,css,react&theme=dark" />

</div>

<br>

| Layer          | Technology        |
| -------------- | ----------------- |
| 🎨 Frontend    | Streamlit         |
| 🎨 UI          | Custom HTML / CSS |
| ⚡ Backend      | FastAPI           |
| 🧩 Validation  | Pydantic          |
| 🤖 AI Provider | Groq / Gemini     |
| 📘 DOCX        | python-docx       |
| 📕 PDF         | ReportLab         |
| ⚛️ Original UI | React             |
| 🐍 Runtime     | Python 3.12       |

---

# 🤖 AI Provider Architecture

LegalEase uses an environment-based provider configuration.

```text
                         LegalEase
                             │
                             ▼
                    ┌─────────────────┐
                    │  AI_PROVIDER    │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
                🟠 Groq           🔵 Gemini
                    │                 │
                    └────────┬────────┘
                             ▼
                       AI Response
```

Set the provider in `.env`:

```env
AI_PROVIDER=groq
```

or:

```env
AI_PROVIDER=gemini
```

---

# 🔐 Security

LegalEase keeps AI API credentials on the backend.

```text
                 ❌
        Browser → API Key

                 ✅
        Browser → FastAPI
                     │
                     ▼
                 API Key
                     │
                     ▼
                AI Provider
```

### Environment variables

```env
AI_PROVIDER=groq

GROQ_API_KEY=your_groq_api_key

GEMINI_API_KEY=your_gemini_api_key

API_BASE_URL=http://127.0.0.1:8001
```

### Never commit secrets

Your `.gitignore` should include:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

# 💻 Local Development

## 1. Install Python 3.12

Windows:

```powershell
winget install --id Python.Python.3.12
```

Verify:

```powershell
python --version
```

---

## 2. Clone Repository

```powershell
git clone YOUR_REPOSITORY_URL

cd LegalEase
```

---

## 3. Create Virtual Environment

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# 🔑 Environment Configuration

Copy:

```text
.env.example
```

to:

```text
.env
```

Example:

```env
AI_PROVIDER=groq

GROQ_API_KEY=your_groq_api_key

GEMINI_API_KEY=your_gemini_api_key

API_BASE_URL=http://127.0.0.1:8001
```

Only the selected provider needs to be configured.

---

# ⚡ Backend

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Start FastAPI:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app `
  --host 127.0.0.1 `
  --port 8001 `
  --reload
```

Backend:

```text
http://127.0.0.1:8001
```

Interactive API documentation:

```text
http://127.0.0.1:8001/docs
```

---

# 🎨 Frontend

Open another terminal.

Activate environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r frontend\requirements.txt
```

Start Streamlit:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend\streamlit_app.py `
  --server.address 127.0.0.1 `
  --server.port 8501
```

Open:

```text
http://127.0.0.1:8501
```

---

# 📂 Project Structure

```text
LegalEase/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── ...
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── streamlit_app.py
│   ├── requirements.txt
│   │
│   └── src/
│       └── ...
│
├── docs/
│   ├── screenshots/
│   │   ├── dashboard.png
│   │   ├── editor.png
│   │   └── assistant.png
│   │
│   └── demo/
│       └── legalease-demo.gif
│
├── .env.example
├── .gitignore
└── README.md
```

---

# 🔌 API Reference

## `GET /`

Health check.

```http
GET /
```

---

## `POST /api/documents/generate`

Generate an AI-assisted legal document.

```http
POST /api/documents/generate
```

```text
User Requirements
       ↓
AI Provider
       ↓
Legal Document Draft
```

---

## `POST /api/ai/summary`

Summarize supplied document text.

```http
POST /api/ai/summary
```

Example:

```json
{
  "text": "Your legal document content..."
}
```

---

## `POST /api/ai/explain`

Explain a supplied legal clause.

```http
POST /api/ai/explain
```

Example:

```json
{
  "clause": "The employee shall..."
}
```

---

## `POST /api/exports/txt`

Export document text.

```http
POST /api/exports/txt
```

---

## `POST /api/exports/docx`

Generate a Word document.

```http
POST /api/exports/docx
```

Powered by:

```text
python-docx
```

---

## `POST /api/exports/pdf`

Generate a PDF document.

```http
POST /api/exports/pdf
```

Powered by:

```text
ReportLab
```

---

# 🖥️ Animated Terminal Demo

You can include a terminal GIF here:

<div align="center">

<img src="docs/demo/terminal.gif" width="800" alt="LegalEase Terminal Demo">

</div>

Example terminal flow:

```text
$ git clone LegalEase

$ cd LegalEase

$ python -m venv .venv

$ pip install -r backend/requirements.txt

$ uvicorn backend.main:app --reload --port 8001

✓ Backend started
✓ AI provider configured
✓ LegalEase ready
```

---

# 🔍 Before / After

<div align="center">

### Complex Legal Language

<img src="docs/demo/before-clause.gif" width="80%" alt="Complex legal clause">

⬇️

### AI Explanation

<img src="docs/demo/after-clause.gif" width="80%" alt="AI explanation">

</div>

---

# 📊 GitHub Stats

<div align="center">

<img src="https://github-readme-stats.vercel.app/api?username=YOUR_USERNAME&show_icons=true&theme=transparent&hide_border=true&title_color=8B5CF6&icon_color=8B5CF6&text_color=94A3B8"/>

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=YOUR_USERNAME&layout=compact&theme=transparent&hide_border=true&title_color=8B5CF6&text_color=94A3B8"/>

<br><br>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=YOUR_USERNAME&theme=transparent&hide_border=true&ring=8B5CF6&fire=EC4899&currStreakLabel=8B5CF6"/>

</div>

---

# 🐍 Contribution Animation

<div align="center">

<img src="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake-dark.svg" alt="GitHub Contribution Snake">

</div>

> If the snake animation isn't available yet, configure the GitHub Action that generates it.

---

# 📈 Project Roadmap

```text
CORE PLATFORM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%

[x] AI Document Generation
[x] AI Summary
[x] Clause Explanation
[x] Document Editing
[x] TXT Export
[x] DOCX Export
[x] PDF Export
[x] Groq Integration
[x] Gemini Integration
[x] Streamlit Migration


NEXT GENERATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[ ] Authentication
[ ] Cloud Document Storage
[ ] Document Versioning
[ ] Document Sharing
[ ] Real-Time Collaboration
[ ] OCR
[ ] Digital Signatures
[ ] Multi-Language Support
[ ] Advanced Legal Analysis
[ ] Role-Based Access
```

---

# 🧩 Interactive Features

<details>
<summary>📄 Supported Documents</summary>

<br>

LegalEase can be used for drafting:

* Employment Contracts
* Non-Disclosure Agreements
* Lease Agreements
* Freelance Contracts
* Service Agreements
* Custom Agreements

</details>

<details>
<summary>🤖 AI Features</summary>

<br>

* AI document generation
* AI summaries
* Clause explanation
* Document understanding
* Provider switching
* Error-aware AI configuration

</details>

<details>
<summary>📤 Export Features</summary>

<br>

Supported formats:

```text
TXT
DOCX
PDF
```

</details>

<details>
<summary>🔐 Security</summary>

<br>

* API keys remain server-side
* `.env` configuration
* No fabricated AI fallback
* Browser-local document history
* Explicit provider/configuration errors

</details>

<details>
<summary>🧪 Development</summary>

<br>

Backend:

```powershell
uvicorn backend.main:app --host 127.0.0.1 --port 8001 --reload
```

Frontend:

```powershell
streamlit run frontend/streamlit_app.py
```

</details>

---

# 🤝 Contributing

Contributions are welcome.

### 1. Fork

```bash
git fork
```

### 2. Create a branch

```bash
git checkout -b feature/your-feature
```

### 3. Make changes

```bash
git add .
```

### 4. Commit

```bash
git commit -m "feat: add your feature"
```

### 5. Push

```bash
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 🐛 Issues & Feature Requests

Found a bug?

Open an issue and include:

```text
Environment
Python version
Operating system
Steps to reproduce
Expected behavior
Actual behavior
Error logs
```

For feature requests, describe:

```text
Problem
Proposed solution
Expected user experience
```

---

# ⚠️ Legal Disclaimer

LegalEase is an **AI-assisted legal document workspace**.

It does not provide legal representation and does not establish an attorney-client relationship.

AI-generated content may contain errors, omissions, or provisions that are unsuitable for a particular situation.

Documents should be reviewed by a qualified legal professional before being relied upon, signed, submitted, or used for legal purposes.

---

# 📜 License

If this project is intended to be open source, add your chosen license.

For example:

```text
MIT License
```

Then add:

```text
LICENSE
```

to the repository.

---

# 🌟 Why LegalEase?

```text
Traditional Workflow

Search
  ↓
Read
  ↓
Copy
  ↓
Edit
  ↓
Format
  ↓
Export
  ↓
Repeat


             VS


LegalEase

      Describe
          ↓
      🤖 Generate
          ↓
       ✏️ Edit
          ↓
      🧠 Understand
          ↓
       🔍 Review
          ↓
       📄 Export
```

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7c3aed,50:312e81,100:0f172a&height=150&section=footer"/>

## ⚖️ LegalEase

### Draft smarter. Understand better. Review carefully.

<br>

**Built with Python · FastAPI · Streamlit · AI**

<br>

⭐ **Star the repository if you find LegalEase useful.**

</div>
