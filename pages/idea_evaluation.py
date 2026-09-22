import streamlit as st
from database.db import save_project


def show_idea_evaluation():

    st.title("💡 AI Idea Evaluation")
    st.write("Fill in the details below to evaluate your hackathon idea.")

    if "form_version" not in st.session_state:
        st.session_state["form_version"] = 0

    url_new_project = st.query_params.get("mode") == "new"

    if url_new_project:
        st.session_state["new_project_mode"] = True

    if st.button("🆕 Start New Project"):
        st.session_state.pop("project", None)
        st.session_state.pop("latest_score", None)

        st.session_state["new_project_mode"] = True
        st.query_params["mode"] = "new"

        st.session_state["form_version"] += 1
        st.session_state["idea_loaded"] = True

        st.rerun()

    if "idea_loaded" not in st.session_state:
        st.session_state["idea_title"] = ""
        st.session_state["idea_domain"] = "Smart City"
        st.session_state["idea_description"] = ""
        st.session_state["idea_team_size"] = 4
        st.session_state["idea_duration"] = "24 Hours"
        st.session_state["idea_skill"] = "Beginner"
        st.session_state["idea_tech_stack"] = []
        st.session_state["idea_target_users"] = ""
        st.session_state["idea_problem"] = ""

        st.session_state["new_project_mode"] = True
        st.session_state["idea_loaded"] = True

    if st.session_state.get("new_project_mode", True):

        default_title = ""
        default_domain = "Smart City"
        default_description = ""
        default_team_size = 4
        default_duration = "24 Hours"
        default_skill = "Beginner"
        default_tech_stack = []
        default_target_users = ""
        default_problem = ""

    else:

        default_title = st.session_state.get(
            "idea_title",
            ""
        )

        default_domain = st.session_state.get(
            "idea_domain",
            "Smart City"
        )

        default_description = st.session_state.get(
            "idea_description",
            ""
        )

        default_team_size = st.session_state.get(
            "idea_team_size",
            4
        )

        default_duration = st.session_state.get(
            "idea_duration",
            "24 Hours"
        )

        default_skill = st.session_state.get(
            "idea_skill",
            "Beginner"
        )

        default_tech_stack = st.session_state.get(
            "idea_tech_stack",
            []
        )

        default_target_users = st.session_state.get(
            "idea_target_users",
            ""
        )

        default_problem = st.session_state.get(
            "idea_problem",
            ""
        )

    version = st.session_state["form_version"]

    st.subheader("📌 Project Details")

    project_title = st.text_input(
        "Project Title",
        value=default_title,
        key=f"idea_title_{version}",
        placeholder="Example: AI Smart Garbage Collection System"
    )

    domains = [
        "Smart City",
        "Healthcare",
        "Education",
        "Agriculture",
        "Environment",
        "AI / ML",
        "Cyber Security",
        "FinTech",
        "IoT",
        "Others"
    ]

    domain = st.selectbox(
        "Project Domain",
        domains,
        index=(
            domains.index(default_domain)
            if default_domain in domains
            else 0
        ),
        key=f"idea_domain_{version}"
    )

    description = st.text_area(
        "Project Description",
        value=default_description,
        height=150,
        key=f"idea_description_{version}"
    )

    st.subheader("👥 Team Details")

    col1, col2 = st.columns(2)

    with col1:

        team_size = st.slider(
            "Number of Team Members",
            1,
            6,
            value=default_team_size,
            key=f"idea_team_size_{version}"
        )

    with col2:

        durations = [
            "24 Hours",
            "36 Hours",
            "48 Hours",
            "More than 48 Hours"
        ]

        duration = st.selectbox(
            "Hackathon Duration",
            durations,
            index=(
                durations.index(default_duration)
                if default_duration in durations
                else 0
            ),
            key=f"idea_duration_{version}"
        )

    skills = [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]

    skill = st.selectbox(
        "Skill Level",
        skills,
        index=(
            skills.index(default_skill)
            if default_skill in skills
            else 0
        ),
        key=f"idea_skill_{version}"
    )

    st.subheader("💻 Technical Details")

    tech_options = [
        "Python",
        "Streamlit",
        "SQL",
        "FastAPI",
        "React",
        "Flutter",
        "Node.js",
        "AI/ML",
        "IoT",
        "MongoDB",
        "Firebase"
    ]

    tech_stack = st.multiselect(
        "Tech Stack",
        tech_options,
        default=[
            item
            for item in default_tech_stack
            if item in tech_options
        ],
        key=f"idea_tech_stack_{version}"
    )

    target_users = st.text_input(
        "Target Users",
        value=default_target_users,
        key=f"idea_target_users_{version}",
        placeholder="Students, Farmers, Hospitals..."
    )

    problem = st.text_area(
        "Problem Statement",
        value=default_problem,
        height=120,
        key=f"idea_problem_{version}"
    )

    if st.button("🚀 Analyze My Idea"):

        if (
            not project_title.strip()
            or not description.strip()
            or not problem.strip()
        ):
            st.error(
                "Please fill all the required fields."
            )
            return

        project_data = {
            "title": project_title.strip(),
            "domain": domain,
            "description": description.strip(),
            "team_size": team_size,
            "duration": duration,
            "skill": skill,
            "tech_stack": tech_stack,
            "target_users": target_users.strip(),
            "problem": problem.strip()
        }

        # Current logged-in user
        user = st.session_state.get("user")

        if not user:
            st.error(
                "⚠️ Please login again before creating a project."
            )
            return

        user_id = user["id"]

        # Save project for this user
        save_project(
            project_data,
            user_id
        )

        # Keep active project in current session
        st.session_state["project"] = project_data
        st.session_state["new_project_mode"] = False

        if "history" not in st.session_state:
            st.session_state["history"] = []

        st.session_state["history"].append(
            project_data
        )

        st.query_params.clear()

        st.success(
            "✅ Project information saved successfully!"
        )

        st.info(
            "Go to Analysis, AI Mentor, or Roadmap to continue 🚀"
        )