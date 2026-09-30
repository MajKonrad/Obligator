import sqlite3

connection = sqlite3.connect("resources.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course TEXT NOT NULL,
    description TEXT NOT NULL, 
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    added_by TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

)
""")

connection.commit()


def detect_resource_type(url):
    if "youtube.com" in url.lower() or "youtu.be" in url.lower():
        return "youtube"
    if "github.com" in url.lower():
        return "github"
    if url.lower().endswith(".pdf"):
        return "pdf"
    return "website"

def add_resource(course, title, description, url, added_by):
    resource_type = detect_resource_type(url)
    try:
        cursor.execute("""
        INSERT INTO resources (
            course,
            title,
            description,
            url,
            type,
            added_by
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            course,
            title,
            description,
            url,
            resource_type,
            added_by
        ))

        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False


print("Ressurs lagt til!")