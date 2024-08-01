import json

from .models import Command, GameState, PlayerData, PlayerInfo, RoomData
from .utils import process_game_state


async def handle_message(message, websocket, verbose=False):
    data = json.loads(message)
    message_type = data.get("type")
    
    if message_type == "room_data":
        room_data = RoomData(**data["payload"]["roomData"])
        if verbose:
            print("Room Data:", room_data)
    elif message_type == "player_joined":
        player_data = PlayerData(**data["payload"]["playerData"])
        if verbose:
            print("Player Joined:", player_data)
    elif message_type == "player_left":
        session_id = data["payload"]["sessionId"]
        if verbose:
            print("Player Left:", session_id)
    elif message_type == "player_banned":
        player_info = PlayerInfo(**data["payload"]["playerInfo"])
        if verbose:
            print("Player Banned:", player_info)
    elif message_type == "player_unbanned":
        player_info = PlayerInfo(**data["payload"]["playerInfo"])
        if verbose:
            print("Player Unbanned:", player_info)
    elif message_type == "settings_changed":
        room_data = RoomData(**data["payload"]["roomData"])
        if verbose:
            print("Settings Changed:", room_data)
    elif message_type == "host_changed":
        host_info = PlayerInfo(**data["payload"]["hostInfo"])
        if verbose:
            print("Host Changed:", host_info)
    elif message_type == "game_started":
        if verbose:
            print("Game Started")
    elif message_type == "round_started":
        starts_at = data["payload"]["startsAt"]
        room_data = RoomData(**data["payload"]["roomData"])
        if verbose:
            print("Round Started:", starts_at, room_data)
    elif message_type == "request_move":
        game_state = GameState(**data["payload"]["gameState"])
        players = [PlayerData(**p) for p in data["payload"]["players"]]
        commands = process_game_state(game_state, players)
        await send_action(websocket, commands)
    elif message_type == "player_action":
        session_id = data["payload"]["sessionId"]
        commands = data["payload"]["commands"]
        game_state = GameState(**data["payload"]["gameState"])
        events = data["payload"]["events"]
        if verbose:
         print("Player Action:", session_id, commands, game_state, events)
    elif message_type == "player_damage_received":
        session_id = data["payload"]["sessionId"]
        damage = data["payload"]["damage"]
        game_state = GameState(**data["payload"]["gameState"])
        if verbose:
            print("Player Damage Received:", session_id, damage, game_state)
    elif message_type == "round_over":
        winner_id = data["payload"]["winnerId"]
        winner_info = PlayerInfo(**data["payload"]["winnerInfo"])
        room_data = RoomData(**data["payload"]["roomData"])
        if verbose:
            print("Round Over:", winner_id, winner_info, room_data)
    elif message_type == "game_over":
        winner_id = data["payload"]["winnerId"]
        winner_info = PlayerInfo(**data["payload"]["winnerInfo"])
        room_data = RoomData(**data["payload"]["roomData"])
        if verbose:
            print("Game Over:", winner_id, winner_info, room_data)
    elif message_type == "game_reset":
        room_data = RoomData(**data["payload"]["roomData"])
        if verbose:
            print("Game Reset:", room_data)

async def send_action(websocket, commands):
    action_message = {
        "type": "action",
        "payload": {
            "commands": commands
        }
    }
    await websocket.send(json.dumps(action_message))
