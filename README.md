# SkillBridge
SkillBridge is an intelligent career assistant powered by AI that helps users analyze their profiles, plan career transitions, and compare CVs against job offers.

## Preview
![SkillBridge Preview](./assets/preview.png "SkillBridge")

## About
SkillBridge is a web application built with Streamlit and the Groq API (Llama 3). Unlike local LLM solutions that require expensive hardware, SkillBridge utilizes a **Cloud-First architecture** to provide instant, high-quality career guidance accessible from any device.

### How it works
1. **Upload PDF** → The user uploads a CV, and the system extracts raw text using `PyMuPDF` for high fidelity.
2. **Prompt Engineering** → The text is injected into specialized system prompts acting as an expert recruiter.
3. **Cloud Inference** → The data is sent to **Groq Cloud**, which processes the request using **Llama 3** models on LPU units for ultra-low latency.
4. **Strategic Analysis** → The AI performs complex reasoning (Gap Analysis, A/B Testing, or Skill Extraction).
5. **Result Rendering** → Streamlit displays the insights in a polished, custom-styled interface.

## Features to highlight
- **Smart Profile Analysis:** Automatically extracts Hard & Soft Skills and allows chatting with your CV.
- **Career Transition Plan:** Performs a "Gap Analysis" between your current profile and your target job, generating a personalized roadmap.
- **CV A/B Testing:** Upload two versions of a resume to mathematically determine which one fits a specific job offer better.
- **Cloud-First Performance:** Zero hardware requirements for the user; runs instantly via Groq API.
- **Modern UI:** Custom CSS implementation for a glassmorphism look and feel.

## Technologies
SkillBridge is built with:
- `Python`
- `Streamlit` for the frontend and state management (`session_state`)
- `Groq API` for ultra-fast cloud inference
- `Llama 3 (Meta)` as the underlying reasoning engine (70b & 8b models)
- `PyMuPDF (fitz)` for robust PDF text extraction
- `Base64` for efficient in-memory asset handling

## Installation
Clone the repository and install dependencies:

```bash
git clone [https://github.com/Nebrija-ia-bigdata/SkillBridge.git](https://github.com/Nebrija-ia-bigdata/SkillBridge.git)
cd SkillBridge
pip install -r requirements.txt