from __future__ import annotations

from typing import List, Tuple, Dict, Any
from piece import Piece, PieceData
from utils import generate_bag, spawn_piece, check_collision, check_pc, calculate_score, clear_lines, add_garbage, try_wall_kicks, place_piece

class Block:
    def __init__(self, piece_type: str = None):
        self.piece_type = piece_type


class GameState:
    def __init__(self):
        self.board: List[List[Block]] = []
        self.queue: List[Piece] = []
        self.garbage_queue: List[int] = []
        self.held: Piece = None
        self.current: PieceData = None
        self.is_immobile: bool = False
        self.can_hold: bool = True
        self.combo: int = 0
        self.b2b: bool = False
        self.score: int = 0
        self.pieces_placed: int = 0
        self.dead: bool = False

    @classmethod
    def create_game_state(cls, options: Dict[str, Any], initial_bag: List[Piece] = None) -> GameState:
        game_state = cls()
        game_state.queue = initial_bag or generate_bag()
        if len(game_state.queue) < 6:
            game_state.queue.extend(generate_bag())
        game_state.current, _ = spawn_piece(game_state.board, game_state.queue.pop(0), options)
        return game_state

    def get_public_game_state(self) -> Dict[str, Any]:
        return {
            "board": self.board,
            "queue": self.queue[:6],
            "garbage_queued": len(self.garbage_queue),
            "held": self.held,
            "current": self.current,
            "is_immobile": self.is_immobile,
            "can_hold": self.can_hold,
            "combo": self.combo,
            "b2b": self.b2b,
            "score": self.score,
            "pieces_placed": self.pieces_placed,
            "dead": self.dead,
        }

    def execute_command(self, command: Command, options: Dict[str, Any]) -> Tuple[GameState, List[GameEvent]]:
        new_game_state = GameState()
        new_game_state.__dict__.update(self.__dict__)
        events = []

        if command == Command.MOVE_LEFT:
            new_game_state.current.x -= 1
            if check_collision(new_game_state.board, new_game_state.current, options):
                new_game_state.current.x += 1
        elif command == Command.MOVE_RIGHT:
            new_game_state.current.x += 1
            if check_collision(new_game_state.board, new_game_state.current, options):
                new_game_state.current.x -= 1
        elif command == Command.SONIC_LEFT:
            while not check_collision(new_game_state.board, new_game_state.current, options):
                new_game_state.current.x -= 1
            new_game_state.current.x += 1
        elif command == Command.SONIC_RIGHT:
            while not check_collision(new_game_state.board, new_game_state.current, options):
                new_game_state.current.x += 1
            new_game_state.current.x -= 1
        elif command == Command.DROP:
            new_game_state.current.y -= 1
            if check_collision(new_game_state.board, new_game_state.current, options):
                new_game_state.current.y += 1
        elif command == Command.SONIC_DROP:
            while not check_collision(new_game_state.board, new_game_state.current, options):
                new_game_state.current.y -= 1
            new_game_state.current.y += 1
        elif command == Command.HARD_DROP:
            initial_piece_state = new_game_state.current
            while not check_collision(new_game_state.board, new_game_state.current, options):
                new_game_state.current.y -= 1
            new_game_state.current.y += 1
            final_piece_state = new_game_state.current

            new_game_state.board = place_piece(new_game_state.board, new_game_state.current, options)
            new_game_state.board, cleared_lines = clear_lines(new_game_state.board)

            pc = check_pc(new_game_state.board)
            score_data = calculate_score({
                'pc': pc,
                'lines_cleared': len(cleared_lines),
                'is_immobile': new_game_state.is_immobile,
                'b2b': new_game_state.b2b,
                'combo': new_game_state.combo,
            }, options)

            new_game_state.combo = score_data['combo']
            new_game_state.b2b = score_data['b2b']
            new_game_state.score += score_data['score']
            new_game_state.pieces_placed += 1

            attack = score_data['score']
            cancelled = 0
            while new_game_state.garbage_queue and attack > 0:
                new_game_state.garbage_queue.pop(0)
                attack -= 1
                cancelled += 1

            tanked_lines = []
            if not cleared_lines:
                garbage_indices = new_game_state.garbage_queue[:attack]
                new_game_state.board = add_garbage(new_game_state.board, garbage_indices, options)
                tanked_lines.extend(garbage_indices)
                new_game_state.garbage_queue = new_game_state.garbage_queue[attack:]

            new_piece, is_dead = spawn_piece(new_game_state.board, new_game_state.queue.pop(0), options)
            new_game_state.dead = is_dead
            new_game_state.current = new_piece
            new_game_state.can_hold = True

            if len(new_game_state.queue) < 6:
                new_game_state.queue.extend(generate_bag())

            events.append(GameEvent("piece_placed", {
                "initial": initial_piece_state,
                "final": final_piece_state
            }))

            if score_data['clear_name']:
                events.append(GameEvent("clear", {
                    "clear_name": score_data['clear_name'],
                    "all_spin": score_data['all_spin'],
                    "b2b": score_data['b2b'],
                    "combo": score_data['combo'],
                    "pc": pc,
                    "attack": attack,
                    "cancelled": cancelled,
                    "piece": final_piece_state,
                    "cleared_lines": cleared_lines
                }))

            if tanked_lines:
                events.append(GameEvent("damage_tanked", {
                    "hole_indices": tanked_lines
                }))

            if new_game_state.dead:
                events.append(GameEvent("game_over", {}))

        elif command in [Command.ROTATE_CW, Command.ROTATE_CCW]:
            initial_rotation = new_game_state.current.rotation
            new_rotation = (initial_rotation + (1 if command == Command.ROTATE_CW else 3)) % 4
            new_piece_data, success = try_wall_kicks(new_game_state.board, new_game_state.current, new_rotation, options)
            if success:
                new_game_state.current = new_piece_data
                new_game_state.is_immobile = all(
                    check_collision(new_game_state.board, PieceData(new_game_state.current.piece, new_game_state.current.x + dx, new_game_state.current.y + dy, new_game_state.current.rotation), options)
                    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                )
        elif command == Command.HOLD:
            if new_game_state.can_hold:
                new_held = new_game_state.current.piece
                if new_game_state.held:
                    new_piece, is_dead = spawn_piece(new_game_state.board, new_game_state.held, options)
                else:
                    new_piece, is_dead = spawn_piece(new_game_state.board, new_game_state.queue.pop(0), options)
                    if len(new_game_state.queue) < 6:
                        new_game_state.queue.extend(generate_bag())

                new_game_state.dead = is_dead
                new_game_state.current = new_piece
                new_game_state.held = new_held
                new_game_state.can_hold = False
                new_game_state.is_immobile = all(
                    check_collision(new_game_state.board, PieceData(new_game_state.current.piece, new_game_state.current.x + dx, new_game_state.current.y + dy, new_game_state.current.rotation), options)
                    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                )

        return new_game_state, events

    def queue_garbage(self, hole_indices: List[int]) -> GameState:
        new_game_state = GameState()
        new_game_state.__dict__.update(self.__dict__)
        new_game_state.garbage_queue.extend(hole_indices)
        return new_game_state


def render_board(board: List[List[Block]]):
    rendered_board = [''.join(block.piece_type if block else ' ' for block in row) for row in reversed(board)]
    print('\n'.join(rendered_board))


class Command:
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    SONIC_LEFT = "sonic_left"
    SONIC_RIGHT = "sonic_right"
    DROP = "drop"
    SONIC_DROP = "sonic_drop"
    HARD_DROP = "hard_drop"
    ROTATE_CW = "rotate_cw"
    ROTATE_CCW = "rotate_ccw"
    HOLD = "hold"

class GameEvent:
    def __init__(self, event_type: str, payload: Dict[str, Any]):
        self.type = event_type
        self.payload = payload