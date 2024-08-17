import json
from typing import Awaitable, Callable, List, Tuple

from websockets import WebSocketServerProtocol

from .models import Command, GameState, PlayerData, PlayerInfo, RoomData


def construct_message_handler(
    analyze_function: Callable[[GameState, List[PlayerData]], Awaitable[List[Command]]],
    verbose: bool = False,
) -> Callable[[str, WebSocketServerProtocol], Awaitable[None]]:
    async def handle_message(message: str, websocket: WebSocketServerProtocol):
        data = json.loads(message)
        message_type = data.get("type")
        if message_type != "request_move":
            return
        match message_type:
            case "request_move":
                game_state = GameState(**data["payload"]["gameState"])
                players = []  # [PlayerData(**p) for p in data["payload"]["players"]]
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
    action_message = {"type": "action", "payload": {"commands": commands}}
    await websocket.send(json.dumps(action_message))


class GameBuffer:
    def __init__(self):
        self.num_games: int = 0
        self.total_frames: int = 0
        self.trajectory_buffer: List[List[Tuple[List[Command], GameState]]] = []

    def add_frame(self, game_state: GameState, commands: List[Command]):
        if self.num_games == 0:
            self.new_game()
        self.trajectory_buffer[-1].append((commands, game_state))
        self.total_frames += 1

    def new_game(self):
        self.num_games += 1
        self.trajectory_buffer.append([])


def tracker_construct_message_handler(
    analyze_function: Callable[[GameState, List[PlayerData]], Awaitable[List[Command]]],
    verbose: bool = False,
) -> Callable[[str, WebSocketServerProtocol], Awaitable[None]]:
    gb: GameBuffer = GameBuffer()

    async def handle_message(message: str, websocket: WebSocketServerProtocol):
        data = json.loads(message)
        message_type = data.get("type")
        if message_type != "request_move":
            if message_type == "round_over":
                gb.new_game()
                import pickle

                with open("test.game_buffer", "wb") as f:
                    pickle.dump(gb, f)
            return
        match message_type:
            case "request_move":
                game_state = GameState(**data["payload"]["gameState"])
                players = []  # [PlayerData(**p) for p in data["payload"]["players"]]
                commands = await analyze_function(game_state, players)
                gb.add_frame(game_state, commands)
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
