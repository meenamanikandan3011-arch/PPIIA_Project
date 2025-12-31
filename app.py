import streamlit as st
import os, re
import fitz  # PyMuPDF
from groq import Groq
from fpdf import FPDF

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Parliament Bill Auditor", layout="wide")
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

# ---------------- PDF EXTRACTION ----------------
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
    return text.strip()

# ---------------- CHUNKING ----------------
def chunk_text(text, size=900):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

# ---------------- AI ANALYSIS ----------------
def analyze_bill(text):
    chunks = chunk_text(text)
    partial = []

    for chunk in chunks[:5]:
        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{
                "role": "user",
                "content": f"Summarize this Indian Parliament Bill section:\n{chunk}"
            }],
            temperature=0.3
        )
        partial.append(res.choices[0].message.content)

    combined = "\n".join(partial)

    final = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": """
STRICTLY use the following format:

### SECTOR
(one line)

### OBJECTIVE
- bullets

### SUMMARY
- bullets

### IMPACT
Citizens:
- bullets

Businesses:
- bullets

Government:
- bullets

Text:
""" + combined
        }],
        temperature=0.3
    )
    return final.choices[0].message.content

# ---------------- SECTION PARSER (IMPORTANT) ----------------
def parse_sections(text):
    def get_section(title):
        pattern = rf"### {title}(.*?)(###|$)"
        match = re.search(pattern, text, re.S | re.I)
        return match.group(1).strip() if match else "Not available"

    return {
        "sector": get_section("SECTOR"),
        "summary": get_section("SUMMARY"),
        "impact": get_section("IMPACT")
    }

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

if uploaded and st.button("🚀 Generate Analysis"):
    with st.spinner("Analyzing bill..."):
        raw = extract_text(uploaded)
        cleaned = clean_text(raw)
        st.session_state.bill_text = cleaned
        st.session_state.analysis = analyze_bill(cleaned)

# ---------------- DISPLAY ----------------
if st.session_state.analysis:
    sections = parse_sections(st.session_state.analysis)

    tab1, tab2, tab3 = st.tabs(["📊 Sector", "📝 Summary", "⚖️ Impact"])

    with tab1:
        st.subheader("📊 Sector Analysis")
        st.write(sections["sector"])

    with tab2:
        st.subheader("📝 Bill Summary")
        st.write(sections["summary"])

    with tab3:
        st.subheader("⚖️ Impact Analysis")
        st.write(sections["impact"])

    st.download_button(
        "📥 Download Full Summary PDF",
        make_pdf(st.session_state.analysis),
        "parliament_bill_summary.pdf",
        "application/pdf"
    )

# ---------------- ASK AI ----------------
st.markdown("---")
st.subheader("💬 Ask AI about this Bill")

question = st.text_input("Ask a question")

if st.button("Ask AI") and question:
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"Bill:\n{st.session_state.bill_text}\n\nQuestion:\n{question}"
        }],
        temperature=0.3
    )
    st.success(res.choices[0].message.content)
