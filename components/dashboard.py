import streamlit as st
from database.db import get_project_count, get_projects


def show_dashboard():

    user = st.session_state.get("user")

    if not user:
        st.warning("⚠️ Please login again.")
        return

    user_id = user["id"]

    # Get user projects
    project_count = get_project_count(user_id)
    projects = get_projects(user_id)

    latest_score = st.session_state.get("latest_score")
    report_count = st.session_state.get("report_count", 0)

    # Custom CSS
    st.markdown(
        """
<style>
.hero {
    padding: 42px 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 44px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 17px;
    margin-bottom: 8px;
}

.section-title {
    margin-top: 25px;
    margin-bottom: 15px;
}

.feature-card {
    padding: 22px;
    border-radius: 18px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    margin-bottom: 15px;
    min-height: 135px;
}

.feature-card h4 {
    margin-top: 0;
}

.recent-card {
    padding: 18px;
    border-radius: 15px;
    background: #F8FAFC;
    border-left: 5px solid #2563EB;
    margin-bottom: 12px;
}
</style>
        """,
        unsafe_allow_html=True
    )

    # Hero
    st.markdown(
        f"""
<div class="hero">
<h1>🚀 InnovateX</h1>

<p>
Welcome back, <b>{user["name"]}</b>! 👋
</p>

<p>
Turn your ideas into smarter,
stronger and hackathon-ready projects.
</p>
</div>
        """,
        unsafe_allow_html=True
    )

    # Statistics
    st.markdown(
        '<h2 class="section-title">📊 Your Innovation Overview</h2>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "💡 Projects",
            project_count
        )

    with c2:
        if latest_score is not None:
            st.metric(
                "🏆 Latest Score",
                f"{latest_score}/100"
            )
        else:
            st.metric(
                "🏆 Latest Score",
                "--"
            )

    with c3:
        st.metric(
            "🤖 AI Mentor",
            "Ready"
        )

    with c4:
        st.metric(
            "📄 Reports",
            report_count
        )

    # Quick Actions
    st.markdown(
        '<h2 class="section-title">⚡ Quick Actions</h2>',
        unsafe_allow_html=True
    )

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button(
            "💡 Evaluate New Idea",
            use_container_width=True
        ):
            st.session_state["dashboard_action"] = "Idea Evaluation"
            st.rerun()

    with q2:
        if st.button(
            "🤖 Ask AI Mentor",
            use_container_width=True
        ):
            st.session_state["dashboard_action"] = "AI Mentor"
            st.rerun()

    with q3:
        if st.button(
            "📚 View History",
            use_container_width=True
        ):
            st.session_state["dashboard_action"] = "History"
            st.rerun()

    # Features
    st.markdown(
        '<h2 class="section-title">✨ InnovateX Features</h2>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
<div class="feature-card">
<h4>💡 AI Idea Evaluation</h4>
<p>
Evaluate your project idea using AI-powered
innovation, feasibility and market analysis.
</p>
</div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="feature-card">
<h4>🧩 Innovation Gap Analyzer</h4>
<p>
Discover missing features, weaknesses
and opportunities in your project.
</p>
</div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="feature-card">
<h4>🤖 AI Project Mentor</h4>
<p>
Get personalized guidance while
designing and building your project.
</p>
</div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
<div class="feature-card">
<h4>🛣️ AI Roadmap Generator</h4>
<p>
Generate a structured development
roadmap based on your project.
</p>
</div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="feature-card">
<h4>📄 Professional PDF Reports</h4>
<p>
Generate professional AI-powered
project evaluation reports.
</p>
</div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
<div class="feature-card">
<h4>📚 Project History</h4>
<p>
Keep track of your previously
evaluated projects.
</p>
</div>
            """,
            unsafe_allow_html=True
        )

    # Recent Projects
    st.markdown(
        '<h2 class="section-title">📌 Recent Projects</h2>',
        unsafe_allow_html=True
    )

    if not projects:

        st.info(
            "No projects evaluated yet. "
            "Start your first project from 💡 Idea Evaluation."
        )

    else:

        for project in projects[:5]:

            title, domain, skill, team_size, problem, created_at = project

            st.markdown(
                f"""
<div class="recent-card">
<b>🚀 {title}</b>

<br><br>

<small>
📂 Domain: {domain}
&nbsp; | &nbsp;
🎯 Skill: {skill}
&nbsp; | &nbsp;
👥 Team: {team_size}
</small>

<br><br>

<small>
🕒 Created: {created_at}
</small>
</div>
                """,
                unsafe_allow_html=True
            )

    # Footer
    st.divider()

    st.caption(
        "🚀 InnovateX — AI Innovation & Hackathon Mentor"
    )