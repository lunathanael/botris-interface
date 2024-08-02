import json
from websockets import WebSocketServerProtocol
from .models import Command, GameState, PlayerData, PlayerInfo, RoomData
from typing import Callable, Awaitable

def construct_message_handler(analyze_function: Callable[[GameState, list[PlayerData]], Awaitable[list[Command]]], verbose: bool=False) -> Callable[[str, WebSocketServerProtocol], Awaitable[None]]:
    async def handle_message(message: str, websocket: WebSocketServerProtocol):
        data = json.loads(message)
        message_type = data.get("type")
        if message_type != 'request_move':
            return
        match message_type:
            case "request_move":
                game_state = GameState(**data["payload"]["gameState"])
                players = [] #[PlayerData(**p) for p in data["payload"]["players"]]
                commands = await analyze_function(game_state, players)
                await send_action(websocket, commands)
            case "room_data":
                room_data = RoomData(**data["payload"]["roomData"])
                if verbose:
                    print("Room Data:", room_data)
            case "player_joined":
                player_data = PlayerData(**data["payload"]["playerData"])
                if verbose:
                    print("Player Joined:", player_data)
            case "player_left":
                session_id = data["payload"]["sessionId"]
                if verbose:
                    print("Player Left:", session_id)
            case "player_banned":
                player_info = PlayerInfo(**data["payload"]["playerInfo"])
                if verbose:
                    print("Player Banned:", player_info)
            case "player_unbanned":
                player_info = PlayerInfo(**data["payload"]["playerInfo"])
                if verbose:
                    print("Player Unbanned:", player_info)
            case "settings_changed":
                room_data = RoomData(**data["payload"]["roomData"])
                if verbose:
                    print("Settings Changed:", room_data)
            case "host_changed":
                host_info = PlayerInfo(**data["payload"]["hostInfo"])
                if verbose:
                    print("Host Changed:", host_info)
            case "game_started":
                if verbose:
                    print("Game Started")
            case "round_started":
                starts_at = data["payload"]["startsAt"]
                room_data = RoomData(**data["payload"]["roomData"])
                if verbose:
                    print("Round Started:", starts_at, room_data)
            case "player_action":
                session_id = data["payload"]["sessionId"]
                commands = data["payload"]["commands"]
                game_state = GameState(**data["payload"]["gameState"])
                events = data["payload"]["events"]
                if verbose:
                    print("Player Action:", session_id, commands, game_state, events)
            case "player_damage_received":
                session_id = data["payload"]["sessionId"]
                damage = data["payload"]["damage"]
                game_state = GameState(**data["payload"]["gameState"])
                if verbose:
                    print("Player Damage Received:", session_id, damage, game_state)
            case "round_over":
                winner_id = data["payload"]["winnerId"]
                winner_info = PlayerInfo(**data["payload"]["winnerInfo"])
                room_data = RoomData(**data["payload"]["roomData"])
                if verbose:
                    print("Round Over:", winner_id, winner_info, room_data)
            case "game_over":
                winner_id = data["payload"]["winnerId"]
                winner_info = PlayerInfo(**data["payload"]["winnerInfo"])
                room_data = RoomData(**data["payload"]["roomData"])
                if verbose:
                    print("Game Over:", winner_id, winner_info, room_data)
            case "game_reset":
                room_data = RoomData(**data["payload"]["roomData"])
                if verbose:
                    print("Game Reset:", room_data)
    return handle_message

async def send_action(websocket, commands):
    action_message = {
        "type": "action",
        "payload": {
            "commands": commands
        }
    }
    await websocket.send(json.dumps(action_message))
