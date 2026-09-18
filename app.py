import os
import io
import time
import hashlib
import streamlit as st

from google import genai
from google.genai import types

# File readers
import PyPDF2
from docx import Document


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ReqPilot AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "file_text" not in st.session_state:
    st.session_state.file_text = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = ""


# ============================================================
# LIQUID GLASS UI
# ============================================================

st.markdown("""
<style>

/* ============================================================
   BACKGROUND
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 15% 15%,
            rgba(110, 90, 255, 0.30),
            transparent 30%
        ),
        radial-gradient(
            circle at 85% 15%,
            rgba(0, 200, 255, 0.22),
            transparent 30%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(255, 80, 190, 0.16),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #060810,
            #0b1020,
            #070a13
        );

    color: white;
}


/* ============================================================
   MAIN WIDTH
   ============================================================ */

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ============================================================
   HEADINGS
   ============================================================ */

h1 {
    font-size: 3.4rem !important;
    font-weight: 800 !important;
    letter-spacing: -2px;
}

h2 {
    font-weight: 750 !important;
}

h3 {
    font-weight: 700 !important;
}


/* ============================================================
   GLASS CONTAINERS
   ============================================================ */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.10),
            rgba(255,255,255,0.035)
        );

    border:
        1px solid rgba(255,255,255,0.14);

    border-radius: 26px;

    backdrop-filter:
        blur(28px)
        saturate(150%);

    -webkit-backdrop-filter:
        blur(28px)
        saturate(150%);

    box-shadow:
        0 20px 55px rgba(0,0,0,0.28),
        inset 0 1px 0 rgba(255,255,255,0.15),
        inset 0 -1px 0 rgba(255,255,255,0.03);
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {

    min-height: 48px;

    border-radius: 16px;

    border:
        1px solid rgba(255,255,255,0.16);

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.11),
            rgba(255,255,255,0.04)
        );

    color: white;

    font-weight: 700;

    transition:
        all 0.2s ease;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.13),
        0 8px 25px rgba(0,0,0,0.18);
}


.stButton > button:hover {

    transform: translateY(-2px);

    background:
        rgba(255,255,255,0.15);

    border-color:
        rgba(255,255,255,0.28);
}


/* ============================================================
   PRIMARY BUTTON
   ============================================================ */

.stButton > button[kind="primary"] {

    background:
        linear-gradient(
            135deg,
            #765cff,
            #00b8ff
        );

    border:
        1px solid rgba(255,255,255,0.25);

    box-shadow:
        0 12px 35px rgba(60,110,255,0.30);
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="input"] {

    background:
        rgba(255,255,255,0.055) !important;

    border:
        1px solid rgba(255,255,255,0.12) !important;

    border-radius: 15px !important;
}


div[data-baseweb="input"] input {
    color: white !important;
}


textarea {

    background:
        rgba(255,255,255,0.055) !important;

    color: white !important;

    border:
        1px solid rgba(255,255,255,0.12) !important;

    border-radius: 18px !important;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

section[data-testid="stFileUploaderDropzone"] {

    background:
        rgba(255,255,255,0.045);

    border:
        1px dashed rgba(255,255,255,0.22);

    border-radius: 20px;
}


/* ============================================================
   METRICS
   ============================================================ */

div[data-testid="stMetric"] {

    background:
        rgba(255,255,255,0.045);

    border:
        1px solid rgba(255,255,255,0.10);

    border-radius: 18px;

    padding: 15px;
}


/* ============================================================
   TABS
   ============================================================ */

button[data-baseweb="tab"] {

    color:
        rgba(255,255,255,0.65);

    font-weight: 650;
}


button[data-baseweb="tab"][aria-selected="true"] {
    color: white;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {

    background:
        rgba(5,7,15,0.90);

    border-right:
        1px solid rgba(255,255,255,0.08);
}


/* ============================================================
   CODE / READER
   ============================================================ */

.stCodeBlock {

    border-radius: 18px;
}


/* ============================================================
   DIVIDER
   ============================================================ */

hr {
    border-color:
        rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.write("")
    st.write("")
    st.write("")

    left, center, right = st.columns(
        [1, 1.5, 1]
    )

    with center:

        with st.container(border=True):

            st.markdown(
                """
                <h1 style="
                    text-align:center;
                    font-size:3.5rem;
                    margin-bottom:0;
                ">
                    🚀
                </h1>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <h2 style="text-align:center;">
                    ReqPilot AI
                </h2>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <p style="text-align:center;">
                    AI Requirements Engineering Agent
                </p>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            username = st.text_input(
                "Username",
                placeholder="Enter username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password"
            )

            passkey = st.text_input(
                "Passkey",
                type="password",
                placeholder="Enter passkey"
            )

            st.write("")

            login = st.button(
                "🔐 Sign In",
                type="primary",
                use_container_width=True
            )

            if login:

                # CHANGE THESE
                valid_username = "admin"
                valid_password = "reqpilot123"
                valid_passkey = "G14"

                if (
                    username == valid_username
                    and password == valid_password
                    and passkey == valid_passkey
                ):

                    st.session_state.logged_in = True

                    st.success(
                        "Login successful!"
                    )

                    time.sleep(0.5)

                    st.rerun()

                else:

                    st.error(
                        "Invalid login credentials."
                    )

            st.write("")

            st.caption(
                "Demo: admin / reqpilot123 / G14"
            )


# ============================================================
# FILE READER
# ============================================================

def read_txt(file):

    return file.getvalue().decode(
        "utf-8",
        errors="ignore"
    )


def read_csv(file):

    return file.getvalue().decode(
        "utf-8",
        errors="ignore"
    )


def read_json(file):

    return file.getvalue().decode(
        "utf-8",
        errors="ignore"
    )


def read_pdf(file):

    pdf_bytes = io.BytesIO(
        file.getvalue()
    )

    reader = PyPDF2.PdfReader(
        pdf_bytes
    )

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text
            text += "\n\n"

    return text


def read_docx(file):

    document = Document(
        io.BytesIO(
            file.getvalue()
        )
    )

    text = ""

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text += paragraph.text
            text += "\n\n"

    return text


def read_uploaded_file(file):

    filename = file.name.lower()

    if filename.endswith(".txt"):

        return read_txt(file)

    elif filename.endswith(".md"):

        return read_txt(file)

    elif filename.endswith(".csv"):

        return read_csv(file)

    elif filename.endswith(".json"):

        return read_json(file)

    elif filename.endswith(".pdf"):

        return read_pdf(file)

    elif filename.endswith(".docx"):

        return read_docx(file)

    else:

        return ""


# ============================================================
# AI ANALYSIS
# ============================================================

def analyze_document(document_text, api_key):

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
You are ReqPilot AI, an AI Requirements Engineering Agent.

Read the following software/project document carefully.

DOCUMENT:

{document_text}

Analyze the document as a professional software requirements engineer.

Return the result as a HUMAN-READABLE REPORT.

Do NOT return JSON.

Do NOT use programming syntax.

Create these sections:

1. PROJECT OVERVIEW

Give a short explanation of what the project is about.

2. FUNCTIONAL REQUIREMENTS

List all functional requirements found or inferred from the document.

3. NON-FUNCTIONAL REQUIREMENTS

Identify performance, security, reliability, usability,
scalability and other quality requirements.

4. USER STORIES

Create useful Agile user stories.

Format:

As a [user],
I want [function],
so that [benefit].

5. ACCEPTANCE CRITERIA

Give clear acceptance criteria for the important user stories.

6. MOSCOW PRIORITIZATION

Classify requirements as:

Must Have
Should Have
Could Have
Won't Have

Explain each classification briefly.

7. REQUIREMENT GAPS

Identify missing, unclear or ambiguous requirements.

8. TEST CASES

Generate practical test scenarios and expected results.

9. TECHNICAL DEPENDENCIES

Identify databases, APIs, authentication,
external services, hardware, software or other dependencies.

10. RECOMMENDATIONS

Give practical recommendations for improving
the requirements before development.

Use clean headings and bullet points.
Be concise but detailed enough for a development team.
"""

    response = client.models.generate_content(

        model="gemini-3.6-flash",

        contents=prompt
    )

    return response.text


# ============================================================
# MAIN APPLICATION
# ============================================================

if not st.session_state.logged_in:

    login_page()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🚀 ReqPilot")

    st.caption(
        "Requirements Intelligence"
    )

    st.divider()

    api_key = None

    try:

        api_key = st.secrets[
            "GEMINI_API_KEY"
        ]

        st.success(
            "Gemini API connected"
        )

    except Exception:

        api_key = st.text_input(
            "Gemini API Key",
            type="password"
        )

    st.divider()

    st.write(
        "📖 File Reader"
    )

    st.write(
        "🤖 AI Analysis"
    )

    st.write(
        "🧩 Requirements"
    )

    st.write(
        "👤 User Stories"
    )

    st.write(
        "🧪 Test Cases"
    )

    st.write(
        "🔎 Gap Detection"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.file_text = ""

        st.session_state.analysis = ""

        st.rerun()


# ============================================================
# HERO
# ============================================================

with st.container(border=True):

    st.caption(
        "G14 • REQUIREMENTS INTELLIGENCE"
    )

    st.title(
        "ReqPilot AI 🚀"
    )

    st.write(
        "Read your project document, understand the requirements, "
        "and convert them into a structured engineering report."
    )

    st.write(
        "📖 File Reader  •  🤖 AI Analysis  •  "
        "🧩 Requirements  •  🧪 Validation"
    )


# ============================================================
# FILE UPLOAD
# ============================================================

st.write("")

with st.container(border=True):

    st.subheader(
        "📂 Requirement File Reader"
    )

    st.write(
        "Upload your existing requirement document."
    )

    uploaded_file = st.file_uploader(

        "Choose a file",

        type=[
            "txt",
            "md",
            "csv",
            "json",
            "pdf",
            "docx"
        ],

        label_visibility="collapsed"
    )


# ============================================================
# FILE PROCESSING
# ============================================================

if uploaded_file:

    try:

        file_text = read_uploaded_file(
            uploaded_file
        )

        if not file_text.strip():

            st.error(
                "The file could not be read or contains no text."
            )

        else:

            st.session_state.file_text = file_text

            st.success(
                f"📖 Successfully read: {uploaded_file.name}"
            )

            # ==================================================
            # FILE INFORMATION
            # ==================================================

            word_count = len(
                file_text.split()
            )

            character_count = len(
                file_text
            )

            pages_info = "N/A"

            if uploaded_file.name.lower().endswith(".pdf"):

                try:

                    pdf_reader = PyPDF2.PdfReader(
                        io.BytesIO(
                            uploaded_file.getvalue()
                        )
                    )

                    pages_info = len(
                        pdf_reader.pages
                    )

                except Exception:

                    pages_info = "N/A"


            m1, m2, m3 = st.columns(3)

            with m1:

                st.metric(
                    "File",
                    uploaded_file.name
                )

            with m2:

                st.metric(
                    "Words",
                    word_count
                )

            with m3:

                st.metric(
                    "Pages",
                    pages_info
                )


            # ==================================================
            # READER VIEW
            # ==================================================

            st.write("")

            with st.container(border=True):

                st.subheader(
                    "📖 Reader Mode"
                )

                st.write(
                    "Extracted document content:"
                )

                st.text_area(

                    "Document Content",

                    value=file_text,

                    height=350,

                    label_visibility="collapsed"
                )


    except Exception as error:

        st.error(
            f"File reading error: {error}"
        )


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.session_state.file_text:

    st.write("")

    analyze_button = st.button(

        "🤖 Analyze Document with ReqPilot AI",

        type="primary",

        use_container_width=True
    )


    if analyze_button:

        if not api_key:

            st.error(
                "Gemini API key is required."
            )

        else:

            try:

                with st.spinner(
                    "🤖 ReqPilot is reading and analyzing your document..."
                ):

                    result = analyze_document(

                        st.session_state.file_text,

                        api_key
                    )

                    st.session_state.analysis = result


                st.success(
                    "✅ Analysis completed successfully!"
                )

            except Exception as error:

                error_message = str(error)

                if (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                ):

                    st.error(
                        "Gemini is temporarily unavailable. "
                        "Please try again."
                    )

                elif (
                    "429" in error_message
                    or "quota" in error_message.lower()
                ):

                    st.error(
                        "Gemini API quota/rate limit reached."
                    )

                else:

                    st.error(
                        f"AI Error: {error_message}"
                    )


# ============================================================
# ANALYSIS RESULT
# ============================================================

if st.session_state.analysis:

    st.write("")

    with st.container(border=True):

        st.subheader(
            "🧠 ReqPilot Analysis"
        )

        st.markdown(
            st.session_state.analysis
        )


# ============================================================
# QUICK FEATURES
# ============================================================

st.write("")

st.divider()

st.subheader(
    "✨ ReqPilot Workflow"
)

c1, c2, c3, c4 = st.columns(4)


with c1:

    with st.container(border=True):

        st.markdown(
            "### 📖"
        )

        st.write(
            "**Read**"
        )

        st.caption(
            "Extract content from project documents."
        )


with c2:

    with st.container(border=True):

        st.markdown(
            "### 🧠"
        )

        st.write(
            "**Understand**"
        )

        st.caption(
            "AI understands the project context."
        )


with c3:

    with st.container(border=True):

        st.markdown(
            "### 🧩"
        )

        st.write(
            "**Structure**"
        )

        st.caption(
            "Convert information into engineering requirements."
        )


with c4:

    with st.container(border=True):

        st.markdown(
            "### 🧪"
        )

        st.write(
            "**Validate**"
        )

        st.caption(
            "Generate gaps, test cases and recommendations."
        )


# ============================================================
# FOOTER
# ============================================================

st.write("")

st.caption(
    "ReqPilot AI • AI Requirements Engineering Agent • G14"
)
