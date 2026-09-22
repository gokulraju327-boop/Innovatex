import re
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from utils.ai_engine import get_ai_report, get_ai_scores, get_ai_roadmap
import json


def clean_for_pdf(text):
    # Remove markdown headers
    text = re.sub(r'#{1,6}\s*', '', text)

    # Remove bold/italic markers
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)

    # Remove horizontal rules
    text = re.sub(r'---+', '', text)

    # Remove table rows
    text = re.sub(r'\|.*', '', text)

    # Replace unicode stars/bullets with dash
    text = re.sub(r'[★☆✓•·]', '-', text)

    # Remove non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # Split into lines
    lines = [line.strip() for line in text.split('\n')]

    # Remove empty lines
    lines = [line for line in lines if line]

    return lines


def show_pdf_report():

    st.title("📄 AI PDF Report Generator")

    # --------------------------------------------------
    # Get Active Project
    # --------------------------------------------------

    project = st.session_state.get("project")

    # --------------------------------------------------
    # New Project Mode
    # --------------------------------------------------

    if project is None and st.session_state.get(
        "new_project_mode",
        False
    ):

        st.warning("🆕 No active project yet.")

        st.info(
            "Please complete your new project details in "
            "💡 Idea Evaluation and click 🚀 Analyze My Idea."
        )

        return

    # --------------------------------------------------
    # No Project
    # --------------------------------------------------

    if project is None:

        st.warning(
            "⚠️ Please evaluate a project first."
        )

        st.info(
            "Go to 💡 Idea Evaluation and create a project."
        )

        return

    # --------------------------------------------------
    # Active Project
    # --------------------------------------------------

    st.success(
        f"📄 Report for: {project['title']}"
    )

    st.subheader(
        f"🚀 {project['title']}"
    )

    # --------------------------------------------------
    # Project Information
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

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

    # --------------------------------------------------
    # Generate PDF
    # --------------------------------------------------

    st.divider()

    if st.button("📥 Generate AI Report PDF"):

        # --------------------------------------------------
        # Generate AI Data
        # --------------------------------------------------

        with st.spinner(
            "🤖 Generating AI report..."
        ):

            raw_scores = get_ai_scores(project)

            try:

                start = raw_scores.find("{")
                end = raw_scores.rfind("}") + 1

                clean_json = raw_scores[start:end]

                scores = json.loads(clean_json)

            except Exception:

                st.error(
                    "⚠️ Score parsing failed."
                )

                return

            roadmap = get_ai_roadmap(project)

            report_text = get_ai_report(
                project,
                scores,
                roadmap
            )

        # --------------------------------------------------
        # PDF Creation
        # --------------------------------------------------

        file_name = "InnovateX_AI_Report.pdf"

        doc = SimpleDocTemplate(
            file_name,
            pagesize=A4
        )

        styles = getSampleStyleSheet()

        story = []

        # --------------------------------------------------
        # PDF Header
        # --------------------------------------------------

        story.append(
            Paragraph(
                "InnovateX AI Report",
                styles["Title"]
            )
        )

        story.append(
            Spacer(1, 12)
        )

        # --------------------------------------------------
        # Project Details
        # --------------------------------------------------

        story.append(
            Paragraph(
                f"<b>Title:</b> {project['title']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Domain:</b> {project['domain']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Team Size:</b> {project['team_size']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Skill Level:</b> {project['skill']}",
                styles["Normal"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Duration:</b> {project['duration']}",
                styles["Normal"]
            )
        )

        story.append(
            Spacer(1, 12)
        )

        # --------------------------------------------------
        # AI Report
        # --------------------------------------------------

        story.append(
            Paragraph(
                "<b>AI Generated Report:</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Spacer(1, 8)
        )

        # --------------------------------------------------
        # Add Report Lines
        # --------------------------------------------------

        for line in clean_for_pdf(report_text):

            try:

                story.append(
                    Paragraph(
                        line,
                        styles["Normal"]
                    )
                )

                story.append(
                    Spacer(1, 4)
                )

            except Exception:

                # Last resort
                safe = re.sub(
                    r'[^\x20-\x7E]',
                    '',
                    line
                )

                if safe:

                    story.append(
                        Paragraph(
                            safe,
                            styles["Normal"]
                        )
                    )

                    story.append(
                        Spacer(1, 4)
                    )

        # --------------------------------------------------
        # Build PDF
        # --------------------------------------------------

        doc.build(story)

        # --------------------------------------------------
        # Download Button
        # --------------------------------------------------

        with open(file_name, "rb") as f:

            st.download_button(
                "⬇️ Download AI Report PDF",
                f,
                file_name="InnovateX_AI_Report.pdf",
                mime="application/pdf"
            )

        st.success(
            "✅ AI PDF Report Generated!"
        )