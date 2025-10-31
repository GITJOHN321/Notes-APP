import sqlite3

DB_NAME = "notas.db"

def get_conn():
    return sqlite3.connect(DB_NAME)

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