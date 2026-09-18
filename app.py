import json
import time
import hashlib
import streamlit as st
from google import genai
from google.genai import types


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ReqPilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None


# ============================================================
# LIQUID GLASS UI
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(112, 92, 255, 0.30),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(0, 200, 255, 0.22),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 90%,
                rgba(255, 90, 190, 0.16),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #070912 0%,
                #0b1020 50%,
                #080b15 100%
            );

        color: #ffffff;
        min-height: 100vh;
    }


    .block-container {
        max-width: 1250px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }


    /* ======================================================
       TEXT
       ====================================================== */

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

    p {
        color: rgba(245, 247, 255, 0.78);
    }


    /* ======================================================
       GLASS CONTAINERS
       ====================================================== */

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

        backdrop-filter: blur(25px) saturate(150%);
        -webkit-backdrop-filter: blur(25px) saturate(150%);

        box-shadow:
            0 18px 50px rgba(0,0,0,0.25),
            inset 0 1px 0 rgba(255,255,255,0.15),
            inset 0 -1px 0 rgba(255,255,255,0.03);

        overflow: hidden;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {

        min-height: 48px;

        border-radius: 16px;

        border:
            1px solid rgba(255,255,255,0.15);

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.11),
                rgba(255,255,255,0.04)
            );

        color: white;

        font-weight: 700;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.13),
            0 8px 25px rgba(0,0,0,0.16);

        transition:
            transform 0.2s ease,
            background 0.2s ease,
            border 0.2s ease;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.17),
                rgba(255,255,255,0.07)
            );

        border-color:
            rgba(255,255,255,0.28);
    }


    /* ======================================================
       PRIMARY BUTTON
       ====================================================== */

    .stButton > button[kind="primary"] {

        background:
            linear-gradient(
                135deg,
                rgba(116, 88, 255, 0.95),
                rgba(0, 190, 255, 0.85)
            );

        border:
            1px solid rgba(255,255,255,0.25);

        box-shadow:
            0 10px 35px rgba(80,100,255,0.30),
            inset 0 1px 0 rgba(255,255,255,0.25);
    }


    /* ======================================================
       TEXT INPUT
       ====================================================== */

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


    /* ======================================================
       TEXT AREA
       ====================================================== */

    textarea {

        background:
            rgba(255,255,255,0.055) !important;

        color: white !important;

        border:
            1px solid rgba(255,255,255,0.12) !important;

        border-radius: 18px !important;
    }


    /* ======================================================
       SELECT BOX
       ====================================================== */

    div[data-baseweb="select"] > div {

        background:
            rgba(255,255,255,0.055) !important;

        border:
            1px solid rgba(255,255,255,0.12) !important;

        border-radius: 14px !important;

        color: white !important;
    }


    /* ======================================================
       METRICS
       ====================================================== */

    div[data-testid="stMetric"] {

        background:
            rgba(255,255,255,0.045);

        border:
            1px solid rgba(255,255,255,0.09);

        border-radius: 18px;

        padding: 15px;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.08);
    }


    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {

        color:
            rgba(255,255,255,0.62);

        font-weight: 650;
    }


    button[data-baseweb="tab"][aria-selected="true"] {

        color: white;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {

        background:
            rgba(6,8,17,0.88);

        border-right:
            1px solid rgba(255,255,255,0.08);
    }


    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {

        border-color:
            rgba(255,255,255,0.08);
    }


    /* ======================================================
       DOWNLOAD BUTTON
       ====================================================== */

    .stDownloadButton > button {

        width: 100%;

        min-height: 48px;

        border-radius: 15px;

        background:
            rgba(255,255,255,0.07);

        color: white;

        border:
            1px solid rgba(255,255,255,0.14);

        font-weight: 700;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.write("")
    st.write("")
    st.write("")

    left, center, right = st.columns([1, 1.5, 1])

    with center:

        with st.container(border=True):

            st.markdown(
                """
                <h1 style="
                    text-align:center;
                    font-size:3rem;
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
                    ReqPilot
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
                placeholder="Enter access passkey"
            )

            st.write("")

            login = st.button(
                "🔐 Sign In",
                type="primary",
                use_container_width=True
            )

            if login:

                # ------------------------------------------------
                # CHANGE THESE CREDENTIALS
                # ------------------------------------------------

                correct_username = "admin"
                correct_password = "reqpilot123"
                correct_passkey = "G14"

                if (
                    username == correct_username
                    and password == correct_password
                    and passkey == correct_passkey
                ):

                    st.session_state.logged_in = True

                    st.success(
                        "Login successful. Welcome to ReqPilot!"
                    )

                    time.sleep(0.7)

                    st.rerun()

                else:

                    st.error(
                        "Invalid username, password, or passkey."
                    )

            st.write("")

            st.caption(
                "Demo credentials: admin / reqpilot123 / G14"
            )


# ============================================================
# DEMO DATA
# ============================================================

demo_data = {

    "functional_requirements": [

        "Users should be able to create an account and securely log in.",

        "Users should be able to browse groceries by category.",

        "Users should be able to search for grocery products.",

        "Users should be able to add products to a shopping cart.",

        "Users should be able to update product quantities.",

        "Users should be able to place orders.",

        "Users should be able to make online payments.",

        "Users should be able to track delivery status.",

        "The system should send order notifications."
    ],

    "non_functional_requirements": [

        "User credentials and payment information must be protected.",

        "The system should respond quickly under normal operating conditions.",

        "The application should support multiple concurrent users.",

        "The service should maintain high availability.",

        "The system should securely communicate with external payment services."
    ],

    "user_stories": [

        {
            "story":
            "As a customer, I want to search for groceries so that I can quickly find the products I need.",

            "acceptance_criteria": [

                "Given the user is on the product page, when they search for a product, matching products should be displayed.",

                "Given no product matches the search, when the user submits the search, a suitable message should be displayed."
            ]
        },

        {
            "story":
            "As a customer, I want to add products to my cart so that I can purchase multiple items together.",

            "acceptance_criteria": [

                "Given a product is available, when the user selects Add to Cart, the product should appear in the cart.",

                "The cart should correctly display product quantity and total price."
            ]
        },

        {
            "story":
            "As a customer, I want to track my order so that I know when my groceries will arrive.",

            "acceptance_criteria": [

                "Given an order exists, when the user opens tracking, the current delivery status should be displayed.",

                "The user should receive an update when the delivery status changes."
            ]
        }
    ],

    "priorities": [

        {
            "requirement": "User registration and login",
            "priority": "Must Have",
            "reason":
            "Authentication is required for managing user accounts and orders."
        },

        {
            "requirement": "Product browsing and search",
            "priority": "Must Have",
            "reason":
            "Customers need to discover products before purchasing."
        },

        {
            "requirement": "Shopping cart",
            "priority": "Must Have",
            "reason":
            "The cart is part of the core purchasing workflow."
        },

        {
            "requirement": "Online payment",
            "priority": "Must Have",
            "reason":
            "Payment is required to complete online purchases."
        },

        {
            "requirement": "Order tracking",
            "priority": "Should Have",
            "reason":
            "Tracking provides visibility into delivery progress."
        },

        {
            "requirement": "Personalized recommendations",
            "priority": "Could Have",
            "reason":
            "Recommendations can improve discovery but are not essential to the core workflow."
        }
    ],

    "ambiguities": [

        "Which payment methods should be supported?",

        "Which geographical areas should the service support?",

        "What happens when a product becomes unavailable during checkout?",

        "Can customers cancel orders after payment?",

        "What delivery time window should be supported?",

        "Which notification channels should be supported?"
    ],

    "test_cases": [

        {
            "id": "TC-01",
            "scenario": "User searches for an available grocery product.",
            "expected":
            "Matching products should be displayed."
        },

        {
            "id": "TC-02",
            "scenario": "User adds a product to the cart.",
            "expected":
            "The product should appear in the cart with the correct quantity and price."
        },

        {
            "id": "TC-03",
            "scenario": "User completes checkout successfully.",
            "expected":
            "An order should be created and confirmation should be displayed."
        },

        {
            "id": "TC-04",
            "scenario": "Payment fails during checkout.",
            "expected":
            "The order should not be confirmed."
        },

        {
            "id": "TC-05",
            "scenario": "User checks an existing order.",
            "expected":
            "The current delivery status should be displayed."
        }
    ],

    "technical_dependencies": [

        "Authentication service",

        "Product and inventory database",

        "Order management backend",

        "Payment gateway",

        "Delivery tracking service",

        "Notification service",

        "Frontend application"
    ]
}


# ============================================================
# GEMINI PROMPT
# ============================================================

def build_prompt(idea):

    return f"""
You are ReqPilot, an AI Requirements Engineering Agent.

Analyze this software product idea:

{idea}

Return ONLY valid JSON.

Use exactly this schema:

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
- Create realistic Agile user stories.
- Add acceptance criteria.
- Use MoSCoW priorities.
- Identify missing requirements and ambiguities.
- Generate practical test cases.
- Identify technical dependencies.
- Do not invent unnecessary features.
- Keep the result concise.
"""


# ============================================================
# GEMINI FUNCTION
# ============================================================

def analyze_with_gemini(idea, api_key):

    client = genai.Client(
        api_key=api_key
    )

    response = client.models.generate_content(

        model="gemini-3.6-flash",

        contents=build_prompt(idea),

        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)


# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(data):

    st.write("")

    st.subheader("📊 Requirements Intelligence")

    tabs = st.tabs(
        [
            "📋 Requirements",
            "👤 User Stories",
            "⚡ Priorities",
            "🔎 Gaps",
            "🧪 Test Cases",
            "🔧 Dependencies"
        ]
    )


    # ========================================================
    # REQUIREMENTS
    # ========================================================

    with tabs[0]:

        st.markdown("### Functional Requirements")

        for index, req in enumerate(
            data.get("functional_requirements", []),
            1
        ):

            with st.container(border=True):

                st.write(
                    f"**FR-{index:02d}**"
                )

                st.write(req)


        st.markdown("### Non-Functional Requirements")

        for index, req in enumerate(
            data.get("non_functional_requirements", []),
            1
        ):

            with st.container(border=True):

                st.write(
                    f"**NFR-{index:02d}**"
                )

                st.write(req)


    # ========================================================
    # USER STORIES
    # ========================================================

    with tabs[1]:

        stories = data.get(
            "user_stories",
            []
        )

        for index, story in enumerate(
            stories,
            1
        ):

            with st.container(border=True):

                st.markdown(
                    f"### 👤 User Story {index}"
                )

                st.write(
                    story.get("story", "")
                )

                criteria = story.get(
                    "acceptance_criteria",
                    []
                )

                if criteria:

                    st.write(
                        "**Acceptance Criteria**"
                    )

                    for criterion in criteria:

                        st.write(
                            f"• {criterion}"
                        )


    # ========================================================
    # PRIORITIES
    # ========================================================

    with tabs[2]:

        priorities = data.get(
            "priorities",
            []
        )

        for item in priorities:

            with st.container(border=True):

                st.write(
                    f"**{item.get('requirement', '')}**"
                )

                st.write(
                    f"Priority: **{item.get('priority', '')}**"
                )

                st.caption(
                    item.get('reason', '')
                )


    # ========================================================
    # GAPS
    # ========================================================

    with tabs[3]:

        gaps = data.get(
            "ambiguities",
            []
        )

        if not gaps:

            st.success(
                "No major ambiguities detected."
            )

        for index, gap in enumerate(
            gaps,
            1
        ):

            with st.container(border=True):

                st.write(
                    f"🔎 **Gap {index}**"
                )

                st.write(gap)


    # ========================================================
    # TEST CASES
    # ========================================================

    with tabs[4]:

        test_cases = data.get(
            "test_cases",
            []
        )

        for test in test_cases:

            with st.container(border=True):

                st.markdown(
                    f"### 🧪 {test.get('id', '')}"
                )

                st.write(
                    f"**Scenario:** "
                    f"{test.get('scenario', '')}"
                )

                st.write(
                    f"**Expected:** "
                    f"{test.get('expected', '')}"
                )


    # ========================================================
    # DEPENDENCIES
    # ========================================================

    with tabs[5]:

        dependencies = data.get(
            "technical_dependencies",
            []
        )

        for dependency in dependencies:

            with st.container(border=True):

                st.write(
                    f"🔧 {dependency}"
                )


    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.write("")
    st.divider()

    st.download_button(

        "⬇️ Download Requirements JSON",

        data=json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),

        file_name="reqpilot_requirements.json",

        mime="application/json",

        use_container_width=True
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

if not st.session_state.logged_in:

    login_page()

    st.stop()


# ============================================================
# SIDEBAR AFTER LOGIN
# ============================================================

with st.sidebar:

    st.title("🚀 ReqPilot")

    st.caption(
        "AI Requirements Engineering Agent"
    )

    st.divider()

    st.subheader("🔑 Gemini API")

    api_key = None

    try:

        api_key = st.secrets[
            "GEMINI_API_KEY"
        ]

        st.success(
            "API key loaded"
        )

    except Exception:

        api_key = st.text_input(
            "Gemini API Key",
            type="password"
        )


    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.analysis_result = None

        st.rerun()


# ============================================================
# HERO
# ============================================================

with st.container(border=True):

    st.caption(
        "G14 • AI REQUIREMENTS ENGINEERING AGENT"
    )

    st.title(
        "ReqPilot 🚀"
    )

    st.write(
        "Transform an informal product idea into "
        "structured, development-ready software requirements."
    )

    st.write(
        "Requirements  •  User Stories  •  MoSCoW  •  "
        "Gap Detection  •  Test Cases  •  Dependencies"
    )


# ============================================================
# PRODUCT INPUT
# ============================================================

st.write("")

with st.container(border=True):

    st.subheader(
        "💡 Product Idea"
    )

    preset = st.selectbox(

        "Demo Preset",

        [
            "Custom Idea",
            "QuickCart Grocery Platform",
            "AI Fitness Platform",
            "EV Charging Platform",
            "Student Learning Platform"
        ]
    )


    preset_text = {

        "QuickCart Grocery Platform":
        """
        We want to build QuickCart, a grocery delivery platform.

        Users should be able to create accounts, browse groceries,
        search for products, add products to a cart, make online
        payments, place orders, track deliveries, and receive
        notifications.
        """,

        "AI Fitness Platform":
        """
        We want to build an AI fitness platform where users can
        create profiles, set fitness goals, follow personalized
        workout plans, track progress, and receive recommendations.
        """,

        "EV Charging Platform":
        """
        We want to build an EV charging platform where users can
        find nearby charging stations, check availability, reserve
        charging slots, make payments, and receive notifications.
        """,

        "Student Learning Platform":
        """
        We want to build a student learning platform where students
        can access courses, watch lessons, complete quizzes, track
        progress, and receive personalized recommendations.
        """
    }


    if preset == "Custom Idea":

        default_idea = ""

    else:

        default_idea = preset_text[preset]


    idea = st.text_area(

        "Describe your software product",

        value=default_idea,

        height=180,

        placeholder=
        "Example: We want to build an online grocery platform..."
    )


# ============================================================
# METRICS
# ============================================================

word_count = (
    len(idea.split())
    if idea.strip()
    else 0
)


st.write("")

m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(
        "Input Words",
        word_count
    )


with m2:

    st.metric(
        "AI Modules",
        "6"
    )


with m3:

    st.metric(
        "Artifacts",
        "6"
    )


with m4:

    st.metric(
        "Status",
        "Ready"
    )


# ============================================================
# PIPELINE
# ============================================================

st.write("")

st.subheader(
    "🔄 Intelligence Pipeline"
)


pipeline = [
    ("💡", "Idea"),
    ("🧩", "Extract"),
    ("🏷️", "Classify"),
    ("⚡", "Prioritize"),
    ("🔎", "Gaps"),
    ("🧪", "Test")
]


cols = st.columns(6)


for col, item in zip(
    cols,
    pipeline
):

    with col:

        with st.container(border=True):

            st.markdown(
                f"### {item[0]}"
            )

            st.caption(
                item[1]
            )


# ============================================================
# ACTIONS
# ============================================================

st.write("")

a1, a2 = st.columns(2)


with a1:

    analyze = st.button(
        "⚡ Analyze Requirements",
        type="primary",
        use_container_width=True
    )


with a2:

    demo = st.button(
        "🎬 Run Demo",
        use_container_width=True
    )


# ============================================================
# ANALYZE
# ============================================================

if analyze:

    if not idea.strip():

        st.warning(
            "Please enter a product idea."
        )

    elif not api_key:

        st.error(
            "Gemini API key is missing."
        )

    else:

        try:

            with st.spinner(
                "🤖 ReqPilot is analyzing your product..."
            ):

                result = analyze_with_gemini(
                    idea,
                    api_key
                )

                st.session_state.analysis_result = result


            st.success(
                "✅ Requirements generated successfully."
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
# DEMO
# ============================================================

if demo:

    st.session_state.analysis_result = demo_data

    st.success(
        "🎬 Demo requirements loaded."
    )


# ============================================================
# RESULTS
# ============================================================

if st.session_state.analysis_result:

    display_results(
        st.session_state.analysis_result
    )


# ============================================================
# CAPABILITIES
# ============================================================

st.write("")
st.divider()

st.subheader(
    "✨ ReqPilot Capabilities"
)


c1, c2, c3 = st.columns(3)


with c1:

    with st.container(border=True):

        st.markdown(
            "### 🧩 Requirement Extraction"
        )

        st.write(
            "Converts natural-language product ideas "
            "into structured software requirements."
        )


with c2:

    with st.container(border=True):

        st.markdown(
            "### 🔎 Gap Detection"
        )

        st.write(
            "Finds ambiguous, missing, or undefined "
            "requirements before development."
        )


with c3:

    with st.container(border=True):

        st.markdown(
            "### 🧪 Test Generation"
        )

        st.write(
            "Automatically creates test scenarios "
            "from generated requirements."
        )


# ============================================================
# TECHNICAL CONTRIBUTION
# ============================================================

st.write("")

with st.container(border=True):

    st.subheader(
        "🧠 Technical Contribution"
    )

    st.write(
        "ReqPilot combines AI-based requirement extraction, "
        "classification, prioritization, ambiguity detection, "
        "Agile user-story generation, and test-case generation "
        "into a single requirements engineering workflow."
    )


# ============================================================
# FOOTER
# ============================================================

st.write("")

st.caption(
    "ReqPilot • AI Requirements Engineering Agent • G14"
)
