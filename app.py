import streamlit as st
import txt
import time
from google import genai
from google.genai import types


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ReqPilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# GLASS UI CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(90, 70, 180, 0.22), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(0, 170, 255, 0.16), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(150, 50, 200, 0.14), transparent 35%),
        #080b14;
    color: #f5f7ff;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* Glass containers */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 22px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.06);
    padding: 8px;
}


/* Headings */

h1 {
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    letter-spacing: -2px;
}

h2 {
    font-weight: 750 !important;
}

h3 {
    font-weight: 700 !important;
}


/* Normal text */

p {
    color: rgba(240, 243, 255, 0.78);
}


/* Buttons */

.stButton > button {
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.14);
    background: rgba(255,255,255,0.07);
    color: white;
    font-weight: 650;
    min-height: 45px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.13);
    border-color: rgba(255,255,255,0.25);
    transform: translateY(-1px);
}


/* Primary button */

.stButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        rgba(116, 80, 255, 0.85),
        rgba(0, 174, 255, 0.75)
    );
    border: 1px solid rgba(255,255,255,0.18);
}


/* Text area */

textarea {
    background: rgba(255,255,255,0.055) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 16px !important;
    color: white !important;
}


/* Select boxes */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.12);
}


/* Metrics */

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.09);
    padding: 14px;
    border-radius: 16px;
}


/* Tabs */

button[data-baseweb="tab"] {
    color: rgba(255,255,255,0.7);
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: white;
}


/* Sidebar */

section[data-testid="stSidebar"] {
    background: rgba(7, 9, 18, 0.82);
    border-right: 1px solid rgba(255,255,255,0.08);
}


/* Divider */

hr {
    border-color: rgba(255,255,255,0.08);
}


/* Code blocks */

code {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🚀 ReqPilot")
    st.caption("AI Requirements Engineering Agent")

    st.divider()

    st.subheader("🔑 AI Connection")

    api_key = None

    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("API Key Loaded from Secrets")
    except Exception:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Enter API key"
        )

    st.divider()

    st.subheader("🎬 Demo Preset")

    preset = st.selectbox(
        "Choose a product idea",
        [
            "Custom Idea",
            "QuickCart Grocery Platform",
            "AI Fitness Platform",
            "EV Charging Platform",
            "Student Learning Platform"
        ]
    )

    st.divider()

    st.subheader("⚙️ Pipeline")

    st.write("💡 Raw Idea")
    st.write("🧩 Requirement Extraction")
    st.write("🏷️ Classification")
    st.write("⚡ Prioritization")
    st.write("🔎 Gap Detection")
    st.write("🧪 Test Generation")

    st.divider()

    st.caption("G14 • AI Requirements Engineering Agent")


# =========================================================
# DEMO INPUTS
# =========================================================

demo_inputs = {

    "QuickCart Grocery Platform": """
We want to build QuickCart, a grocery delivery platform.

Users should be able to create accounts, browse and search for groceries,
add products to a cart, make online payments, place orders, track deliveries,
and receive order notifications.

The platform should securely handle user information and payments, support
multiple users, and provide a reliable shopping experience.
""",

    "AI Fitness Platform": """
We want to build an AI fitness platform where users can create profiles,
set fitness goals, follow personalized workout plans, track progress,
and receive recommendations based on their activity.
""",

    "EV Charging Platform": """
We want to build an EV charging platform where electric vehicle owners
can find nearby charging stations, check availability, reserve a charging
slot, make payments, and receive notifications when charging is complete.
""",

    "Student Learning Platform": """
We want to build a student learning platform where students can access
courses, watch lessons, complete quizzes, track their progress, and receive
personalized learning recommendations.
"""
}


# =========================================================
# HERO
# =========================================================

with st.container(border=True):

    st.caption("G14 • AI REQUIREMENTS ENGINEERING AGENT")

    st.title("🚀 ReqPilot")

    st.write(
        "Turn an informal product idea into structured, development-ready "
        "software requirements using AI."
    )

    st.write(
        "Requirements • User Stories • Priorities • Gaps • Test Cases • Dependencies"
    )


# =========================================================
# INPUT SECTION
# =========================================================

st.write("")

if preset == "Custom Idea":

    default_text = ""

else:

    default_text = demo_inputs[preset]


with st.container(border=True):

    st.subheader("💡 Describe Your Product")

    idea = st.text_area(
        "Product / Startup Idea",
        value=default_text,
        height=190,
        placeholder=(
            "Example: We want to build an online grocery delivery "
            "platform where users can..."
        ),
        label_visibility="collapsed"
    )


# =========================================================
# METRICS
# =========================================================

word_count = len(idea.split()) if idea.strip() else 0

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Input Words", word_count)

with m2:
    st.metric("AI Modules", "6")

with m3:
    st.metric("Artifacts", "6")

with m4:
    st.metric("AI Engine", "Gemini")


# =========================================================
# PIPELINE
# =========================================================

st.write("")
st.subheader("🔄 Requirement Intelligence Pipeline")

pipeline = [
    ("💡", "Raw Idea", "User Input"),
    ("🧩", "Extract", "Requirements"),
    ("🏷️", "Classify", "FR / NFR"),
    ("⚡", "Prioritize", "MoSCoW"),
    ("🔎", "Detect Gaps", "Ambiguities"),
    ("🧪", "Test Cases", "Validation")
]

cols = st.columns(6)

for col, item in zip(cols, pipeline):

    icon, title, subtitle = item

    with col:

        with st.container(border=True):

            st.markdown(f"### {icon}")

            st.write(f"**{title}**")

            st.caption(subtitle)


# =========================================================
# DEMO DATA
# =========================================================

demo_data = {

    "functional_requirements": [

        "Users should be able to create an account and securely log in.",

        "Users should be able to browse groceries by category and search for products.",

        "Users should be able to add products to a shopping cart and update quantities.",

        "Users should be able to place orders and make online payments.",

        "Users should be able to view their order status and track delivery.",

        "The system should send notifications for order confirmation and delivery updates."
    ],

    "non_functional_requirements": [

        "User payment and personal information must be securely protected.",

        "The application should provide fast response times during normal usage.",

        "The system should remain available during high-demand periods.",

        "The application should support multiple users placing orders simultaneously."
    ],

    "user_stories": [

        {
            "story":
                "As a customer, I want to search for groceries so that I can quickly find the products I need.",

            "acceptance_criteria": [

                "Given the user is on the product page, when they enter a product name, then matching products should be displayed.",

                "Given no matching product exists, when the user searches, then a suitable message should be displayed."
            ]
        },

        {
            "story":
                "As a customer, I want to place an online order so that I can receive groceries at my preferred address.",

            "acceptance_criteria": [

                "Given the cart contains products, when the user confirms the order and payment succeeds, then the order should be created.",

                "Given payment fails, when the user attempts to place the order, then the order should not be confirmed."
            ]
        },

        {
            "story":
                "As a customer, I want to track my order so that I know its current delivery status.",

            "acceptance_criteria": [

                "Given an order has been placed, when the user opens order tracking, then the current order status should be displayed.",

                "The user should receive updates when the delivery status changes."
            ]
        }
    ],

    "priorities": [

        {
            "requirement": "User registration and login",
            "priority": "Must Have",
            "reason":
                "Users need secure accounts to manage orders and personal information."
        },

        {
            "requirement": "Product search and browsing",
            "priority": "Must Have",
            "reason":
                "Customers need to find products before placing an order."
        },

        {
            "requirement": "Shopping cart",
            "priority": "Must Have",
            "reason":
                "Customers need to select and manage products before checkout."
        },

        {
            "requirement": "Online payment",
            "priority": "Must Have",
            "reason":
                "Payment is required to complete an online order."
        },

        {
            "requirement": "Order tracking",
            "priority": "Should Have",
            "reason":
                "Tracking improves delivery visibility and customer experience."
        },

        {
            "requirement": "Personalized product recommendations",
            "priority": "Could Have",
            "reason":
                "Recommendations can improve product discovery but are not required for the core ordering flow."
        }
    ],

    "ambiguities": [

        "Which payment methods should be supported?",

        "What delivery areas and geographical locations should be supported?",

        "What happens when a product becomes unavailable after the user adds it to the cart?",

        "Should users be able to cancel an order after payment?",

        "What is the expected delivery time?",

        "Should notifications be sent through SMS, email, push notifications, or all three?"
    ],

    "test_cases": [

        {
            "id": "TC-01",
            "scenario": "User searches for an available grocery product.",
            "expected":
                "Matching products should be displayed with product name, price, and availability."
        },

        {
            "id": "TC-02",
            "scenario":
                "User adds products to the cart and changes the quantity.",
            "expected":
                "Cart quantity and total price should update correctly."
        },

        {
            "id": "TC-03",
            "scenario":
                "User completes checkout with a successful payment.",
            "expected":
                "The order should be created and an order confirmation should be displayed."
        },

        {
            "id": "TC-04",
            "scenario":
                "Payment fails during checkout.",
            "expected":
                "The order should not be confirmed and the user should receive an appropriate error message."
        },

        {
            "id": "TC-05",
            "scenario":
                "User opens tracking for an existing order.",
            "expected":
                "The current delivery status should be displayed."
        }
    ],

    "technical_dependencies": [

        "User authentication and authorization",

        "Product and inventory database",

        "Shopping cart and order management backend",

        "Payment gateway API",

        "Delivery and order tracking service",

        "Notification service",

        "Web or mobile frontend"
    ]
}


# =========================================================
# GEMINI PROMPT
# =========================================================

def create_prompt(idea):

    return f"""
You are an AI Requirements Engineering Agent.

Analyze the following software product idea:

{idea}

Return ONLY valid JSON using exactly this structure:

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

Rules:

1. Extract clear functional requirements.
2. Extract realistic non-functional requirements.
3. Generate Agile-style user stories.
4. Include Given/When/Then style acceptance criteria where useful.
5. Prioritize requirements using MoSCoW:
   Must Have, Should Have, Could Have, Won't Have.
6. Identify missing or ambiguous requirements.
7. Generate practical test cases.
8. Identify realistic technical dependencies.
9. Do not invent unnecessary features.
10. Keep the output concise and suitable for a software development team.
"""


# =========================================================
# GEMINI ANALYSIS
# =========================================================

def analyze_with_gemini(idea, key):

    client = genai.Client(api_key=key)

    prompt = create_prompt(idea)

    last_error = None

    for attempt in range(3):

        try:

            response = client.models.generate_content(

                model="gemini-3.6-flash",

                contents=prompt,

                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            return json.loads(response.text)

        except Exception as e:

            last_error = e

            error_text = str(e)

            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue

            raise last_error

    raise last_error


# =========================================================
# DISPLAY RESULTS
# =========================================================

def display_results(data):

    st.write("")

    st.subheader("📊 Generated Requirements")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "📋 Requirements",
            "👤 User Stories",
            "⚡ Priorities",
            "🔎 Gaps",
            "🧪 Test Cases",
            "🔧 Technical"
        ]
    )


    # -----------------------------------------------------
    # REQUIREMENTS
    # -----------------------------------------------------

    with tab1:

        st.markdown("### Functional Requirements")

        for i, req in enumerate(
            data.get("functional_requirements", []),
            1
        ):

            with st.container(border=True):

                st.write(f"**FR-{i:02d}**")

                st.write(req)


        st.markdown("### Non-Functional Requirements")

        for i, req in enumerate(
            data.get("non_functional_requirements", []),
            1
        ):

            with st.container(border=True):

                st.write(f"**NFR-{i:02d}**")

                st.write(req)


    # -----------------------------------------------------
    # USER STORIES
    # -----------------------------------------------------

    with tab2:

        stories = data.get("user_stories", [])

        if not stories:

            st.info("No user stories generated.")

        for i, story in enumerate(stories, 1):

            with st.container(border=True):

                st.markdown(f"### 👤 User Story {i}")

                st.write(story.get("story", ""))

                criteria = story.get("acceptance_criteria", [])

                if criteria:

                    st.write("**Acceptance Criteria**")

                    for criterion in criteria:

                        st.write(f"• {criterion}")


    # -----------------------------------------------------
    # PRIORITIES
    # -----------------------------------------------------

    with tab3:

        priorities = data.get("priorities", [])

        for item in priorities:

            with st.container(border=True):

                st.write(
                    f"**{item.get('requirement', 'Requirement')}**"
                )

                st.write(
                    f"Priority: **{item.get('priority', 'N/A')}**"
                )

                st.caption(
                    item.get('reason', '')
                )


    # -----------------------------------------------------
    # GAPS
    # -----------------------------------------------------

    with tab4:

        ambiguities = data.get("ambiguities", [])

        if not ambiguities:

            st.success("No major ambiguities detected.")

        else:

            for i, item in enumerate(ambiguities, 1):

                with st.container(border=True):

                    st.write(f"🔎 **Gap {i}**")

                    st.write(item)


    # -----------------------------------------------------
    # TEST CASES
    # -----------------------------------------------------

    with tab5:

        test_cases = data.get("test_cases", [])

        for test in test_cases:

            with st.container(border=True):

                st.write(
                    f"### 🧪 {test.get('id', 'Test Case')}"
                )

                st.write(
                    f"**Scenario:** {test.get('scenario', '')}"
                )

                st.write(
                    f"**Expected:** {test.get('expected', '')}"
                )


    # -----------------------------------------------------
    # TECHNICAL
    # -----------------------------------------------------

    with tab6:

        dependencies = data.get(
            "technical_dependencies",
            []
        )

        st.markdown("### 🔧 Technical Dependencies")

        for dependency in dependencies:

            st.write(f"• {dependency}")


    # -----------------------------------------------------
    # DOWNLOAD JSON
    # -----------------------------------------------------

    st.divider()

    st.download_button(

        label="⬇️ Download Requirements JSON",

        data=json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),

        file_name="reqpilot_requirements.json",

        mime="application/json"
    )


# =========================================================
# ACTION BUTTONS
# =========================================================

st.write("")

col1, col2 = st.columns(2)


with col1:

    analyze_button = st.button(
        "⚡ Analyze Requirements",
        type="primary",
        use_container_width=True
    )


with col2:

    demo_button = st.button(
        "🎬 Demo Mode",
        use_container_width=True
    )


# =========================================================
# LIVE AI ANALYSIS
# =========================================================

if analyze_button:

    if not idea.strip():

        st.warning(
            "Please enter a product or startup idea first."
        )

    elif not api_key:

        st.error(
            "Gemini API key not found. Add GEMINI_API_KEY in Streamlit Secrets."
        )

    else:

        with st.spinner(
            "🤖 ReqPilot is analyzing your requirements..."
        ):

            try:

                result = analyze_with_gemini(
                    idea,
                    api_key
                )

                st.success(
                    "✅ Requirements successfully generated!"
                )

                display_results(result)

            except Exception as e:

                error_text = str(e)

                if "503" in error_text or "UNAVAILABLE" in error_text:

                    st.error(
                        "Gemini is temporarily unavailable. "
                        "Please try again or use Demo Mode."
                    )

                elif (
                    "429" in error_text
                    or "quota" in error_text.lower()
                ):

                    st.error(
                        "Gemini API quota/rate limit reached. "
                        "Please try again later or use Demo Mode."
                    )

                else:

                    st.error(
                        f"Execution Error: {error_text}"
                    )


# =========================================================
# DEMO MODE
# =========================================================

if demo_button:

    st.success(
        "🎬 Demo Mode activated — showing QuickCart example."
    )

    display_results(demo_data)


# =========================================================
# FEATURES
# =========================================================

st.write("")
st.divider()

st.subheader("✨ Core Capabilities")

c1, c2, c3 = st.columns(3)


with c1:

    with st.container(border=True):

        st.markdown("### 🧩 Requirement Extraction")

        st.write(
            "Converts an informal product idea into structured "
            "functional and non-functional requirements."
        )


with c2:

    with st.container(border=True):

        st.markdown("### 🔎 Ambiguity Detection")

        st.write(
            "Identifies missing decisions and unclear requirements "
            "before development begins."
        )


with c3:

    with st.container(border=True):

        st.markdown("### 🧪 Test Generation")

        st.write(
            "Creates practical test scenarios from the generated "
            "requirements."
        )


# =========================================================
# TECHNICAL CONTRIBUTION
# =========================================================

st.write("")

with st.container(border=True):

    st.subheader("🧠 Technical Contribution")

    st.write(
        "Our solution is not just a generic API wrapper. "
        "ReqPilot uses a structured multi-stage requirements analysis "
        "pipeline covering requirement classification, ambiguity detection, "
        "prioritization, user-story generation and test-case generation "
        "from a single project description."
    )


# =========================================================
# FOOTER
# =========================================================

st.write("")

st.caption(
    "ReqPilot • AI Requirements Engineering Agent • G14"
)
import streamlit as st
import json
import time
from google import genai
from google.genai import types


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ReqPilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# GLASS UI CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(90, 70, 180, 0.22), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(0, 170, 255, 0.16), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(150, 50, 200, 0.14), transparent 35%),
        #080b14;
    color: #f5f7ff;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* Glass containers */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 22px;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.06);
    padding: 8px;
}


/* Headings */

h1 {
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    letter-spacing: -2px;
}

h2 {
    font-weight: 750 !important;
}

h3 {
    font-weight: 700 !important;
}


/* Normal text */

p {
    color: rgba(240, 243, 255, 0.78);
}


/* Buttons */

.stButton > button {
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.14);
    background: rgba(255,255,255,0.07);
    color: white;
    font-weight: 650;
    min-height: 45px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.13);
    border-color: rgba(255,255,255,0.25);
    transform: translateY(-1px);
}


/* Primary button */

.stButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        rgba(116, 80, 255, 0.85),
        rgba(0, 174, 255, 0.75)
    );
    border: 1px solid rgba(255,255,255,0.18);
}


/* Text area */

textarea {
    background: rgba(255,255,255,0.055) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 16px !important;
    color: white !important;
}


/* Select boxes */

div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.06);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.12);
}


/* Metrics */

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.09);
    padding: 14px;
    border-radius: 16px;
}


/* Tabs */

button[data-baseweb="tab"] {
    color: rgba(255,255,255,0.7);
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: white;
}


/* Sidebar */

section[data-testid="stSidebar"] {
    background: rgba(7, 9, 18, 0.82);
    border-right: 1px solid rgba(255,255,255,0.08);
}


/* Divider */

hr {
    border-color: rgba(255,255,255,0.08);
}


/* Code blocks */

code {
    border-radius: 8px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🚀 ReqPilot")
    st.caption("AI Requirements Engineering Agent")

    st.divider()

    st.subheader("🔑 AI Connection")

    api_key = None

    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("API Key Loaded from Secrets")
    except Exception:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="Enter API key"
        )

    st.divider()

    st.subheader("🎬 Demo Preset")

    preset = st.selectbox(
        "Choose a product idea",
        [
            "Custom Idea",
            "QuickCart Grocery Platform",
            "AI Fitness Platform",
            "EV Charging Platform",
            "Student Learning Platform"
        ]
    )

    st.divider()

    st.subheader("⚙️ Pipeline")

    st.write("💡 Raw Idea")
    st.write("🧩 Requirement Extraction")
    st.write("🏷️ Classification")
    st.write("⚡ Prioritization")
    st.write("🔎 Gap Detection")
    st.write("🧪 Test Generation")

    st.divider()

    st.caption("G14 • AI Requirements Engineering Agent")


# =========================================================
# DEMO INPUTS
# =========================================================

demo_inputs = {

    "QuickCart Grocery Platform": """
We want to build QuickCart, a grocery delivery platform.

Users should be able to create accounts, browse and search for groceries,
add products to a cart, make online payments, place orders, track deliveries,
and receive order notifications.

The platform should securely handle user information and payments, support
multiple users, and provide a reliable shopping experience.
""",

    "AI Fitness Platform": """
We want to build an AI fitness platform where users can create profiles,
set fitness goals, follow personalized workout plans, track progress,
and receive recommendations based on their activity.
""",

    "EV Charging Platform": """
We want to build an EV charging platform where electric vehicle owners
can find nearby charging stations, check availability, reserve a charging
slot, make payments, and receive notifications when charging is complete.
""",

    "Student Learning Platform": """
We want to build a student learning platform where students can access
courses, watch lessons, complete quizzes, track their progress, and receive
personalized learning recommendations.
"""
}


# =========================================================
# HERO
# =========================================================

with st.container(border=True):

    st.caption("G14 • AI REQUIREMENTS ENGINEERING AGENT")

    st.title("🚀 ReqPilot")

    st.write(
        "Turn an informal product idea into structured, development-ready "
        "software requirements using AI."
    )

    st.write(
        "Requirements • User Stories • Priorities • Gaps • Test Cases • Dependencies"
    )


# =========================================================
# INPUT SECTION
# =========================================================

st.write("")

if preset == "Custom Idea":

    default_text = ""

else:

    default_text = demo_inputs[preset]


with st.container(border=True):

    st.subheader("💡 Describe Your Product")

    idea = st.text_area(
        "Product / Startup Idea",
        value=default_text,
        height=190,
        placeholder=(
            "Example: We want to build an online grocery delivery "
            "platform where users can..."
        ),
        label_visibility="collapsed"
    )


# =========================================================
# METRICS
# =========================================================

word_count = len(idea.split()) if idea.strip() else 0

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Input Words", word_count)

with m2:
    st.metric("AI Modules", "6")

with m3:
    st.metric("Artifacts", "6")

with m4:
    st.metric("AI Engine", "Gemini")


# =========================================================
# PIPELINE
# =========================================================

st.write("")
st.subheader("🔄 Requirement Intelligence Pipeline")

pipeline = [
    ("💡", "Raw Idea", "User Input"),
    ("🧩", "Extract", "Requirements"),
    ("🏷️", "Classify", "FR / NFR"),
    ("⚡", "Prioritize", "MoSCoW"),
    ("🔎", "Detect Gaps", "Ambiguities"),
    ("🧪", "Test Cases", "Validation")
]

cols = st.columns(6)

for col, item in zip(cols, pipeline):

    icon, title, subtitle = item

    with col:

        with st.container(border=True):

            st.markdown(f"### {icon}")

            st.write(f"**{title}**")

            st.caption(subtitle)


# =========================================================
# DEMO DATA
# =========================================================

demo_data = {

    "functional_requirements": [

        "Users should be able to create an account and securely log in.",

        "Users should be able to browse groceries by category and search for products.",

        "Users should be able to add products to a shopping cart and update quantities.",

        "Users should be able to place orders and make online payments.",

        "Users should be able to view their order status and track delivery.",

        "The system should send notifications for order confirmation and delivery updates."
    ],

    "non_functional_requirements": [

        "User payment and personal information must be securely protected.",

        "The application should provide fast response times during normal usage.",

        "The system should remain available during high-demand periods.",

        "The application should support multiple users placing orders simultaneously."
    ],

    "user_stories": [

        {
            "story":
                "As a customer, I want to search for groceries so that I can quickly find the products I need.",

            "acceptance_criteria": [

                "Given the user is on the product page, when they enter a product name, then matching products should be displayed.",

                "Given no matching product exists, when the user searches, then a suitable message should be displayed."
            ]
        },

        {
            "story":
                "As a customer, I want to place an online order so that I can receive groceries at my preferred address.",

            "acceptance_criteria": [

                "Given the cart contains products, when the user confirms the order and payment succeeds, then the order should be created.",

                "Given payment fails, when the user attempts to place the order, then the order should not be confirmed."
            ]
        },

        {
            "story":
                "As a customer, I want to track my order so that I know its current delivery status.",

            "acceptance_criteria": [

                "Given an order has been placed, when the user opens order tracking, then the current order status should be displayed.",

                "The user should receive updates when the delivery status changes."
            ]
        }
    ],

    "priorities": [

        {
            "requirement": "User registration and login",
            "priority": "Must Have",
            "reason":
                "Users need secure accounts to manage orders and personal information."
        },

        {
            "requirement": "Product search and browsing",
            "priority": "Must Have",
            "reason":
                "Customers need to find products before placing an order."
        },

        {
            "requirement": "Shopping cart",
            "priority": "Must Have",
            "reason":
                "Customers need to select and manage products before checkout."
        },

        {
            "requirement": "Online payment",
            "priority": "Must Have",
            "reason":
                "Payment is required to complete an online order."
        },

        {
            "requirement": "Order tracking",
            "priority": "Should Have",
            "reason":
                "Tracking improves delivery visibility and customer experience."
        },

        {
            "requirement": "Personalized product recommendations",
            "priority": "Could Have",
            "reason":
                "Recommendations can improve product discovery but are not required for the core ordering flow."
        }
    ],

    "ambiguities": [

        "Which payment methods should be supported?",

        "What delivery areas and geographical locations should be supported?",

        "What happens when a product becomes unavailable after the user adds it to the cart?",

        "Should users be able to cancel an order after payment?",

        "What is the expected delivery time?",

        "Should notifications be sent through SMS, email, push notifications, or all three?"
    ],

    "test_cases": [

        {
            "id": "TC-01",
            "scenario": "User searches for an available grocery product.",
            "expected":
                "Matching products should be displayed with product name, price, and availability."
        },

        {
            "id": "TC-02",
            "scenario":
                "User adds products to the cart and changes the quantity.",
            "expected":
                "Cart quantity and total price should update correctly."
        },

        {
            "id": "TC-03",
            "scenario":
                "User completes checkout with a successful payment.",
            "expected":
                "The order should be created and an order confirmation should be displayed."
        },

        {
            "id": "TC-04",
            "scenario":
                "Payment fails during checkout.",
            "expected":
                "The order should not be confirmed and the user should receive an appropriate error message."
        },

        {
            "id": "TC-05",
            "scenario":
                "User opens tracking for an existing order.",
            "expected":
                "The current delivery status should be displayed."
        }
    ],

    "technical_dependencies": [

        "User authentication and authorization",

        "Product and inventory database",

        "Shopping cart and order management backend",

        "Payment gateway API",

        "Delivery and order tracking service",

        "Notification service",

        "Web or mobile frontend"
    ]
}


# =========================================================
# GEMINI PROMPT
# =========================================================

def create_prompt(idea):

    return f"""
You are an AI Requirements Engineering Agent.

Analyze the following software product idea:

{idea}

Return ONLY valid JSON using exactly this structure:

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

Rules:

1. Extract clear functional requirements.
2. Extract realistic non-functional requirements.
3. Generate Agile-style user stories.
4. Include Given/When/Then style acceptance criteria where useful.
5. Prioritize requirements using MoSCoW:
   Must Have, Should Have, Could Have, Won't Have.
6. Identify missing or ambiguous requirements.
7. Generate practical test cases.
8. Identify realistic technical dependencies.
9. Do not invent unnecessary features.
10. Keep the output concise and suitable for a software development team.
"""


# =========================================================
# GEMINI ANALYSIS
# =========================================================

def analyze_with_gemini(idea, key):

    client = genai.Client(api_key=key)

    prompt = create_prompt(idea)

    last_error = None

    for attempt in range(3):

        try:

            response = client.models.generate_content(

                model="gemini-3.6-flash",

                contents=prompt,

                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            return json.loads(response.text)

        except Exception as e:

            last_error = e

            error_text = str(e)

            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < 2:
                    time.sleep(2 ** attempt)
                    continue

            raise last_error

    raise last_error


# =========================================================
# DISPLAY RESULTS
# =========================================================

def display_results(data):

    st.write("")

    st.subheader("📊 Generated Requirements")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "📋 Requirements",
            "👤 User Stories",
            "⚡ Priorities",
            "🔎 Gaps",
            "🧪 Test Cases",
            "🔧 Technical"
        ]
    )


    # -----------------------------------------------------
    # REQUIREMENTS
    # -----------------------------------------------------

    with tab1:

        st.markdown("### Functional Requirements")

        for i, req in enumerate(
            data.get("functional_requirements", []),
            1
        ):

            with st.container(border=True):

                st.write(f"**FR-{i:02d}**")

                st.write(req)


        st.markdown("### Non-Functional Requirements")

        for i, req in enumerate(
            data.get("non_functional_requirements", []),
            1
        ):

            with st.container(border=True):

                st.write(f"**NFR-{i:02d}**")

                st.write(req)


    # -----------------------------------------------------
    # USER STORIES
    # -----------------------------------------------------

    with tab2:

        stories = data.get("user_stories", [])

        if not stories:

            st.info("No user stories generated.")

        for i, story in enumerate(stories, 1):

            with st.container(border=True):

                st.markdown(f"### 👤 User Story {i}")

                st.write(story.get("story", ""))

                criteria = story.get("acceptance_criteria", [])

                if criteria:

                    st.write("**Acceptance Criteria**")

                    for criterion in criteria:

                        st.write(f"• {criterion}")


    # -----------------------------------------------------
    # PRIORITIES
    # -----------------------------------------------------

    with tab3:

        priorities = data.get("priorities", [])

        for item in priorities:

            with st.container(border=True):

                st.write(
                    f"**{item.get('requirement', 'Requirement')}**"
                )

                st.write(
                    f"Priority: **{item.get('priority', 'N/A')}**"
                )

                st.caption(
                    item.get('reason', '')
                )


    # -----------------------------------------------------
    # GAPS
    # -----------------------------------------------------

    with tab4:

        ambiguities = data.get("ambiguities", [])

        if not ambiguities:

            st.success("No major ambiguities detected.")

        else:

            for i, item in enumerate(ambiguities, 1):

                with st.container(border=True):

                    st.write(f"🔎 **Gap {i}**")

                    st.write(item)


    # -----------------------------------------------------
    # TEST CASES
    # -----------------------------------------------------

    with tab5:

        test_cases = data.get("test_cases", [])

        for test in test_cases:

            with st.container(border=True):

                st.write(
                    f"### 🧪 {test.get('id', 'Test Case')}"
                )

                st.write(
                    f"**Scenario:** {test.get('scenario', '')}"
                )

                st.write(
                    f"**Expected:** {test.get('expected', '')}"
                )


    # -----------------------------------------------------
    # TECHNICAL
    # -----------------------------------------------------

    with tab6:

        dependencies = data.get(
            "technical_dependencies",
            []
        )

        st.markdown("### 🔧 Technical Dependencies")

        for dependency in dependencies:

            st.write(f"• {dependency}")


    # -----------------------------------------------------
    # DOWNLOAD JSON
    # -----------------------------------------------------

    st.divider()

    st.download_button(

        label="⬇️ Download Requirements JSON",

        data=json.dumps(
            data,
            indent=2,
            ensure_ascii=False
        ),

        file_name="reqpilot_requirements.json",

        mime="application/json"
    )


# =========================================================
# ACTION BUTTONS
# =========================================================

st.write("")

col1, col2 = st.columns(2)


with col1:

    analyze_button = st.button(
        "⚡ Analyze Requirements",
        type="primary",
        use_container_width=True
    )


with col2:

    demo_button = st.button(
        "🎬 Demo Mode",
        use_container_width=True
    )


# =========================================================
# LIVE AI ANALYSIS
# =========================================================

if analyze_button:

    if not idea.strip():

        st.warning(
            "Please enter a product or startup idea first."
        )

    elif not api_key:

        st.error(
            "Gemini API key not found. Add GEMINI_API_KEY in Streamlit Secrets."
        )

    else:

        with st.spinner(
            "🤖 ReqPilot is analyzing your requirements..."
        ):

            try:

                result = analyze_with_gemini(
                    idea,
                    api_key
                )

                st.success(
                    "✅ Requirements successfully generated!"
                )

                display_results(result)

            except Exception as e:

                error_text = str(e)

                if "503" in error_text or "UNAVAILABLE" in error_text:

                    st.error(
                        "Gemini is temporarily unavailable. "
                        "Please try again or use Demo Mode."
                    )

                elif (
                    "429" in error_text
                    or "quota" in error_text.lower()
                ):

                    st.error(
                        "Gemini API quota/rate limit reached. "
                        "Please try again later or use Demo Mode."
                    )

                else:

                    st.error(
                        f"Execution Error: {error_text}"
                    )


# =========================================================
# DEMO MODE
# =========================================================

if demo_button:

    st.success(
        "🎬 Demo Mode activated — showing QuickCart example."
    )

    display_results(demo_data)


# =========================================================
# FEATURES
# =========================================================

st.write("")
st.divider()

st.subheader("✨ Core Capabilities")

c1, c2, c3 = st.columns(3)


with c1:

    with st.container(border=True):

        st.markdown("### 🧩 Requirement Extraction")

        st.write(
            "Converts an informal product idea into structured "
            "functional and non-functional requirements."
        )


with c2:

    with st.container(border=True):

        st.markdown("### 🔎 Ambiguity Detection")

        st.write(
            "Identifies missing decisions and unclear requirements "
            "before development begins."
        )


with c3:

    with st.container(border=True):

        st.markdown("### 🧪 Test Generation")

        st.write(
            "Creates practical test scenarios from the generated "
            "requirements."
        )


# =========================================================
# TECHNICAL CONTRIBUTION
# =========================================================

st.write("")

with st.container(border=True):

    st.subheader("🧠 Technical Contribution")

    st.write(
        "Our solution is not just a generic API wrapper. "
        "ReqPilot uses a structured multi-stage requirements analysis "
        "pipeline covering requirement classification, ambiguity detection, "
        "prioritization, user-story generation and test-case generation "
        "from a single project description."
    )


# =========================================================
# FOOTER
# =========================================================

st.write("")

st.caption(
    "ReqPilot • AI Requirements Engineering Agent • G14"
)import os
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
