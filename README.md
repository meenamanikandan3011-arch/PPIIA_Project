🏛️ Parliament Bill Auditor AI-Powered Public Policy Analysis Platform

📌 Project Overview
  Parliament Bill Auditor is an AI-driven application that analyzes Indian Parliament Bills (PDF format) and generates structured, easy-to-understand policy insights. The platform assists students, researchers, policymakers, and analysts in quickly understanding the sector, objectives, summaries, and policy impacts of legislative documents.
The system leverages LLM-powered summarization, PDF text extraction, and an interactive Streamlit dashboard to convert complex legal text into actionable insights.

🎯 Key Objectives
1. Simplify complex legislative documents
2. Provide structured policy analysis
3. Enable quick impact assessment
4. Support public policy research and learning

🚀 Features
  📄 Upload Parliament Bills (PDF)
  🧠 AI-Powered Policy Analysis
  📊 Sector Identification
  📝 Clear & Structured Summary
  ⚖️ Short / Medium / Long-term Impact Analysis
  💬 Ask AI questions about the bill
  📥 Download summary as PDF
  🌙 Clean, professional Streamlit UI

🧩 System Architecture
          PDF Upload
              ↓
      Text Extraction (PyMuPDF)
              ↓
      Text Cleaning & Chunking
              ↓
      LLM Summarization (Groq)
              ↓
      Structured Policy Analysis
              ↓
      Interactive Streamlit Dashboard

🖥️ Application Workflow
  1. User uploads a Parliament Bill (PDF)
  2. System extracts and cleans text
  3. Bill text is split into manageable chunks
  4. AI summarizes each chunk
  5. A final structured policy analysis is generated
  6. Results are displayed in tabs:
     *Sector
     *Summary
     *Impact
  7. Users can ask follow-up questions
  8. Analysis can be downloaded as a PDF

📂 Project Structure
PPIIA_Project/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation

🔐 Environment Setup
  1. This project uses secure API key management.
  2. Streamlit Secrets
  3. Add the following in Streamlit Cloud → Secrets:
     GROQ_API_KEY = "your_groq_api_key_here"

👤 Author
Santhameena Manikandan
Data Science & AI Enthusiast
Project: Public Policy Insight & Impact Analyzer (PPIIA)
