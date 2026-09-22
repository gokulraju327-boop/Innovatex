from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY)

MODEL = "openai/gpt-oss-20b"


# -----------------------------
# GENERAL AI RESPONSE
# -----------------------------
def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"


# -----------------------------
# AI PROJECT EVALUATION
# -----------------------------
def get_ai_scores(project):

    prompt = f"""You are an expert hackathon judge.

Evaluate the following project fairly and realistically.

Project Title: {project['title']}
Domain: {project['domain']}
Description: {project['description']}
Problem Statement: {project['problem']}
Target Users: {project['target_users']}
Team Size: {project['team_size']}
Skill Level: {project['skill']}
Hackathon Duration: {project['duration']}
Tech Stack: {project['tech_stack']}

Give scores from 0 to 100 based on:

- Innovation: originality and uniqueness
- Feasibility: technical and practical possibility
- Market Potential: usefulness, users and scalability
- Overall: combined evaluation

Also provide exactly:
- 3 strengths
- 3 weaknesses
- 3 improvement suggestions
- 1 short professional judge feedback

Return ONLY valid JSON.
Do not use markdown.
Do not add any text outside JSON.

JSON format:

{{
    "innovation": 0,
    "feasibility": 0,
    "market": 0,
    "overall": 0,

    "strengths": [
        "Strength 1",
        "Strength 2",
        "Strength 3"
    ],

    "weaknesses": [
        "Weakness 1",
        "Weakness 2",
        "Weakness 3"
    ],

    "suggestions": [
        "Suggestion 1",
        "Suggestion 2",
        "Suggestion 3"
    ],

    "judge_feedback": "Short professional feedback from a hackathon judge."
}}"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=700
        )

        text = response.choices[0].message.content.strip()

        # Remove markdown code block if AI adds it
        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        data = json.loads(text)

        required_keys = [
            "innovation",
            "feasibility",
            "market",
            "overall",
            "strengths",
            "weaknesses",
            "suggestions",
            "judge_feedback"
        ]

        for key in required_keys:

            if key not in data:
                raise ValueError(f"Missing AI field: {key}")

        return json.dumps(data)

    except Exception as e:

        print("AI Score Error:", e)

        return json.dumps({
            "innovation": 70,
            "feasibility": 70,
            "market": 70,
            "overall": 70,

            "strengths": [
                "Clear project concept",
                "Addresses a real-world problem",
                "Has potential for further development"
            ],

            "weaknesses": [
                "More detailed implementation is needed",
                "Scalability needs further planning",
                "User validation should be strengthened"
            ],

            "suggestions": [
                "Add a working prototype",
                "Validate the solution with target users",
                "Prepare a clear scalability plan"
            ],

            "judge_feedback": "The project has potential, but stronger validation and implementation details would improve its hackathon evaluation."
        })


# -----------------------------
# AI ROADMAP
# -----------------------------
def get_ai_roadmap(project):

    prompt = f"""Create a detailed 8-week roadmap for this hackathon project.

Title: {project['title']}
Domain: {project['domain']}
Description: {project['description']}
Tech Stack: {project['tech_stack']}

Format:

Week 1:
Week 2:
Week 3:
Week 4:
Week 5:
Week 6:
Week 7:
Week 8:
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Roadmap Error:\n{str(e)}"


# -----------------------------
# AI PDF REPORT
# -----------------------------
def get_ai_report(project, scores, roadmap):

    prompt = f"""You are an expert hackathon evaluator.

Project: {project['title']}

Scores:
{scores}

Roadmap:
{roadmap}

Generate a professional report containing:

1. Executive Summary
2. Innovation Analysis
3. Strengths
4. Weaknesses
5. Suggested Improvements
6. Final Verdict
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Report Error:\n{str(e)}"


# -----------------------------
# AI MENTOR
# -----------------------------
def get_ai_mentor_response(messages: list):

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI Innovation & Hackathon Mentor. Help students build, evaluate, and improve their projects."
                }
            ] + messages,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"AI Error: {str(e)}"