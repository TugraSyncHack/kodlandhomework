import aiosqlite

class DatabaseManager:
    def __init__(self, db_path="project_data.db"):
        self.db_path = db_path

    async def initialize(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    xp INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()

    async def sync_user(self, user_id, username):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO users (user_id, username) 
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET 
                username = excluded.username,
                last_active = CURRENT_TIMESTAMP
            """, (user_id, username))
            await db.commit()

    async def add_xp(self, user_id, amount):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE users SET xp = xp + ? WHERE user_id = ?",
                (amount, user_id)
            )
            await db.execute(
                "UPDATE users SET level = (xp / 100) + 1 WHERE user_id = ?",
                (user_id,)
            )
            await db.commit()

    async def get_user_stats(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT xp, level FROM users WHERE user_id = ?", (user_id,)) as cursor:
                return await cursor.fetchone()

    async def get_leaderboard(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT username, level, xp FROM users ORDER BY xp DESC LIMIT 10") as cursor:
                return await cursor.fetchall()
