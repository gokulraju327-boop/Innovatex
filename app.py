import streamlit as st

from pages.login import show_login
from pages.profile import show_profile

from components.sidebar import show_sidebar
from components.dashboard import show_dashboard

from pages.idea_evaluation import show_idea_evaluation
from pages.analysis import show_analysis
from pages.ai_mentor import show_ai_mentor
from pages.pdf_report import show_pdf_report
from pages.roadmap import show_roadmap
from pages.history import show_history


st.set_page_config(
    page_title="InnovateX",
    page_icon="🚀",
    layout="wide"
)


# 🔐 Login protection
if not st.session_state.get("logged_in", False):
    show_login()
    st.stop()


# Sidebar
selected = show_sidebar()


# Dashboard quick actions
dashboard_action = st.session_state.pop(
    "dashboard_action",
    None
)

if dashboard_action:
    selected = dashboard_action


# Page routing
if selected == "Dashboard":
    show_dashboard()

elif selected == "Idea Evaluation":
    show_idea_evaluation()

elif selected == "Analysis":
    show_analysis()

elif selected == "AI Mentor":
    show_ai_mentor()

elif selected == "Roadmap":
    show_roadmap()

elif selected == "PDF Report":
    show_pdf_report()

elif selected == "History":
    show_history()

elif selected == "Profile":
    show_profile()

elif selected == "About":
    st.title("ℹ️ About")

    st.markdown(
        """
        ## 🚀 InnovateX

        **AI Innovation & Hackathon Mentor**

        InnovateX helps students and innovators
        transform their ideas into practical,
        hackathon-ready projects.

        ### Platform Features

        💡 AI Idea Evaluation  
        📊 Project Analysis  
        🤖 AI Mentor  
        🛣️ AI Roadmap Generator  
        📄 Professional PDF Reports  
        📚 Project History  
        👤 User Profile
        """
    )