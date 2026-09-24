import streamlit as st
from utils.ai_engine import get_ai_scores
import json
import re
import html


def show_analysis():

    st.title("📊 AI Evaluation Report")

    # ==================================================
    # ACTIVE PROJECT ONLY
    # ==================================================

    project = st.session_state.get("project")

    if project is None:

        st.warning("🆕 No active project.")

        st.info(
            "Please go to 💡 Idea Evaluation, "
            "create a project and click 🚀 Analyze My Idea."
        )

        return

    # ==================================================
    # ACTIVE PROJECT
    # ==================================================

    st.success(
        f"🚀 Evaluating: {project['title']}"
    )

    # ==================================================
    # AI EVALUATION
    # ==================================================

    with st.spinner(
        "🤖 AI is evaluating your project..."
    ):

        raw = get_ai_scores(project)

    # ==================================================
    # PARSE AI RESPONSE
    # ==================================================

    try:

        start = raw.find("{")
        end = raw.rfind("}") + 1

        clean_json = raw[start:end]

        scores = json.loads(clean_json)

    except Exception:

        st.error(
            "⚠️ AI returned an invalid response. "
            "Please try again."
        )

        return

    # ==================================================
    # SAVE LATEST SCORE
    # ==================================================

    st.session_state["latest_score"] = scores["overall"]

    # ==================================================
    # PROJECT SUMMARY
    # ==================================================

    st.subheader("📌 Project Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Project Title:**",
            project["title"]
        )

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

        st.write(
            "**Target Users:**",
            project["target_users"]
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

    st.divider()

    # ==================================================
    # AI SCORE
    # ==================================================

    st.subheader("🏆 AI Score")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "💡 Innovation",
            f"{scores['innovation']}/100"
        )

    with c2:
        st.metric(
            "⚙️ Feasibility",
            f"{scores['feasibility']}/100"
        )

    with c3:
        st.metric(
            "📈 Market Potential",
            f"{scores['market']}/100"
        )

    with c4:
        st.metric(
            "🏆 Overall Score",
            f"{scores['overall']}/100"
        )

    st.divider()

    # ==================================================
    # STRENGTHS
    # ==================================================

    st.subheader("✅ Strengths")

    for strength in scores.get("strengths", []):

        st.success(
            f"✔️ {strength}"
        )

    # ==================================================
    # WEAKNESSES
    # ==================================================

    st.subheader("⚠️ Weaknesses")

    for weakness in scores.get("weaknesses", []):

        st.warning(
            f"⚠️ {weakness}"
        )

    # ==================================================
    # SUGGESTIONS
    # ==================================================

    st.subheader(
        "💡 AI Improvement Suggestions"
    )

    for suggestion in scores.get("suggestions", []):

        st.info(
            f"💡 {suggestion}"
        )

    # ==================================================
    # JUDGE FEEDBACK
    # ==================================================

    st.subheader(
        "👨‍⚖️ Hackathon Judge Feedback"
    )

    judge_feedback = scores.get(
        "judge_feedback",
        "No feedback available."
    )

    # Convert escaped HTML entities if AI returned them
    judge_feedback = html.unescape(
        str(judge_feedback)
    )

    # Remove any HTML tags from AI response
    judge_feedback = re.sub(
        r"<[^>]*>",
        "",
        judge_feedback
    ).strip()

    # Native Streamlit container
    with st.container(border=True):

        st.markdown("### 🤖 AI Judge")

        st.write(judge_feedback)

    # ==================================================
    # FOOTER
    # ==================================================

    st.divider()

    st.caption(
        "🤖 Evaluation generated by InnovateX AI."
    )