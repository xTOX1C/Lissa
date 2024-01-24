import highrise
from highrise import*
from highrise import (
    BaseBot,
    ChatEvent,
    Highrise,
    __main__,
    UserJoinedEvent,
    UserLeftEvent,
)
from highrise.models import (
    GetMessagesRequest,
    AnchorPosition,
    ChannelEvent,
    ChannelRequest,
    ChatEvent,
    ChatRequest,
    CurrencyItem,
    EmoteEvent,
    EmoteRequest,
    Error,
    FloorHitRequest,
    GetRoomUsersRequest,
    GetWalletRequest,
    IndicatorRequest,
    Item,
    Position,
    Reaction,
    ReactionEvent,
    ReactionRequest,
    SessionMetadata,
    TeleportRequest,
    TipReactionEvent,
    User,
    UserJoinedEvent,
    UserLeftEvent,
)
from asyncio import run as arun
from handlers.public.loop import ContinuousEmoteHandler
import requests
import random
import asyncio
import os
import sys
import json
import time
import importlib

class BotDefinition:
    def __init__(self, bot, room_id, api_token):
        self.bot = bot
        self.room_id = room_id
        self.api_token = api_token

class Bot(BaseBot):

    def __init__(self,  *args, **kwargs):
        super().__init__( *args, **kwargs)

        with open("mods.json", "r") as e:
           self._mods = json.load(e)                   

        with open("emote.json", "r") as f:
            self.emotes = json.load(f)

            self.continuous_emote_tasks = {} 
            self.continuous_emote_handler = ContinuousEmoteHandler(self.emotes, self.continuous_emote_tasks)


    async def on_start(self, SessionMetadata: SessionMetadata) -> None:
        try:
            print("alive")
            await self.highrise.walk_to(AnchorPosition(entity_id='65a963e9000000000000030c', anchor_ix='1'))
            await self.highrise.chat("Reconnected...")

            while True:
                random_key = random.choice(list(self.emotes.keys()))
                random_emote = self.emotes[random_key]
                await self.highrise.send_emote(random_emote)
                await asyncio.sleep(10)

        except Exception as e:
            print(f"error : {e}")

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        try:
            print(f"{user.username} Joined Room.")
            wm = [
            'Where hearts connect!',
            'Take a seat, let love find you.',
            'Don\'t hesitate to say Hi and start a conversation.',
            'Embrace the magic of connection and let your journey begin!',
            'where souls intertwine!',
            'Find your special someone and break the ice with a friendly Hi.',
            'No need to be shy, love awaits you here.',
            'Enjoy the enchantment!',
            'Where sparks fly!',
            'Take a seat, open your heart, and don\'t be afraid to say Hi.',
            'Love is in the air, and this is where your story begins.',
            'A sanctuary for lovebirds!',
            'Find your perfect match, make eye contact, and say Hi to create a magical connection.',
            'Let love guide you on this extraordinary journey.',
            'Where love stories unfold!',
            'Take a seat, let destiny lead the way.',
            'Don\'t hold back, say Hi, and let the magic of love embrace you in this enchanting space.',
            'Where love finds its voice!',
            'Settle in, seize the moment, and greet someone with a warm Hi.',
            'Embrace the possibilities and let love weave its beautiful tapestry.'
            ]
            rwm = random.choice(wm)
            await self.highrise.send_whisper(user.id, f'Hey @{user.username}\nWelcome to the 🎀💙FIND A CUTIE💙🎀\n{rwm}\n\nJust say "help" for guide\n~ Code by @OGToxic')
            await self.highrise.send_whisper(user.id, f'\nTry new emotes "sleighride", "Timejump" and "Jingle"')
            await self.highrise.react("heart", user.id)
            face = ["FrontRight","FrontLeft"]
            fp = random.choice(face)
            _ = [Position(0.5, 1.25, 29.5, fp),Position(10.5, 1.25, 22.5, fp),Position(6.5, 1.0, 19.5, fp),Position(7.5, 1.25, 11.5, fp),Position(14.5, 7.25, 3.5, fp),Position(14.5, 7.0, 17.5, fp),Position(0.5, 7.0, 3.5, fp),Position(14.5, 7.0, 28.5, fp),Position(1.5, 14.5, 3.5, fp),Position(14.5, 14.5, 3.5, fp),Position(14.5, 14.5, 16.5, fp),Position(14.5, 14.5, 28.5, fp),]
            __ = random.choice(_)
            #await self.highrise.teleport(user.id, __)
        except Exception as e:
            print(f"error : {e}")

    async def on_whisper(self, user: User, message: str) -> None:
        try:
            _bid = "641b12cd8da19079b7cc34d1"
            _uri = "644c84fc64d782bbf8721bc5"
            _id = f"1_on_1:{_bid}:{_uri}"
            _idx = f"1_on_1:{_uri}:{_bid}"
            try:
                await self.highrise.send_message(_id, f'\n~ @{user.username} Whispered "{message}"', "text")
            except:
                await self.highrise.send_message(_idx, f'\n~ @{user.username} Whispered "{message}"', "text")
            #print(f"{user.username} whispered: {message}")
        except Exception as e:
            print(f"error in whisper : {e}")

    async def on_chat(self, user: User, message: str):
        try:
            _bid = "641b12cd8da19079b7cc34d1"
            _id = f"1_on_1:{_bid}:{user.id}"
            _idx = f"1_on_1:{user.id}:{_bid}"
            _rid = "64243855bf25fe0e8301bef6"
            input_emote = message.strip().lower()

            if input_emote.startswith("loop"):
                # Extract the emote name from the message
                loop_emote_name = input_emote[4:].strip()

                # Start a new loop with the specified emote
                await self.continuous_emote_handler.start_continuous_emote(self.highrise, loop_emote_name, user.id)
            elif input_emote.lower() == "stop":
                # Stop the continuous emote for the user
                await self.continuous_emote_handler.stop_continuous_emote(user.id)

            if message.lower().lstrip() == "help":
                await self.highrise.send_whisper(user.id, f"\n-loop emotename\n• Example :\n  loop enthused\n  stop ( to stop loop)\n\nemotename\nemotename @username\n• Example:\n  enthused\n  enthused @findlove")
                
            if message.lower().strip().startswith(("!")):
                if user.username.lower() in self._mods:
                    pass
                else:
                    await self.highrise.send_whisper(user.id, f"\nHey @{user.username}, You're not allowed to use commands that starts with !")
                    return
                await self.mod_handler(user, message)
            
            _message = message.lower().strip()
            command_split = _message.split()
            emote_detect = command_split[0]
            
            if emote_detect in self.emotes and len(command_split) == 1:
                await self.highrise.send_emote(self.emotes[emote_detect], user.id)
                return
            elif emote_detect in self.emotes and len(command_split) > 1 and not command_split[1].startswith("@"):
                await self.highrise.send_whisper(user.id, "Invalid user format. Please use '@username'.")
                return

            elif emote_detect in self.emotes and len(command_split) == 2:
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]
                user_id = next((u.id for u in users if u.username.lower() == command_split[1][1:].lower()), None)
                if not user_id:
                    await self.highrise.send_whisper(user.id, f"User @{command_split[1][1:]} not found")
                    return
                try:
                    await self.highrise.send_emote(self.emotes[emote_detect], user.id)
                    await self.highrise.send_emote(self.emotes[emote_detect], user_id)
                except Exception as e:
                    print(f"An exception occurred [in user 2 user emote]: {e}")
                return

            elif emote_detect in self.emotes and len(command_split) > 2:
                await self.highrise.send_whisper(user.id, '\nusage : "emotename" or "emotename @username"')
                return

            #elif emote_detect not in self.emotes:
               #await self.highrise.chat("\nEmote Not Found")

            #if message.lower().strip().startswith(("-")):
                #await self.public_handler(user, message)

        except Exception as e:
            print(f"error : {e}")

    async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
        try:
            response = await self.highrise.get_messages(conversation_id)
            if isinstance(response, GetMessagesRequest.GetMessagesResponse):
                message = response.messages[0].content
            print (message)

            #if message.lower().lstrip() == "-rf" and user_id in self._mods:
                #await self.highrise.send_message(conversation_id, "Restarting")
                #await self.restart_program()
        except Exception as e:
                print(f"Error in messages : {e}")
            
    async def mod_handler(self, user: User, message: str):
        parts = message.split(" ")
        command = parts[0][1:]
        functions_folder = "handlers/mods"
        # Check if the function exists in the module
        for file_name in os.listdir(functions_folder):
            if file_name.endswith(".py"):
                module_name = file_name[:-3]  # Remove the '.py' extension
                module_path = os.path.join(functions_folder, file_name)
                
                # Load the module
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if the function exists in the module
                if hasattr(module, command) and callable(getattr(module, command)):
                    function = getattr(module, command)
                    await function(self, user, message)
        return

    async def public_handler(self, user: User, message: str):
        parts = message.split(" ")
        command = parts[0][1:]
        functions_folder = "handlers/public"
        # Check if the function exists in the module
        for file_name in os.listdir(functions_folder):
            if file_name.endswith(".py"):
                module_name = file_name[:-3]  # Remove the '.py' extension
                module_path = os.path.join(functions_folder, file_name)
                
                # Load the module
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Check if the function exists in the module
                if hasattr(module, command) and callable(getattr(module, command)):
                    function = getattr(module, command)
                    await function(self, user, message)
        return

    async def run(self, room_id, token):
        definitions = [BotDefinition(self, room_id, token)]
        await __main__.main(definitions)

#keep_alive()
if __name__ == "__main__":
    room_id = "62339ee15dcb95aa3f9e1080"
    token = "a4b79ec109709b52a0e6390c8eb8907eb85ccc3967b7ab1a1ffced51a6d800ef"
    arun(Bot().run(room_id, token))

                          
