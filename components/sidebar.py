from streamlit_option_menu import option_menu
import streamlit as st


def show_sidebar():

    with st.sidebar:

        # Logo
        st.markdown(
            """
            <h2 style='text-align:center;color:#4F46E5;'>
            🚀 InnovateX
            </h2>

            <p style='text-align:center;color:gray;'>
            AI Innovation & Hackathon Mentor
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # Logged-in user
        user = st.session_state.get("user")

        if user:

            st.markdown(
                f"""
                <div style="
                    padding:12px;
                    border-radius:12px;
                    background:#F8FAFC;
                    margin-bottom:15px;
                ">
                    <b>👤 {user["name"]}</b><br>
                    <small>{user["email"]}</small>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Navigation
        selected = option_menu(
            menu_title=None,

            options=[
                "Dashboard",
                "Idea Evaluation",
                "Analysis",
                "AI Mentor",
                "Roadmap",
                "PDF Report",
                "History",
                "Profile",
                "About",
            ],

            icons=[
                "house-fill",
                "lightbulb-fill",
                "bar-chart-fill",
                "robot",
                "map-fill",
                "file-earmark-pdf-fill",
                "clock-history",
                "person-circle",
                "info-circle-fill",
            ],

            default_index=0,
        )

        st.divider()

        # Logout
        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            st.session_state.clear()
            st.rerun()

    return selected