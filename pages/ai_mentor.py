import streamlit as st
from utils.ai_engine import get_ai_mentor_response


def show_ai_mentor():

    st.title("🤖 AI Mentor")

    # ==================================================
    # ACTIVE PROJECT ONLY
    # ==================================================

    project = st.session_state.get("project")

    # ==================================================
    # NO ACTIVE PROJECT
    # ==================================================

    if project is None:

        st.warning("🆕 No active project.")

        st.info(
            "Please go to 💡 Idea Evaluation, "
            "create a project and click 🚀 Analyze My Idea."
        )

    else:

        st.success(
            f"🚀 Mentoring project: {project['title']}"
        )

    # ==================================================
    # CHAT HISTORY
    # ==================================================

    if "mentor_messages" not in st.session_state:

        st.session_state["mentor_messages"] = []

    # ==================================================
    # DISPLAY PREVIOUS CHAT
    # ==================================================

    for msg in st.session_state["mentor_messages"]:

        with st.chat_message(msg["role"]):

            st.markdown(
                msg["content"]
            )

    # ==================================================
    # CHAT INPUT
    # ==================================================

    user_input = st.chat_input(
        "Ask your AI Mentor anything..."
    )

    if user_input:

        # --------------------------------------------------
        # USER MESSAGE
        # --------------------------------------------------

        with st.chat_message("user"):

            st.markdown(user_input)

        st.session_state[
            "mentor_messages"
        ].append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # --------------------------------------------------
        # AI MESSAGES
        # --------------------------------------------------

        messages_for_ai = []

        # --------------------------------------------------
        # PROJECT CONTEXT
        # --------------------------------------------------

        if project:

            project_context = f"""
You are the AI Mentor inside InnovateX.

You are currently mentoring this project:

Project Title: {project['title']}
Domain: {project['domain']}
Description: {project['description']}
Problem Statement: {project['problem']}
Target Users: {project['target_users']}
Team Size: {project['team_size']}
Skill Level: {project['skill']}
Hackathon Duration: {project['duration']}
Tech Stack: {project['tech_stack']}

Use these details to give personalized,
practical and realistic advice.

Do not ask the user to repeat project details
that are already provided above.

Focus on solutions that match their team size,
skill level, hackathon duration and technology stack.
"""

            messages_for_ai.append(
                {
                    "role": "system",
                    "content": project_context
                }
            )

        else:

            messages_for_ai.append(
                {
                    "role": "system",
                    "content": """
You are the AI Mentor inside InnovateX.

There is currently no active project.

Give general hackathon and project-building
guidance until the user creates a project.

If project-specific information is required,
tell the user to create a project in
Idea Evaluation first.
"""
                }
            )

        # --------------------------------------------------
        # ADD CHAT HISTORY
        # --------------------------------------------------

        messages_for_ai.extend(
            st.session_state["mentor_messages"]
        )

        # --------------------------------------------------
        # AI RESPONSE
        # --------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "🤖 AI Mentor is thinking..."
            ):

                reply = get_ai_mentor_response(
                    messages_for_ai
                )

            st.markdown(reply)

        # --------------------------------------------------
        # SAVE AI RESPONSE
        # --------------------------------------------------

        st.session_state[
            "mentor_messages"
        ].append(
            {
                "role": "assistant",
                "content": reply
            }
        )

    # ==================================================
    # CLEAR CHAT
    # ==================================================

    if st.session_state["mentor_messages"]:

        if st.button(
            "🗑️ Clear Chat"
        ):

            st.session_state[
                "mentor_messages"
            ] = []

            st.rerun()