import os
from pathlib import Path
from sqlcipher3 import dbapi2 as sqlite
from entities.note import Note  # ← Importamos la entidad del dominio

# 📁 Rutas seguras
APP_DIR = Path.home() / ".local" / "share" / "test"
DB_PATH = APP_DIR / "notas.db"
KEY_PATH = APP_DIR / "key.bin"

# ==========================================================
# 🔐 Manejo seguro de entorno y clave
# ==========================================================
def ensure_secure_env():
    APP_DIR.mkdir(parents=True, exist_ok=True)
    os.chmod(APP_DIR, 0o700)

    if not KEY_PATH.exists():
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


# ==========================================================
# 🧱 Inicialización de tabla
# ==========================================================
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


# ==========================================================
# 📥 CRUD usando entidades Note
# ==========================================================
def get_all_notes():
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes")
        return cursor.fetchall()

def insert_note(note: Note):
    """Inserta una nota en la BD y actualiza su ID."""
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (title, body) VALUES (?, ?)",
            (note.title, note.body)
        )
        conn.commit()
        note.id = cursor.lastrowid
        return note.id


def update_note(note: Note):
    """
    Actualiza una nota existente. 
    Solo usa los valores del objeto Note.
    """
    if not note.id:
        raise ValueError("La nota debe tener un ID para ser actualizada")

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE notes SET title = ?, body = ? WHERE id_note = ?",
            (note.title, note.body, note.id)
        )
        conn.commit()


def delete_note(note: Note | int):
    """Elimina una nota por objeto Note o por ID."""
    note_id = note.id if isinstance(note, Note) else note
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE id_note = ?", (note_id,))
        conn.commit()


def delete_notes_batch(notes: list[Note] | list[int]):
    """Elimina múltiples notas (pueden ser objetos o IDs)."""
    if not notes:
        return

    # Convertimos a lista de IDs
    ids = [n.id if isinstance(n, Note) else n for n in notes]

    with get_conn() as conn:
        cursor = conn.cursor()
        placeholders = ",".join(["?"] * len(ids))
        query = f"DELETE FROM notes WHERE id_note IN ({placeholders})"
        cursor.execute(query, ids)
        conn.commit()


