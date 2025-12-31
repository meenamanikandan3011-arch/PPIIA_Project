import streamlit as st
import os, re
import fitz  # PyMuPDF
from groq import Groq
from fpdf import FPDF

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Parliament Bill Auditor",
    layout="wide"
)

st.markdown("## 🏛️ Parliament Bill Auditor")
st.caption("Upload Indian Parliament Bills and get AI-powered policy analysis")

# ---------------- API KEY ----------------
if "GROQ_API_KEY" not in st.secrets:
    st.error("❌ GROQ_API_KEY not set in Streamlit Secrets")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------- SESSION STATE ----------------
st.session_state.setdefault("analysis", "")
st.session_state.setdefault("bill_text", "")

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text(pdf_file):
    pdf_file.seek(0)
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ---------------- CLEAN TEXT ----------------
def clean_text(text):
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\(Interruptions\)", "", text)
    text = re.sub(r"\d+\s*hrs", "", text)
    return text.strip()

# ---------------- CHUNKING ----------------
def chunk_text(text, size=800):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

# ---------------- ANALYSIS ----------------
# ---------- SECTION EXTRACTOR ----------
def extract_sections(text):
    sections = {
        "sector": "",
        "summary": "",
        "impact": ""
    }

    current = None
    for line in text.splitlines():
        l = line.lower()

        if "sector" in l:
            current = "sector"
        elif "summary" in l:
            current = "summary"
        elif "short-term impact" in l or "medium-term impact" in l or "long-term impact" in l or "impact" in l:
            current = "impact"

        if current:
            sections[current] += line + "\n"

    return sections


# ---------- DISPLAY RESULTS ----------
if st.session_state.analysis:
    sections = extract_sections(st.session_state.analysis)

    tab1, tab2, tab3 = st.tabs(["📊 Sector", "📝 Summary", "⚖️ Impact"])

    with tab1:
        st.subheader("📊 Sector Analysis")
        st.write(sections["sector"])

    with tab2:
        st.subheader("📝 Bill Summary")
        st.write(sections["summary"])

    with tab3:
        st.subheader("⚖️ Impact Assessment")
        st.write(sections["impact"])

    st.download_button(
        "📥 Download Full Summary as PDF",
        make_pdf(st.session_state.analysis),
        file_name="parliament_bill_summary.pdf",
        mime="application/pdf"
    )

# ---------------- PDF DOWNLOAD ----------------
def make_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)
    return pdf.output(dest="S").encode("latin-1")

# ---------------- FILE UPLOAD ----------------
uploaded = st.file_uploader("📄 Upload Parliament Bill (PDF)", type="pdf")

if uploaded:
    if st.button("🚀 Generate Analysis"):
        with st.spinner("Analyzing bill..."):
            raw = extract_text(uploaded)
            cleaned = clean_text(raw)
            st.session_state.bill_text = cleaned
            st.session_state.analysis = analyze_bill(cleaned)

# ---------------- DISPLAY ----------------
if st.session_state.analysis:
    tab1, tab2, tab3 = st.tabs(["📊 Sector", "📝 Summary", "⚖️ Impact"])

    with tab1:
        st.write(st.session_state.analysis)

    with tab2:
        st.write(st.session_state.analysis)

    with tab3:
        st.write(st.session_state.analysis)

    st.download_button(
        "📥 Download Summary PDF",
        make_pdf(st.session_state.analysis),
        "bill_summary.pdf",
        "application/pdf"
    )

# ---------------- ASK AI ----------------
st.markdown("---")
st.subheader("💬 Ask AI about this Bill")

q = st.text_input("Ask a question")

if st.button("Ask"):
    if q:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": f"Bill:\n{st.session_state.bill_text}\n\nQuestion:\n{q}"
            }],
            temperature=0.3
        )
        st.success(res.choices[0].message.content)
