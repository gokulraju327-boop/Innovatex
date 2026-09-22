import sqlite3
from pathlib import Path
import hashlib


DB_PATH = Path(__file__).parent / "innovatex.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def init_db():
    conn = get_connection()

    # Users table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Projects table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            domain TEXT,
            description TEXT,
            team_size INTEGER,
            duration TEXT,
            skill TEXT,
            tech_stack TEXT,
            target_users TEXT,
            problem TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Add user_id to old projects table if it does not exist
    columns = conn.execute(
        "PRAGMA table_info(projects)"
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "user_id" not in column_names:
        conn.execute(
            "ALTER TABLE projects ADD COLUMN user_id INTEGER"
        )

    conn.commit()
    conn.close()


def create_user(name, email, password):
    conn = get_connection()

    try:
        hashed_password = hash_password(password)

        conn.execute(
            """
            INSERT INTO users (
                name,
                email,
                password
            )
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                hashed_password
            )
        )

        conn.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "Email already registered."

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()


def authenticate_user(email, password):
    conn = get_connection()

    hashed_password = hash_password(password)

    cursor = conn.execute(
        """
        SELECT id, name, email
        FROM users
        WHERE email = ?
        AND password = ?
        """,
        (
            email,
            hashed_password
        )
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2]
        }

    return None


def save_project(project, user_id=None):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO projects (
            title,
            domain,
            description,
            team_size,
            duration,
            skill,
            tech_stack,
            target_users,
            problem,
            user_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            project["title"],
            project["domain"],
            project["description"],
            project["team_size"],
            project["duration"],
            project["skill"],
            ", ".join(project["tech_stack"]),
            project["target_users"],
            project["problem"],
            user_id
        )
    )

    conn.commit()
    conn.close()


def get_project_count(user_id=None):
    conn = get_connection()

    if user_id is None:
        cursor = conn.execute(
            "SELECT COUNT(*) FROM projects"
        )
    else:
        cursor = conn.execute(
            """
            SELECT COUNT(*)
            FROM projects
            WHERE user_id = ?
            """,
            (user_id,)
        )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_projects(user_id=None):
    conn = get_connection()

    if user_id is None:
        cursor = conn.execute(
            """
            SELECT
                title,
                domain,
                skill,
                team_size,
                problem,
                created_at
            FROM projects
            ORDER BY id DESC
            """
        )
    else:
        cursor = conn.execute(
            """
            SELECT
                title,
                domain,
                skill,
                team_size,
                problem,
                created_at
            FROM projects
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )

    projects = cursor.fetchall()

    conn.close()

    return projects


def get_latest_project(user_id=None):
    conn = get_connection()

    if user_id is None:
        cursor = conn.execute(
            """
            SELECT
                title,
                domain,
                description,
                team_size,
                duration,
                skill,
                tech_stack,
                target_users,
                problem
            FROM projects
            ORDER BY id DESC
            LIMIT 1
            """
        )
    else:
        cursor = conn.execute(
            """
            SELECT
                title,
                domain,
                description,
                team_size,
                duration,
                skill,
                tech_stack,
                target_users,
                problem
            FROM projects
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )

    project = cursor.fetchone()

    conn.close()

    if not project:
        return None

    return {
        "title": project[0],
        "domain": project[1],
        "description": project[2],
        "team_size": project[3],
        "duration": project[4],
        "skill": project[5],
        "tech_stack": [
            item.strip()
            for item in project[6].split(",")
            if item.strip()
        ] if project[6] else [],
        "target_users": project[7],
        "problem": project[8]
    }


# Initialize database
init_db()