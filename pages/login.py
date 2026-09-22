import streamlit as st
from database.db import create_user, authenticate_user


def show_login():

    st.markdown(
        """
        <style>

        .login-title {
            text-align: center;
            font-size: 40px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .login-subtitle {
            text-align: center;
            color: gray;
            margin-bottom: 30px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-title">🚀 InnovateX</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">'
        'AI Innovation & Hackathon Mentor'
        '</div>',
        unsafe_allow_html=True
    )

    # ==================================================
    # LOGIN / REGISTER TABS
    # ==================================================

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    # ==================================================
    # LOGIN
    # ==================================================

    with login_tab:

        st.subheader("Welcome Back 👋")

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            use_container_width=True
        ):

            if not email.strip() or not password:

                st.error(
                    "Please enter your email and password."
                )

            else:

                user = authenticate_user(
                    email.strip().lower(),
                    password
                )

                if user:

                    st.session_state["logged_in"] = True

                    st.session_state["user"] = user

                    st.success(
                        f"Welcome back, {user['name']}! 🚀"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid email or password."
                    )

    # ==================================================
    # REGISTER
    # ==================================================

    with register_tab:

        st.subheader("Create Your Account 🚀")

        name = st.text_input(
            "Full Name",
            placeholder="Enter your name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            placeholder="example@email.com",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="register_confirm_password"
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True
        ):

            if (
                not name.strip()
                or not email.strip()
                or not password
                or not confirm_password
            ):

                st.error(
                    "Please fill all the fields."
                )

            elif password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            elif len(password) < 6:

                st.error(
                    "⚠️ Password must contain at least 6 characters."
                )

            else:

                success, message = create_user(
                    name.strip(),
                    email.strip().lower(),
                    password
                )

                if success:

                    st.success(
                        "✅ Account created successfully!"
                    )

                    st.info(
                        "You can now login using your email and password."
                    )

                else:

                    st.error(
                        f"❌ {message}"
                    )