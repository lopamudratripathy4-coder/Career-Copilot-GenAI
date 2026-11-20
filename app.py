import requests
import streamlit as st

st.set_page_config(page_title="Career Copilot | GenAI Project", page_icon="✨", layout="wide")

SYSTEM_RULES = """
You are Career Copilot, a professional Generative AI career assistant for students and early-career applicants.
Give accurate, constructive, realistic suggestions. Never invent qualifications, achievements, skills, or work experience.
Use only information supplied by the user, identify missing information, protect privacy, and organize responses clearly.
Never guarantee employment outcomes.
"""

PROMPTS = {
    "Resume review": """
You are an expert resume reviewer. Analyse the supplied resume information.
Provide: 1. Overall Resume Assessment 2. Strengths 3. Weaknesses and missing information
4. Section-wise Improvements 5. Five relevant ATS keywords, if supported by the background
6. An improved Professional Summary based only on supplied facts 7. Final Recommendations.
Do not invent achievements, qualifications, skills, or experience.
Resume information:
""",
    "Interview preparation": """
You are an experienced technical interviewer. Prepare an interview practice package
based on the candidate's background and target role. Include:
1. Eight likely interview questions 2. Technical questions 3. Project-related questions
4. Behavioural questions 5. What each question evaluates 6. Answer frameworks
7. Three follow-up questions. Do not fabricate experience. Label sample answers as examples
that the candidate must adapt truthfully.
Candidate information:
""",
    "Professional email": """
You are a professional communication assistant. Write a polished professional email.
Include: 1. Subject line 2. Greeting 3. Main message 4. Clear request or call to action
5. Professional closing. Do not invent names, dates, or commitments. Use [placeholders]
where details are missing.
Email context:
""",
    "Learning roadmap": """
You are an AI learning and career mentor. Create a practical four-week learning roadmap.
Include: 1. Weekly objectives 2. Realistic daily or weekly tasks 3. Recommended topics
4. Practical exercises 5. A small portfolio project 6. Self-evaluation checklist.
Keep the plan realistic. Do not claim that completing it guarantees a job.
Learning goal and current skill level:
""",
}

def check_ollama(base_url):
    try:
        response = requests.get(base_url.rstrip("/") + "/api/tags", timeout=5)
        response.raise_for_status()
        return True, response.json()
    except requests.RequestException:
        return False, None

def generate_response(prompt, base_url, model_name):
    url = base_url.rstrip("/") + "/api/generate"
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {"temperature": 0.4, "num_predict": 1800},
    }
    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Cannot connect to Ollama. Make sure Ollama is running. "
            "The default local address is http://localhost:11434."
        )
    except requests.exceptions.Timeout:
        raise RuntimeError(
            "The local model took too long to respond. Close other heavy apps "
            "or try again with shorter input."
        )
    except requests.exceptions.HTTPError as error:
        try:
            detail = response.json().get("error", "")
        except Exception:
            detail = ""
        raise RuntimeError(
            f"Ollama returned an error ({response.status_code}): {detail or error}"
        )
    except ValueError:
        raise RuntimeError("Ollama returned an invalid response.")

    result = data.get("response", "").strip()
    if not result:
        raise RuntimeError("The model returned an empty response. Please try again.")
    return result

st.title("✨ Career Copilot")
st.caption("Your local AI-powered career development assistant")
st.markdown(
    "Career Copilot uses Generative AI and Prompt Engineering to help students "
    "prepare for their professional careers. It runs through a locally hosted "
    "Ollama model and does not require a Gemini API key."
)
st.divider()

with st.sidebar:
    st.header("⚙️ Local AI Settings")
    ollama_url = st.text_input(
        "Ollama server address", value="http://localhost:11434"
    )
    model_name = st.text_input(
        "Model name",
        value="qwen3:1.7b",
        help="Use a model already downloaded in Ollama, such as qwen3:1.7b.",
    ).strip()
    st.divider()

    connected, ollama_data = check_ollama(ollama_url)
    if connected:
        st.success("Ollama server connected")
        installed_models = [
            item.get("name", "")
            for item in ollama_data.get("models", [])
            if item.get("name")
        ]
        if model_name in installed_models:
            st.caption(f"Model available: {model_name}")
        else:
            st.warning(f"{model_name} was not found in the local model list.")
            if installed_models:
                st.caption("Installed models: " + ", ".join(installed_models))
    else:
        st.error("Ollama server not reachable")
        st.caption("Open Ollama or start its service, then refresh this page.")

    st.divider()
    st.success("Four AI tools available")
    st.caption("Avoid entering passwords, financial details, or other sensitive information.")
    st.caption("Verify AI-generated content before using it.")

task = st.selectbox("Choose Your AI Tool", list(PROMPTS.keys()))

if task == "Resume review":
    st.subheader("📄 AI Resume Reviewer")
    context = st.text_area(
        "Paste your resume information", height=260,
        placeholder="Education, skills, projects, internships, achievements..."
    )
elif task == "Interview preparation":
    st.subheader("🎯 AI Interview Preparation")
    context = st.text_area(
        "Enter your target role and background", height=240,
        placeholder="Target role: Python Developer\nSkills: Python, SQL\nProjects: ..."
    )
elif task == "Professional email":
    st.subheader("✉️ Professional Email Generator")
    context = st.text_area(
        "Describe the email you want to write", height=220,
        placeholder="Purpose, recipient's role, key details, and desired tone..."
    )
else:
    st.subheader("📚 AI Learning Roadmap")
    context = st.text_area(
        "Describe your learning goal", height=220,
        placeholder="Goal: Learn Generative AI\nCurrent level: Beginner\nTime available: ..."
    )

if st.button("✨ Generate", type="primary", use_container_width=True):
    if not context.strip():
        st.warning("Please enter some information first.")
    elif not model_name:
        st.error("Please enter an Ollama model name.")
    else:
        full_prompt = SYSTEM_RULES + "\n\n" + PROMPTS[task] + "\n\n" + context.strip()
        with st.spinner(f"Generating with local model {model_name}..."):
            try:
                result = generate_response(full_prompt, ollama_url, model_name)
                st.session_state["last_result"] = result
                st.session_state["last_task"] = task
                st.session_state["used_model"] = model_name
            except Exception as error:
                st.error(str(error))

if "last_result" in st.session_state:
    st.divider()
    st.subheader("📌 Generated Result")
    st.caption("Task: " + st.session_state.get("last_task", ""))
    st.caption("Local model: " + st.session_state.get("used_model", ""))
    st.markdown(st.session_state["last_result"])
    st.download_button(
        label="⬇️ Download Result",
        data=st.session_state["last_result"],
        file_name="Career_Copilot_Result.txt",
        mime="text/plain",
    )

st.divider()
st.markdown(
    """
### Responsible AI
Career Copilot supports career development. Verify AI-generated information before using it.

**Developed using Python, Streamlit, Ollama, Qwen3 and Prompt Engineering.**

*The model runs locally on your computer. Response speed and quality depend on available memory and hardware.*
"""
)
