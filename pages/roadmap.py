import streamlit as st
from utils.ai_engine import get_ai_roadmap


def show_roadmap():

    st.title("🛣️ AI Roadmap Generator")

    # --------------------------------------------------
    # Get Active Project
    # --------------------------------------------------

    project = st.session_state.get("project")

    # --------------------------------------------------
    # New Project Mode
    # --------------------------------------------------

    if project is None and st.session_state.get(
        "new_project_mode",
        False
    ):

        st.warning("🆕 No active project yet.")

        st.info(
            "Please complete your new project details in "
            "💡 Idea Evaluation and click 🚀 Analyze My Idea."
        )

        return

    # --------------------------------------------------
    # No Project
    # --------------------------------------------------

    if project is None:

        st.warning(
            "⚠️ Please evaluate a project first."
        )

        st.info(
            "Go to 💡 Idea Evaluation and create a project."
        )

        return

    # --------------------------------------------------
    # Active Project
    # --------------------------------------------------

    st.success(
        f"🚀 Active Project: {project['title']}"
    )

    st.subheader(
        f"🛣️ Roadmap for {project['title']}"
    )

    # --------------------------------------------------
    # Project Information
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Domain:**",
            project["domain"]
        )

        st.write(
            "**Team Size:**",
            project["team_size"]
        )

        st.write(
            "**Skill Level:**",
            project["skill"]
        )

    with col2:

        st.write(
            "**Duration:**",
            project["duration"]
        )

        if project["tech_stack"]:

            st.write(
                "**Tech Stack:**",
                ", ".join(project["tech_stack"])
            )

        else:

            st.write(
                "**Tech Stack:**",
                "Not specified"
            )

    # --------------------------------------------------
    # Generate Roadmap
    # --------------------------------------------------

    st.divider()

    if st.button("🤖 Generate AI Roadmap"):

        with st.spinner(
            "🤖 Generating roadmap..."
        ):

            roadmap = get_ai_roadmap(project)

        st.success(
            "✅ Your AI Roadmap is Ready!"
        )

        st.markdown(roadmap)