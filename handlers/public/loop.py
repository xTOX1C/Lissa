import asyncio
from highrise import*
from highrise.models import*

class ContinuousEmoteHandler:
    def __init__(self, emote_dict, continuous_emote_tasks):
        self.emote_dict = emote_dict
        self.continuous_emote_tasks = continuous_emote_tasks

    async def start_continuous_emote(self, highrise, emote_name, user_id, delay=1):
        try:
            emote_id = self.emote_dict.get(emote_name)
            
            if user_id in self.continuous_emote_tasks:
                task = self.continuous_emote_tasks.pop(user_id)
                task.cancel()
                try:
                    await asyncio.sleep(0.1)
                    await task
                except asyncio.CancelledError:
                    pass
            
            if emote_id is not None:
                task = asyncio.create_task(self.send_continuous_emote(highrise, emote_id, user_id, delay))
                self.continuous_emote_tasks[user_id] = task
                await highrise.send_whisper(user_id, f"\nSending request\nmaybe won't work in some circumstances")
            else:
                await highrise.send_whisper(user_id, f"Emote '{emote_name}' not found.")
        except Exception as e:
            print(f"error in start_continuous_emote : {e}")

    async def send_continuous_emote(self, highrise, emote_id, user_id, delay):
        try:
            while True:
                await highrise.send_emote(emote_id, user_id)
                await asyncio.sleep(delay)
        except asyncio.CancelledError:
            # Emote was cancelled, restart it immediately
            print(user_id, f"Continuous emote loop for user {user_id} cancelled. Restarting...")
            pass

    async def stop_continuous_emote(self, user_id):
        try:
            if user_id in self.continuous_emote_tasks:
                task = self.continuous_emote_tasks.pop(user_id)
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                await highrise.send_whisper(user_id, f"\nStopped emote loop")
        except Exception as e:
            print(f"error : {e}")
