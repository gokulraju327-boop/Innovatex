from groq import Groq
import json
import os

API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY)
MODEL = "llama3-8b-8192"


def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"


def get_ai_scores(project):
    prompt = f"""You are an expert hackathon judge.

Evaluate the project below.

Title: {project['title']}
Domain: {project['domain']}
Description: {project['description']}
Problem: {project['problem']}
Tech Stack: {project['tech_stack']}

Return ONLY valid JSON, no extra text, no markdown:

{{
    "innovation": 90,
    "feasibility": 85,
    "market": 88,
    "overall": 88
}}"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256
        )
        text = response.choices[0].message.content.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        json.loads(text)
        return text

    except Exception as e:
        print(e)
        return json.dumps({
            "innovation": 70,
            "feasibility": 70,
            "market": 70,
            "overall": 70
        })


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
Week 8:"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Roadmap Error:\n{str(e)}"


def get_ai_report(project, scores, roadmap):
    prompt = f"""You are an expert hackathon evaluator.

Project: {project['title']}
Scores: {scores}
Roadmap: {roadmap}

Generate a professional report containing:
1. Executive Summary
2. Innovation Analysis
3. Strengths
4. Weaknesses
5. Suggested Improvements
6. Final Verdict"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Report Error:\n{str(e)}"


def get_ai_mentor_response(messages: list):
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert AI Innovation & Hackathon Mentor. Help students build, evaluate, and improve their projects."}
            ] + messages,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"