import asyncio
from database_manager import DatabaseManager

class MyBot:
    def __init__(self):
        self.db = DatabaseManager()

    async def start(self):
        await self.db.initialize()
        print("Sistem başlatıldı.")

    async def handle_message(self, user_id, username, text):
        await self.db.sync_user(user_id, username)
        await self.db.add_xp(user_id, 10)
        
        if text == "!stats":
            stats = await self.db.get_user_stats(user_id)
            return f"Seviye: {stats[1]} | XP: {stats[0]}"
        
        elif text == "!top":
            lb = await self.db.get_leaderboard()
            return "\n".join([f"{i+1}. {u[0]} - Lvl {u[1]}" for i, u in enumerate(lb)])

async def run():
    bot = MyBot()
    await bot.start()
    
    # Simülasyon
    response = await bot.handle_message(12345, "YazilimciDostu", "!stats")
    print(response)

if __name__ == "__main__":
    asyncio.run(run())
