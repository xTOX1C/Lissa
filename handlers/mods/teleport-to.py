from highrise import *
from highrise.models import *
import random
        
async def go(self, user: User, message: str) -> None:
    response = await self.highrise.get_room_users()
    users = [content[0] for content in response.content] # extract the user objects
    usernames = [user.username.lower() for user in users] # extract the usernames
    parts = message[1:].split()
    args = parts[1:]
    your_pos = None
        
    if len(args) < 1:
        await self.highrise.send_whisper(user.id, "Usage: !go <@username>")
        return
    elif args[0][0] != "@":
        await self.highrise.send_whisper(user.id, f"Invalid user format. Please use '@username'.")
        return
    elif args[0][1:].lower() not in usernames:
        await self.highrise.send_whisper(user.id, f"{args[0][1:]} is not in the room.")
        return

    user_id = next((u.id for u in users if u.username.lower() == args[0][1:].lower()), None)
    if not user_id:
        await self.highrise.send_whisper(user.id, f"User {args[0][1:]} not found")
        return
        
    for content in response.content:
        if content[0].id == user_id:
            if isinstance(content[1], Position):
                user_pos = content[1]
                break
    if not user_pos:
        await self.highrise.send_whisper(user.id, f"Position not found\nProbably user using furniture.")
        return
    await self.highrise.teleport(user.id, user_pos)