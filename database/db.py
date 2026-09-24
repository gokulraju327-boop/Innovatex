import hashlib
import os

from dotenv import load_dotenv
from supabase import create_client


# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase environment variables are missing.")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def init_db():
    """
    Supabase tables are already created in the Supabase dashboard.
    Nothing needs to be created locally.
    """
    pass


def create_user(name, email, password):
    try:
        hashed_password = hash_password(password)

        supabase.table("users").insert({
            "name": name,
            "email": email,
            "password": hashed_password
        }).execute()

        return True, "Account created successfully."

    except Exception as e:
        error_message = str(e)

        if "duplicate key" in error_message.lower() or "23505" in error_message:
            return False, "Email already registered."

        return False, error_message


def authenticate_user(email, password):
    try:
        hashed_password = hash_password(password)

        response = (
            supabase
            .table("users")
            .select("id, name, email")
            .eq("email", email)
            .eq("password", hashed_password)
            .limit(1)
            .execute()
        )

        if response.data:
            user = response.data[0]

            return {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }

        return None

    except Exception as e:
        print("Authentication Error:", e)
        return None


def save_project(project, user_id=None):
    try:
        data = {
            "title": project["title"],
            "domain": project["domain"],
            "description": project["description"],
            "team_size": project["team_size"],
            "duration": project["duration"],
            "skill": project["skill"],
            "tech_stack": project["tech_stack"],
            "target_users": project["target_users"],
            "problem": project["problem"],
            "user_id": user_id
        }

        supabase.table("projects").insert(data).execute()

        return True

    except Exception as e:
        print("Save Project Error:", e)
        return False


def get_project_count(user_id=None):
    try:
        query = (
            supabase
            .table("projects")
            .select("id", count="exact", head=True)
        )

        if user_id is not None:
            query = query.eq("user_id", user_id)

        response = query.execute()

        return response.count or 0

    except Exception as e:
        print("Project Count Error:", e)
        return 0


def get_projects(user_id=None):
    try:
        query = (
            supabase
            .table("projects")
            .select(
                "title, domain, skill, team_size, problem, created_at"
            )
        )

        if user_id is not None:
            query = query.eq("user_id", user_id)

        response = (
            query
            .order("id", desc=True)
            .execute()
        )

        projects = []

        for project in response.data:
            projects.append((
                project.get("title"),
                project.get("domain"),
                project.get("skill"),
                project.get("team_size"),
                project.get("problem"),
                project.get("created_at")
            ))

        return projects

    except Exception as e:
        print("Get Projects Error:", e)
        return []


def get_latest_project(user_id=None):
    try:
        query = (
            supabase
            .table("projects")
            .select(
                "title, domain, description, team_size, duration, "
                "skill, tech_stack, target_users, problem"
            )
        )

        if user_id is not None:
            query = query.eq("user_id", user_id)

        response = (
            query
            .order("id", desc=True)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        project = response.data[0]

        tech_stack = project.get("tech_stack") or ""

        return {
            "title": project.get("title"),
            "domain": project.get("domain"),
            "description": project.get("description"),
            "team_size": project.get("team_size"),
            "duration": project.get("duration"),
            "skill": project.get("skill"),
            "tech_stack": [
                item.strip()
                for item in tech_stack.split(",")
                if item.strip()
            ],
            "target_users": project.get("target_users"),
            "problem": project.get("problem")
        }

    except Exception as e:
        print("Latest Project Error:", e)
        return None


init_db()