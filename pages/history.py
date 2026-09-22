import streamlit as st
from database.db import get_projects


def show_history():

    st.title("📚 Project History")

    # Get current logged-in user
    user = st.session_state.get("user")

    if not user:
        st.warning("⚠️ Please login again.")
        return

    user_id = user["id"]

    # Get only this user's projects
    projects = get_projects(user_id)

    if not projects:
        st.info(
            "No projects found yet. "
            "Create your first project from 💡 Idea Evaluation."
        )
        return

    st.success(
        f"📊 {len(projects)} project(s) found"
    )

    for i, project in enumerate(projects, 1):

        title, domain, skill, team_size, problem, created_at = project

        with st.expander(
            f"{i}. {title}"
        ):

            st.write(
                "**Domain:**",
                domain
            )

            st.write(
                "**Skill:**",
                skill
            )

            st.write(
                "**Team Size:**",
                team_size
            )

            st.write(
                "**Problem:**",
                problem
            )

            st.write(
                "**Created:**",
                created_at
            )