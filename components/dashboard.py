import streamlit as st
from database.db import get_project_count, get_projects


def show_dashboard():

    user = st.session_state.get("user")

    if not user:
        st.warning("⚠️ Please login again.")
        return

    user_id = user.get("id")
    name = user.get("name", "User")
    email = user.get("email", "")

    project_count = get_project_count(user_id)
    projects = get_projects(user_id)

    latest_score = st.session_state.get("latest_score")
    report_count = st.session_state.get("report_count", 0)

    # ==================================================
    # RESPONSIVE MOBILE + DESKTOP CSS
    # ==================================================

    st.markdown(
        """
        <style>

        .innovatex-hero {
            background: linear-gradient(
                135deg,
                #2563EB 0%,
                #3B82F6 50%,
                #7C3AED 100%
            );

            padding: 36px;
            border-radius: 24px;
            margin-bottom: 30px;

            box-shadow:
                0 10px 30px rgba(37, 99, 235, 0.30);

            color: white !important;
        }

        .innovatex-hero h1 {
            color: white !important;
            font-size: 42px !important;
            font-weight: 800 !important;
            margin: 0 0 15px 0 !important;
        }

        .innovatex-hero .welcome {
            color: white !important;
            font-size: 20px !important;
            font-weight: 700 !important;
            margin: 0 0 6px 0 !important;
        }

        .innovatex-hero .email {
            color: #E0E7FF !important;
            font-size: 15px !important;
            margin: 0 0 18px 0 !important;
            word-break: break-word;
        }

        .innovatex-hero .tagline {
            color: white !important;
            font-size: 17px !important;
            margin: 0 !important;
            line-height: 1.5 !important;
        }


        /* ==============================================
           MOBILE RESPONSIVE
           ============================================== */

        @media (max-width: 768px) {

            .innovatex-hero {
                padding: 22px !important;
                border-radius: 18px !important;
                margin-bottom: 20px !important;
            }

            .innovatex-hero h1 {
                font-size: 30px !important;
                margin-bottom: 10px !important;
            }

            .innovatex-hero .welcome {
                font-size: 17px !important;
                margin-bottom: 5px !important;
            }

            .innovatex-hero .email {
                font-size: 13px !important;
                margin-bottom: 12px !important;
                word-break: break-all !important;
            }

            .innovatex-hero .tagline {
                font-size: 14px !important;
                line-height: 1.45 !important;
            }

            h1 {
                font-size: 28px !important;
            }

            h2 {
                font-size: 24px !important;
            }

            h3 {
                font-size: 20px !important;
            }

            .stMetric {
                padding: 8px !important;
            }

            .stMetric label {
                font-size: 13px !important;
            }

            .stMetric [data-testid="stMetricValue"] {
                font-size: 22px !important;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # ==================================================
    # HERO SECTION
    # ==================================================

    st.html(
        f"""
        <div class="innovatex-hero">

            <h1>🚀 InnovateX</h1>

            <p class="welcome">
                👋 Welcome back, {name}!
            </p>

            <p class="email">
                📧 {email}
            </p>

            <p class="tagline">
                Turn your ideas into smarter, stronger and
                hackathon-ready projects.
            </p>

        </div>
        """
    )


    # ==================================================
    # INNOVATION OVERVIEW
    # ==================================================

    st.header("📊 Your Innovation Overview")

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
                "—"
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


    st.divider()


    # ==================================================
    # QUICK ACTIONS
    # ==================================================

    st.header("⚡ Quick Actions")

    q1, q2, q3 = st.columns(3)

    with q1:

        if st.button(
            "💡 Evaluate New Idea",
            use_container_width=True
        ):

            st.session_state["dashboard_action"] = (
                "Idea Evaluation"
            )

            st.rerun()


    with q2:

        if st.button(
            "🤖 Ask AI Mentor",
            use_container_width=True
        ):

            st.session_state["dashboard_action"] = (
                "AI Mentor"
            )

            st.rerun()


    with q3:

        if st.button(
            "📚 View History",
            use_container_width=True
        ):

            st.session_state["dashboard_action"] = (
                "History"
            )

            st.rerun()


    st.divider()


    # ==================================================
    # FEATURES
    # ==================================================

    st.header("✨ InnovateX Features")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("💡 AI Idea Evaluation")

            st.write(
                "Evaluate your project idea using "
                "AI-powered innovation, feasibility "
                "and market analysis."
            )


        with st.container(border=True):

            st.subheader("🧩 Innovation Gap Analyzer")

            st.write(
                "Discover missing features, weaknesses "
                "and opportunities in your project."
            )


        with st.container(border=True):

            st.subheader("🤖 AI Project Mentor")

            st.write(
                "Get personalized guidance while "
                "designing and building your project."
            )


    with col2:

        with st.container(border=True):

            st.subheader("🛣️ AI Roadmap Generator")

            st.write(
                "Generate a structured development "
                "roadmap based on your project."
            )


        with st.container(border=True):

            st.subheader("📄 Professional PDF Reports")

            st.write(
                "Generate professional AI-powered "
                "project evaluation reports."
            )


        with st.container(border=True):

            st.subheader("📚 Project History")

            st.write(
                "Keep track of your previously "
                "evaluated projects."
            )


    st.divider()


    # ==================================================
    # RECENT PROJECTS
    # ==================================================

    st.header("📌 Recent Projects")


    if not projects:

        st.info(
            "No projects evaluated yet. "
            "Start your first project from "
            "💡 Idea Evaluation."
        )

    else:

        for project in projects[:5]:

            (
                title,
                domain,
                skill,
                team_size,
                problem,
                created_at
            ) = project

            with st.container(border=True):

                st.subheader(
                    f"🚀 {title}"
                )

                st.write(
                    f"📂 **Domain:** {domain}"
                )

                st.write(
                    f"🎯 **Skill:** {skill}   |   "
                    f"👥 **Team:** {team_size}"
                )

                st.caption(
                    f"🕒 Created: {created_at}"
                )


    st.divider()


    st.caption(
        "🚀 InnovateX — AI Innovation & Hackathon Mentor"
    )