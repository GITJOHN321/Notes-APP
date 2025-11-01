import os
from pathlib import Path
from sqlcipher3 import dbapi2 as sqlite

APP_DIR = Path.home() / ".local" / "share" / "miapp"
DB_PATH = APP_DIR / "notas.db"
KEY_PATH = APP_DIR / "key.bin"


def ensure_secure_env():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(APP_DIR, 0o700)

    if not KEY_PATH.exists():
        # 🔐 Generar clave aleatoria y guardarla con permisos 600
        key = os.urandom(32).hex()
        KEY_PATH.write_text(key)
        os.chmod(KEY_PATH, 0o600)
    else:
        key = KEY_PATH.read_text().strip()

    return key


def get_conn():
    key = ensure_secure_env()
    conn = sqlite.connect(str(DB_PATH))
    conn.execute(f"PRAGMA key='{key}';")
    conn.execute("PRAGMA cipher_memory_security = ON;")
    return conn

#def get_conn():
    #return sqlite3.connect(DB_NAME)

def create_table():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id_note INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL
            )
        """)
        conn.commit() 

def get_all_notes():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes")
        return cursor.fetchall()

def get_note_by_id(id_note):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE id_note = ?",(id_note))
        return cursor.fetchone()

def add_note(title, body):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (title, body) VALUES (?,?)",(title, body))
        conn.commit()
        return cursor.lastrowid
        
def update_note(id_note, title=None, body=None):
    campos=[]
    valores=[]

    if title is not None:
        campos.append("title = ?")
        valores.append(title)

    if body is not None:
        campos.append("body = ?")
        valores.append(body)

    if not campos:
        print("⚠️ No hay campos para actualizar.")
        return

    sql = f"UPDATE notes SET {', '.join(campos)} WHERE id_note = ?"
    valores.append(id_note)

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(sql,valores)
        conn.commit()

def delete_note(id_note):
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id_note = ?",(id_note,))
        conn.commit()

def delete_notes_batch(ids):
    """Elimina múltiples notas por lista de IDs."""
    if not ids:
        return

    with get_conn() as conn:
        cursor = conn.cursor()
        placeholders = ','.join(['?'] * len(ids))
        query = f"DELETE FROM notes WHERE id_note IN ({placeholders})"
        cursor.execute(query, ids)
        conn.commit()

