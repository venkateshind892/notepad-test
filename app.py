```python
import streamlit as st
import json
import time
from google import genai
from google.genai import types


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ReqPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None


# ============================================================
# GLASSMORPHISM UI
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(120, 80, 255, 0.25),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(0, 200, 255, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(255, 0, 180, 0.12),
                transparent 35%
            ),
            #070910;

        color: white;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 24px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);

        box-shadow:
            0 10px 40px rgba(0,0,0,0.28),
            inset 0 1px 0 rgba(255,255,255,0.08);
    }

    h1 {
        font-weight: 800 !important;
        letter-spacing: -2px;
    }

    h2, h3 {
        font-weight: 750 !important;
    }

    .stButton > button {
        border-radius: 15px;
        min-height: 46px;

        background: rgba(255,255,255,0.07);
        color: white;

        border: 1px solid rgba(255,255,255,0.14);

        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: rgba(255,255,255,0.14);
        border-color: rgba(255,255,255,0.25);
        transform: translateY(-1px);
    }

    .stButton > button[kind="primary"] {
        background:
            linear-gradient(
                135deg,
                rgba(120,80,255,0.90),
                rgba(0,180,255,0.80)
            );
    }

    .stTextInput input,
    .stTextArea textarea {
        background: rgba(255,255,255,0.055) !important;
        color: white !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(5,7,15,0.88);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 16px;
        padding: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.authenticated:

    st.markdown("<br><br>", unsafe_allow_html=True)

    left, center, right = st.columns(
        [1, 1.4, 1]
    )

    with center:

        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    text-align:center;
                    padding:20px 0;
                ">
                    <div style="font-size:55px;">
                        🚀
                    </div>

                    <h1>
                        ReqPilot
                    </h1>

                    <p>
                        AI Requirements Engineering Agent
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.divider()

            username = st.text_input(
                "👤 Username",
                placeholder="Enter username"
            )

            password = st.text_input(
                "🔐 Password",
                type="password",
                placeholder="Enter password"
            )

            st.write("")

            login = st.button(
                "🚀 Login to ReqPilot",
                type="primary",
                use_container_width=True
            )

            if login:

                if (
                    username == "reqpilot"
                    and password == "reqpilot123"
                ):

                    st.session_state.authenticated = True

                    st.success(
                        "Login successful!"
                    )

                    time.sleep(0.5)

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password."
                    )

            st.write("")

            st.caption(
                "Authorized users only"
            )

    st.stop()


# ============================================================
# GEMINI CONNECTION
# ============================================================

def get_api_key():

    try:

        return st.secrets[
            "GEMINI_API_KEY"
        ]

    except Exception:

        return st.session_state.get(
            "api_key"
        )


# ============================================================
# GEMINI CLIENT
# ============================================================

def get_client():

    api_key = get_api_key()

    if not api_key:

        return None

    return genai.Client(
        api_key=api_key
    )


# ============================================================
# GENERAL AI CHAT
# ============================================================

def ask_ai(question):

    client = get_client()

    if client is None:

        return (
            "⚠️ Gemini API key is not configured.\n\n"
            "Add GEMINI_API_KEY in Streamlit secrets "
            "or enter it from the sidebar."
        )

    prompt = f"""
You are ReqPilot, an advanced AI Requirements Engineering
and software development assistant.

You can answer both:

1. Software engineering questions
2. General questions

For software/project questions, provide structured,
practical answers.

For requirements engineering tasks, help with:

- Functional requirements
- Non-functional requirements
- User stories
- Acceptance criteria
- MoSCoW prioritization
- Requirement gaps
- Ambiguity detection
- Test cases
- Technical dependencies
- SRS
- UML
- System architecture
- API design
- Database design
- Software development planning

User question:

{question}

Answer clearly and accurately.
Use headings and bullet points when useful.
Do not unnecessarily mention that you are an AI.
"""

    try:

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"❌ AI Error: {e}"


# ============================================================
# REQUIREMENT ANALYZER
# ============================================================

def analyze_requirements(idea):

    client = get_client()

    if client is None:

        return None

    prompt = f"""
You are ReqPilot's Requirements Engineering Engine.

Analyze this product idea:

{idea}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "functional_requirements": [],
    "non_functional_requirements": [],
    "user_stories": [
        {{
            "story": "",
            "acceptance_criteria": []
        }}
    ],
    "priorities": [
        {{
            "requirement": "",
            "priority": "",
            "reason": ""
        }}
    ],
    "ambiguities": [],
    "test_cases": [
        {{
            "id": "",
            "scenario": "",
            "expected": ""
        }}
    ],
    "technical_dependencies": []
}}

Requirements:

- Extract functional requirements.
- Extract non-functional requirements.
- Generate realistic user stories.
- Generate acceptance criteria.
- Use MoSCoW prioritization.
- Detect ambiguous or missing requirements.
- Generate practical test cases.
- Identify technical dependencies.
- Do not invent unnecessary functionality.
"""

    try:

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt,

            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        return json.loads(
            response.text
        )

    except Exception as e:

        st.error(
            f"❌ Requirement analysis failed: {e}"
        )

        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 🚀 ReqPilot"
    )

    st.caption(
        "AI Requirements Engineering Agent"
    )

    st.divider()

    st.subheader(
        "🔑 AI Configuration"
    )

    try:

        secret_key = st.secrets[
            "GEMINI_API_KEY"
        ]

        st.success(
            "Gemini API connected"
        )

    except Exception:

        api_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Paste your API key"
        )

        if api_key_input:

            st.session_state.api_key = (
                api_key_input
            )

            st.success(
                "API key added"
            )

    st.divider()

    st.subheader(
        "⚙️ ReqPilot Modules"
    )

    st.write(
        "💬 AI Chat"
    )

    st.write(
        "📋 Requirements"
    )

    st.write(
        "👤 User Stories"
    )

    st.write(
        "⚡ Prioritization"
    )

    st.write(
        "🔎 Gap Detection"
    )

    st.write(
        "🧪 Test Cases"
    )

    st.write(
        "🔧 Technical Dependencies"
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.authenticated = False

        st.session_state.messages = []

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

with st.container(border=True):

    st.markdown(
        "## 🚀 ReqPilot AI"
    )

    st.write(
        "Your AI-powered Requirements Engineering workspace."
    )

    st.caption(
        "Ask questions, analyze ideas, generate requirements "
        "and validate software specifications."
    )


# ============================================================
# TOP METRICS
# ============================================================

st.write("")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "AI Engine",
        "Gemini"
    )

with m2:

    st.metric(
        "Modules",
        "7"
    )

with m3:

    st.metric(
        "Mode",
        "AI + RE"
    )

with m4:

    st.metric(
        "Status",
        "Online"
    )


# ============================================================
# TABS
# ============================================================

st.write("")

chat_tab, requirement_tab = st.tabs(
    [
        "💬 AI Assistant",
        "🧠 Requirement Analyzer"
    ]
)


# ============================================================
# AI CHAT
# ============================================================

with chat_tab:

    st.subheader(
        "💬 Ask ReqPilot Anything"
    )

    st.caption(
        "Requirements questions, coding doubts, "
        "software architecture, project ideas or general questions."
    )

    # Display previous messages

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    question = st.chat_input(
        "Ask ReqPilot anything..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message(
            "user"
        ):

            st.markdown(
                question
            )

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Thinking..."
            ):

                answer = ask_ai(
                    question
                )

            st.markdown(
                answer
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )


# ============================================================
# REQUIREMENT ANALYZER
# ============================================================

with requirement_tab:

    st.subheader(
        "🧠 AI Requirement Analyzer"
    )

    st.write(
        "Enter your project idea and ReqPilot will convert "
        "it into structured software requirements."
    )

    product_idea = st.text_area(
        "Project / Product Idea",
        height=180,
        placeholder=(
            "Example:\n\n"
            "We want to build an AI-based platform "
            "where students can upload study materials, "
            "ask questions, generate quizzes and track progress."
        )
    )

    analyze_button = st.button(
        "⚡ Generate Requirements",
        type="primary",
        use_container_width=True
    )

    if analyze_button:

        if not product_idea.strip():

            st.warning(
                "⚠️ Enter a project idea first."
            )

        elif not get_api_key():

            st.error(
                "❌ Gemini API key is required."
            )

        else:

            with st.spinner(
                "🤖 ReqPilot is analyzing your project..."
            ):

                result = analyze_requirements(
                    product_idea
                )

            if result:

                st.session_state.analysis_result = (
                    result
                )

                st.success(
                    "✅ Requirements generated successfully!"
                )


# ============================================================
# DISPLAY REQUIREMENT RESULTS
# ============================================================

result = st.session_state.analysis_result

if result:

    st.write("")

    st.subheader(
        "📊 Requirement Intelligence Report"
    )

    r1, r2, r3, r4, r5, r6 = st.tabs(
        [
            "📋 Requirements",
            "👤 Stories",
            "⚡ Priority",
            "🔎 Gaps",
            "🧪 Tests",
            "🔧 Technical"
        ]
    )


    # --------------------------------------------------------
    # REQUIREMENTS
    # --------------------------------------------------------

    with r1:

        st.markdown(
            "### Functional Requirements"
        )

        functional = result.get(
            "functional_requirements",
            []
        )

        for index, item in enumerate(
            functional,
            1
        ):

            with st.container(
                border=True
            ):

                st.write(
                    f"**FR-{index:02d}**"
                )

                st.write(item)


        st.markdown(
            "### Non-Functional Requirements"
        )

        non_functional = result.get(
            "non_functional_requirements",
            []
        )

        for index, item in enumerate(
            non_functional,
            1
        ):

            with st.container(
                border=True
            ):

                st.write(
                    f"**NFR-{index:02d}**"
                )

                st.write(item)


    # --------------------------------------------------------
    # USER STORIES
    #
```
```python
import streamlit as st


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="ReqPilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==========================================================
# PREMIUM GLASS UI
# ==========================================================

st.markdown(
    """
    <style>

    /* ---------- MAIN BACKGROUND ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 15%,
                rgba(116, 72, 255, 0.30),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(0, 190, 255, 0.20),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 90%,
                rgba(255, 70, 180, 0.16),
                transparent 35%
            ),
            #060812;

        color: #ffffff;
    }


    /* ---------- REMOVE DEFAULT TOP SPACE ---------- */

    .block-container {
        max-width: 1350px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ---------- GLASS CONTAINERS ---------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.10),
                rgba(255,255,255,0.035)
            );

        border:
            1px solid rgba(255,255,255,0.14);

        border-radius: 28px;

        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);

        box-shadow:
            0 20px 60px rgba(0,0,0,0.30),
            inset 0 1px 0 rgba(255,255,255,0.10);

        padding: 12px;
    }


    /* ---------- HEADINGS ---------- */

    h1 {
        font-size: 3.3rem !important;
        font-weight: 800 !important;
        letter-spacing: -2px;
    }

    h2 {
        font-weight: 750 !important;
    }

    h3 {
        font-weight: 700 !important;
    }


    /* ---------- NORMAL TEXT ---------- */

    p {
        color: rgba(245,248,255,0.78);
    }


    /* ---------- INPUT BOX ---------- */

    .stTextInput input,
    .stTextArea textarea {

        background:
            rgba(255,255,255,0.055) !important;

        color: white !important;

        border:
            1px solid rgba(255,255,255,0.13) !important;

        border-radius: 17px !important;

        backdrop-filter: blur(15px);

    }


    .stTextInput input:focus,
    .stTextArea textarea:focus {

        border:
            1px solid rgba(120,170,255,0.65) !important;

        box-shadow:
            0 0 20px rgba(90,120,255,0.18);

    }


    /* ---------- BUTTONS ---------- */

    .stButton > button {

        min-height: 48px;

        border-radius: 16px;

        background:
            rgba(255,255,255,0.065);

        color: white;

        border:
            1px solid rgba(255,255,255,0.14);

        font-weight: 650;

        transition:
            all 0.2s ease;

    }


    .stButton > button:hover {

        background:
            rgba(255,255,255,0.13);

        border:
            1px solid rgba(255,255,255,0.25);

        transform:
            translateY(-2px);

        box-shadow:
            0 10px 30px rgba(0,0,0,0.25);

    }


    /* ---------- PRIMARY BUTTON ---------- */

    .stButton > button[kind="primary"] {

        background:
            linear-gradient(
                135deg,
                rgba(116,75,255,0.90),
                rgba(0,180,255,0.82)
            );

        border:
            1px solid rgba(255,255,255,0.20);

        box-shadow:
            0 8px 30px rgba(70,100,255,0.25);

    }


    /* ---------- METRICS ---------- */

    div[data-testid="stMetric"] {

        background:
            rgba(255,255,255,0.045);

        border:
            1px solid rgba(255,255,255,0.10);

        border-radius: 20px;

        padding: 15px;

    }


    /* ---------- TABS ---------- */

    button[data-baseweb="tab"] {

        color:
            rgba(255,255,255,0.60);

        font-weight:
            600;

    }


    button[data-baseweb="tab"][aria-selected="true"] {

        color:
            white;

    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {

        background:
            rgba(5,7,16,0.90);

        border-right:
            1px solid rgba(255,255,255,0.08);

        backdrop-filter:
            blur(25px);

    }


    /* ---------- CHAT MESSAGE ---------- */

    div[data-testid="stChatMessage"] {

        background:
            rgba(255,255,255,0.045);

        border:
            1px solid rgba(255,255,255,0.08);

        border-radius:
            20px;

        margin-bottom:
            12px;

    }


    /* ---------- DIVIDER ---------- */

    hr {

        border-color:
            rgba(255,255,255,0.08);

    }


    /* ---------- LOGIN CARD ---------- */

    .login-title {

        text-align: center;

        font-size: 54px;

        font-weight: 800;

        margin-bottom: 0;

    }

    .login-subtitle {

        text-align: center;

        color:
            rgba(255,255,255,0.60);

        font-size: 15px;

        margin-bottom: 25px;

    }


    /* ---------- GLASS BADGE ---------- */

    .glass-badge {

        display: inline-block;

        padding: 8px 14px;

        border-radius: 30px;

        background:
            rgba(255,255,255,0.07);

        border:
            1px solid rgba(255,255,255,0.12);

        color:
            rgba(255,255,255,0.80);

        font-size: 13px;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# LOGIN PAGE
# ==========================================================

if not st.session_state.logged_in:

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    left, center, right = st.columns(
        [1, 1.35, 1]
    )

    with center:

        with st.container(border=True):

            st.markdown(
                """
                <div class="login-title">
                    🚀
                </div>

                <h1 style="text-align:center;">
                    ReqPilot
                </h1>

                <div class="login-subtitle">
                    AI Requirements Engineering Agent
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style="
                    text-align:center;
                    margin-bottom:20px;
                ">
                    <span class="glass-badge">
                        🔐 Secure Workspace
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            username = st.text_input(
                "👤 Username",
                placeholder="Enter your username"
            )

            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter your password"
            )

            st.write("")

            if st.button(
                "🚀 Continue to ReqPilot",
                type="primary",
                use_container_width=True
            ):

                if (
                    username == "reqpilot"
                    and password == "reqpilot123"
                ):

                    st.session_state.logged_in = True

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

            st.write("")

            st.caption(
                "Demo: reqpilot / reqpilot123"
            )

    st.stop()


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        "## 🚀 ReqPilot"
    )

    st.caption(
        "AI Requirements Engineering"
    )

    st.divider()

    st.markdown(
        "### 🧭 Workspace"
    )

    st.write(
        "💬 AI Assistant"
    )

    st.write(
        "🧠 Requirement Analyzer"
    )

    st.write(
        "📋 User Stories"
    )

    st.write(
        "⚡ Prioritization"
    )

    st.write(
        "🔎 Gap Detection"
    )

    st.write(
        "🧪 Test Cases"
    )

    st.write(
        "🔧 Dependencies"
    )

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.messages = []

        st.rerun()


# ==========================================================
# MAIN HEADER
# ==========================================================

with st.container(border=True):

    c1, c2 = st.columns(
        [4, 1]
    )

    with c1:

        st.markdown(
            "# 🚀 ReqPilot"
        )

        st.write(
            "AI-powered requirements engineering workspace."
        )

    with c2:

        st.markdown(
            """
            <div style="
                text-align:right;
                padding-top:20px;
            ">
                <span class="glass-badge">
                    🟢 AI ONLINE
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================================
# METRICS
# ==========================================================

st.write("")

a, b, c, d = st.columns(4)

with a:

    st.metric(
        "AI Engine",
        "Gemini"
    )

with b:

    st.metric(
        "Modules",
        "7"
    )

with c:

    st.metric(
        "Workspace",
        "Active"
    )

with d:

    st.metric(
        "Mode",
        "AI + RE"
    )


# ==========================================================
# MAIN TABS
# ==========================================================

st.write("")

chat_tab, analyzer_tab = st.tabs(
    [
        "💬 AI Assistant",
        "🧠 Requirement Analyzer"
    ]
)


# ==========================================================
# AI ASSISTANT
# ==========================================================

with chat_tab:

    with st.container(border=True):

        st.markdown(
            "## 💬 Ask ReqPilot"
        )

        st.caption(
            "Ask questions about requirements, coding, "
            "software engineering, projects or general topics."
        )

        st.divider()

        if not st.session_state.messages:

            st.markdown(
                """
                ### 👋 Welcome to ReqPilot

                You can ask things like:

                • What is a functional requirement?

                • Generate requirements for an AI project.

                • Explain SRS.

                • Create user stories for my application.

                • What is the difference between FR and NFR?

                • Help me design my project architecture.
                """
            )

        else:

            for message in st.session_state.messages:

                with st.chat_message(
                    message["role"]
                ):

                    st.markdown(
                        message["content"]
                    )

        question = st.chat_input(
            "Ask ReqPilot anything..."
        )

        if question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message(
                "user"
            ):

                st.markdown(
                    question
                )

            # Frontend placeholder response.
            # Connect Gemini backend here.

            with st.chat_message(
                "assistant"
            ):

                response = (
                    "🤖 ReqPilot received your question.\n\n"
                    "Connect your Gemini backend to generate "
                    "the real AI response."
                )

                st.markdown(
                    response
                )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )


# ==========================================================
# REQUIREMENT ANALYZER
# ==========================================================

with analyzer_tab:

    with st.container(border=True):

        st.markdown(
            "## 🧠 Requirement Analyzer"
        )

        st.caption(
            "Convert your raw product idea into structured requirements."
        )

        st.divider()

        project_idea = st.text_area(
            "💡 Product Idea",
            placeholder=(
                "Describe your project here..."
            ),
            height=180
        )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:

            st.button(
                "📋 Extract Requirements",
                type="primary",
                use_container_width=True
            )

        with col2:

            st.button(
                "🧹 Clear",
                use_container_width=True
            )


# ==========================================================
# PIPELINE
# ==========================================================

st.write("")

st.markdown(
    "## ⚙️ ReqPilot Pipeline"
)

pipeline = [

    ("💡", "Idea", "Raw Input"),

    ("🧩", "Extract", "Requirements"),

    ("🏷️", "Classify", "FR / NFR"),

    ("⚡", "Prioritize", "MoSCoW"),

    ("🔎", "Detect", "Gaps"),

    ("🧪", "Validate", "Test Cases")

]

columns = st.columns(
    len(pipeline)
)

for column, item in zip(
    columns,
    pipeline
):

    icon, title, subtitle = item

    with column:

        with st.container(border=True):

            st.markdown(
                f"## {icon}"
            )

            st.write(
                f"**{title}**"
            )

            st.caption(
                subtitle
            )


# ==========================================================
# FOOTER
# ==========================================================

st.write("")

with st.container(border=True):

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px;
        ">
            <b>🚀 ReqPilot</b>
            <br>
            <span style="
                color:rgba(255,255,255,0.5);
            ">
                AI Requirements Engineering Agent
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
```
