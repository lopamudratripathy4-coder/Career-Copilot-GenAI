# Career Copilot — Local Generative AI Career Assistant

A Streamlit application for students and early-career applicants, powered by a locally hosted Ollama model.

## Features
- **Resume Review:** strengths, gaps, ATS keyword suggestions, and professional summary improvements.
- **Interview Preparation:** technical, project, and behavioural practice questions with answer guidance.
- **Professional Email:** structured professional email drafts with placeholders for missing details.
- **Learning Roadmap:** four-week objectives, tasks, exercises, portfolio project, and self-evaluation.

## Technology
Python, Streamlit, Ollama, Qwen3 1.7B (`qwen3:1.7b`), and Requests.

## Setup (Windows PowerShell)
```powershell
cd D:\GenAI_Career_Copilot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama pull qwen3:1.7b
python -m streamlit run app.py
```
Ensure Ollama is running. The default local server is `http://localhost:11434`.
In the app sidebar, use model name `qwen3:1.7b`. No Gemini API key is required.

## Testing
The local Ollama endpoint was tested from Python. The four app features were manually exercised with sample inputs. This is a basic functional check, not a formal accuracy or performance benchmark.

## Limitations and Responsible Use
Output quality and speed depend on local hardware and available memory. A small model can produce incomplete or incorrect information. Verify generated content before using it, and do not enter passwords or sensitive personal information. Model download requires internet access and disk space.

## Files
- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies
- `docs/Project_Report.docx` — project report
- `docs/Project_Presentation.pptx` — presentation
