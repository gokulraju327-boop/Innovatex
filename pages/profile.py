import streamlit as st
from database.db import get_project_count


def show_profile():
    st.title("👤 My Profile")
    st.write("Manage your InnovateX account and project activity.")

    user = st.session_state.get("user")

    if not user:
        st.warning("⚠️ Please login again.")
        return

    user_id = user["id"]
    project_count = get_project_count(user_id)

    st.markdown(
        """
        <style>
        .profile-card {
            padding: 20px;
            border-radius: 15px;
            background: var(--secondary-background-color);
            border: 1px solid rgba(128, 128, 128, 0.25);
            margin-bottom: 15px;
        }

        .profile-card h4 {
            margin-bottom: 8px;
            color: var(--text-color);
        }

        .profile-card p {
            color: var(--text-color);
            margin-bottom: 0;
        }

        .profile-hero {
            padding: 30px;
            border-radius: 20px;
            background: linear-gradient(135deg, #2563EB, #7C3AED);
            color: white;
            margin-bottom: 25px;
        }

        .profile-hero h1 {
            color: white !important;
            margin-bottom: 5px;
        }

        .profile-hero p {
            color: white !important;
            font-size: 17px;
            margin-bottom: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="profile-hero">
            <h1>👋 Welcome, {user["name"]}</h1>
            <p>Your InnovateX innovation workspace</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📋 Account Information")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="profile-card">
                <h4>👤 Full Name</h4>
                <p>{user["name"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="profile-card">
                <h4>📧 Email</h4>
                <p>{user["email"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("📊 Your Activity")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("💡 Projects", project_count)

    with c2:
        st.metric("🤖 AI Mentor", "Ready")

    with c3:
        st.metric("🚀 Account", "Active")

    st.divider()

    st.subheader("🔐 Account Status")

    st.success("✅ Your InnovateX account is active.")

    st.info(
        "Your projects and evaluation history are connected to your account."
    )

    st.divider()

    st.caption("🚀 InnovateX — AI Innovation & Hackathon Mentor")