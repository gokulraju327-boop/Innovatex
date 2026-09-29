import streamlit as st
from streamlit_option_menu import option_menu


def show_sidebar():

    with st.sidebar:

        # ==================================================
        # SIDEBAR STYLE
        # ==================================================

        st.markdown(
            """
            <style>

            /* Sidebar background */
            section[data-testid="stSidebar"] {
                background-color: var(--background-color) !important;
            }

            /* Sidebar text */
            section[data-testid="stSidebar"] * {
                color: var(--text-color);
            }

            /* Sidebar title */
            .innovatex-sidebar-title {
                text-align: center;
                color: var(--text-color) !important;
                font-size: 27px;
                font-weight: 700;
                margin-bottom: 4px;
            }

            /* Sidebar subtitle */
            .innovatex-sidebar-subtitle {
                text-align: center;
                color: var(--secondary-text-color) !important;
                font-size: 13px;
                margin-bottom: 20px;
            }

            /* User name */
            .innovatex-user-name {
                color: var(--text-color) !important;
                font-size: 16px;
                font-weight: 600;
            }

            /* User email */
            .innovatex-user-email {
                color: var(--secondary-text-color) !important;
                font-size: 12px;
            }

            /* Sidebar menu */
            section[data-testid="stSidebar"] .nav-link {
                color: var(--text-color) !important;
                background-color: transparent !important;
                border-radius: 10px;
            }

            section[data-testid="stSidebar"] .nav-link .icon {
                color: var(--text-color) !important;
            }

            /* Hover */
            section[data-testid="stSidebar"] .nav-link:hover {
                background-color: var(--secondary-background-color) !important;
                color: var(--text-color) !important;
            }

            section[data-testid="stSidebar"] .nav-link:hover .icon {
                color: var(--text-color) !important;
            }

            /* Selected menu */
            section[data-testid="stSidebar"] .nav-link-selected {
                background-color: #EF4444 !important;
                color: #FFFFFF !important;
                font-weight: 600;
            }

            section[data-testid="stSidebar"] .nav-link-selected .icon {
                color: #FFFFFF !important;
            }

            /* Logout button */
            section[data-testid="stSidebar"] .stButton button {
                background-color: var(--secondary-background-color) !important;
                color: var(--text-color) !important;
                border: 1px solid var(--secondary-background-color) !important;
                border-radius: 10px;
            }

            section[data-testid="stSidebar"] .stButton button:hover {
                opacity: 0.85;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        # ==================================================
        # TITLE
        # ==================================================

        st.markdown(
            '<div class="innovatex-sidebar-title">🚀 InnovateX</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="innovatex-sidebar-subtitle">'
            'AI Innovation & Hackathon Mentor'
            '</div>',
            unsafe_allow_html=True
        )

        st.divider()

        # ==================================================
        # USER INFORMATION
        # ==================================================

        user = st.session_state.get("user")

        if user:

            st.markdown(
                f'<div class="innovatex-user-name">'
                f'👤 {user["name"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<div class="innovatex-user-email">'
                f'📧 {user["email"]}'
                f'</div>',
                unsafe_allow_html=True
            )

            st.divider()

        # ==================================================
        # MENU
        # ==================================================

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
                "About"
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
                "info-circle-fill"
            ],

            default_index=0,

            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent"
                },

                "icon": {
                    "font-size": "17px"
                },

                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "4px 0",
                    "padding": "11px 14px",
                    "border-radius": "10px"
                },

                "nav-link-selected": {
                    "background-color": "#EF4444",
                    "color": "#FFFFFF",
                    "font-weight": "600"
                },

                "nav-link:hover": {
                    "background-color": "transparent"
                }
            }
        )

        # ==================================================
        # LOGOUT
        # ==================================================

        st.divider()

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            st.session_state.clear()
            st.rerun()

    return selected