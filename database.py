import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                conv_type TEXT,
                summary TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def register_user(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        await db.commit()

async def save_history_log(user_id: int, conv_type: str, summary: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO history (user_id, conv_type, summary) VALUES (?, ?, ?)", (user_id, conv_type, summary))
        await db.commit()

async def get_user_history(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT conv_type, summary FROM history WHERE user_id = ? ORDER BY id DESC LIMIT 5", (user_id,)) as cursor:
            return [{"type": row[0], "summary": row[1]} for row in await cursor.fetchall()]

