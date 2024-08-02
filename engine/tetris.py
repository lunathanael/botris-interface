from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, List, Optional, Deque, Dict, Any
from collections import deque

import colorama
from colorama import Back, Fore, Style
from .models import PieceData, Options, Piece, Command, Board, Event, ClearEvent, GameOverEvent, PiecePlacedEvent, DamageTankedEvent, Statistics, ScoreInfo, ScoreData
from .pieces import generate_bag, get_piece_matrix, WALLKICKS, I_WALLKICKS

from .utils import (add_garbage, calculate_score, check_collision,
                    check_immobile, check_pc, clear_lines, generate_garbage,
                    get_board_avg_height, get_board_bumpiness,
                    get_board_heights, place_piece)

if TYPE_CHECKING:
    from interface.models import GameState

class PublicGameState(TypedDict):
    board: Board
    queue: List[Piece]
    garbageQueued: int
    held: Optional[Piece]
    current: PieceData
    isImmobile: bool
    canHold: bool
    combo: int
    b2b: bool
    score: int
    piecesPlaced: int
    dead: bool


    
class TetrisGame:
    def __init__(self, options: Optional[Dict[str, Any]]=None):
        self.options: Options = Options(**(options or {}))
        
        self.board: Board = None
        self.queue: Deque[Piece] = None
        self.garbage_queue: List[int] = None
        self.held: Optional[Piece] = None
        self.current: PieceData = None
        self.is_immobile: bool = None
        self.can_hold: bool = None
        self.combo: int = None
        self.b2b: bool = None
        self.score: int = None
        self.pieces_placed: int = None
        self.dead: bool = None

        self.reset()

    @classmethod
    def from_game_state(cls, game_state: GameState, options: Optional[Dict[str, Any]]=None) -> TetrisGame:
        self = cls(options)
        
        self.board = game_state.board
        self.queue = deque(game_state.queue)
        self.garbage_queue = generate_garbage(game_state.garbageQueued, self.options.garbage_messiness, self.options.board_width)
        self.held = game_state.held
        self.current = PieceData(
            piece=game_state.current.piece,
            x=game_state.current.x,
            y=game_state.current.y,
            rotation=game_state.current.rotation
        )

        self.is_immobile = game_state.isImmobile
        self.can_hold = game_state.canHold
        self.combo = game_state.combo
        self.b2b = game_state.b2b
        self.score = game_state.score
        self.pieces_placed = game_state.piecesPlaced
        self.dead = game_state.dead

        if len(self.queue) < 6:
            self.queue.extend(generate_bag())

        return self

    def reset(self) -> None:
        self.board = []
        self.queue = deque(generate_bag())
        self.garbage_queue = []
        self.held = None
        self.current = self.spawn_piece()
        self.is_immobile = False
        self.can_hold = True
        self.combo = 0
        self.b2b = False
        self.score = 0
        self.pieces_placed = 0
        self.dead = False

    def _spawn_piece(self, piece: Piece) -> PieceData:
        x: int = self.options.board_width // 2 - ((len(get_piece_matrix(piece, 0)[0]) + 1) // 2)
        y: int = self.options.board_height
        return PieceData(piece=piece, x=x, y=y, rotation=0)

    def spawn_piece(self) -> PieceData:
        piece = self.queue.popleft()
        if len(self.queue) < 6:
            self.queue.extend(generate_bag())
        return self._spawn_piece(piece)

    def get_public_state(self) -> GameState:
        return PublicGameState(
            board=self.board,
            queue=list(self.queue)[:6],
            garbageQueued=len(self.garbage_queue),
            held=self.held,
            current=self.current,
            isImmobile=self.is_immobile,
            canHold=self.can_hold,
            combo=self.combo,
            b2b=self.b2b,
            score=self.score,
            piecesPlaced=self.pieces_placed,
            dead=self.dead,
        )

    def execute_command(self, command: Command) -> List[Event]:
        if self.dead:
            raise ValueError("Cannot act when dead")

        events: List[Event] = []

        match command:
            case 'move_left':
                self.current.x -= 1
                if check_collision(self.board, self.current, self.options.board_width):
                    self.current.x += 1
            case 'move_right':
                self.current.x += 1
                if check_collision(self.board, self.current, self.options.board_width):
                    self.current.x -= 1
            case 'sonic_left':
                while not check_collision(self.board, self.current, self.options.board_width):
                    self.current.x -= 1
                self.current.x += 1
            case 'sonic_right':
                while not check_collision(self.board, self.current, self.options.board_width):
                    self.current.x += 1
                self.current.x -= 1
            case 'drop':
                self.current.y -= 1
                if check_collision(self.board, self.current, self.options.board_width):
                    self.current.y += 1
            case 'sonic_drop':
                while not check_collision(self.board, self.current, self.options.board_width):
                    self.current.y -= 1
                self.current.y += 1
            case 'hard_drop':
                initial_piece_state = self.current.copy()
                while not check_collision(self.board, self.current, self.options.board_width):
                    self.current.y -= 1
                self.current.y += 1
                final_piece_state = self.current.copy()

                self.board = place_piece(self.board, self.current, self.options.board_width)
                self.board, cleared_lines = clear_lines(self.board)
                pc = check_pc(self.board)

                score_info = ScoreInfo(
                    pc=pc,
                    lines_cleared=len(cleared_lines),
                    is_immobile=self.is_immobile,
                    b2b=self.b2b,
                    combo=self.combo,
                )

                score_data: ScoreData = calculate_score(score_info, self.options.attack_table, self.options.combo_table)

                self.combo = score_data.combo
                self.b2b = score_data.b2b

                self.score += score_data.score
                self.pieces_placed += 1

                attack = score_data.score
                cancelled: int = min(len(self.garbage_queue), attack)
                self.garbage_queue = self.garbage_queue[cancelled:]
                attack -= cancelled

                tanked_lines: List[int] = []
                if not cleared_lines:
                    hole_indices: List[int] = self.garbage_queue
                    self.board = add_garbage(self.board, hole_indices, self.options.board_width)
                    tanked_lines = hole_indices
                    self.garbage_queue = []

                events.append(PiecePlacedEvent(initial=initial_piece_state, final=final_piece_state))

                if score_data.clear_name:
                    events.append(ClearEvent(
                        clearName=score_data.clear_name,
                        allSpin=score_data.all_spin,
                        b2b=score_data.b2b,
                        combo=score_data.combo,
                        pc=pc,
                        attack=attack,
                        cancelled=cancelled,
                        piece=final_piece_state,
                        clearedLines=cleared_lines,
                    ))

                if tanked_lines:
                    events.append(DamageTankedEvent(holeIndices=tanked_lines))

                self.current = self.spawn_piece()
                self.can_hold = True
                self.is_immobile = check_immobile(self.board, self.current, self.options.board_width)
                
                if check_collision(self.board, self.current, self.options.board_width):
                    self.dead = True
                    events.append(GameOverEvent())

            case 'rotate_cw' | 'rotate_ccw':
                initial_rotation = self.current.rotation
                new_rotation = (initial_rotation + (1 if command == 'rotate_cw' else 3)) % 4
                
                wallkicks = I_WALLKICKS if self.current.piece == 'I' else WALLKICKS
                kick_data = wallkicks[initial_rotation][new_rotation]
                
                for dx, dy in kick_data:
                    test_piece = self.current.copy()
                    test_piece.rotation = new_rotation
                    test_piece.x += dx
                    test_piece.y += dy
                    if not check_collision(self.board, test_piece, self.options.board_width):
                        self.current = test_piece
                        self.is_immobile = check_immobile(self.board, self.current, self.options.board_width)
                        break

            case 'hold':
                if not self.can_hold:
                    return events

                new_held = self.current.piece
                if self.held:
                    self.current = self.spawn_piece()
                    self.current.piece = self.held
                else:
                    self.current = self.spawn_piece()
                
                self.held = new_held
                self.can_hold = False
                self.is_immobile = check_immobile(self.board, self.current, self.options.board_width)
                
                if check_collision(self.board, self.current, self.options.board_width):
                    self.dead = True
                    events.append(GameOverEvent())

        return events

    def queue_garbage(self, hole_indices: List[int]) -> None:
        self.garbage_queue.extend(hole_indices)

    def __str__(self) -> str:
        representation = ''
        rendered_board = [['.' if cell is None else cell for cell in row] for row in self.board]
        rendered_board.reverse()
        for row in rendered_board:
            representation += ''.join(row) + '\n'
        return representation

    def get_board_stats(self) -> Statistics:
        return Statistics(
            heights=get_board_heights(self.board, self.options.board_width),
            bumpiness=get_board_bumpiness(self.board, self.options.board_width),
            avg_height=get_board_avg_height(self.board, self.options.board_width),
        )

    def render_board(self) -> None:
        t_board = self.board.copy()
        self.board = place_piece(self.board, self.current, self.options.board_width)
        colorama.init()
        color_map = {
            'I': Fore.CYAN,
            'O': Fore.YELLOW,
            'T': Fore.MAGENTA,
            'S': Fore.GREEN,
            'Z': Fore.RED,
            'J': Fore.BLUE,
            'L': Fore.WHITE,
            'G': Fore.BLACK + Back.WHITE
        }

        piece_info = []

        piece_info.append('Queue:')
        for i, piece in enumerate(self.queue[:6]):
            if i > 0:
                piece_info.append('')
            piece_matrix = get_piece_matrix(piece, 0)
            for row in piece_matrix[:-1]:
                piece_info.append('    ' + ''.join([f'{color_map[cell]}██{Style.RESET_ALL}' if cell else '  ' for cell in row]))

        piece_info = [piece for piece in reversed(piece_info)]

        print('┌' + '──' * self.options.board_width + '┐')

        for y in range(self.options.board_height - 1, -1, -1):
            print('│', end='')
            for x in range(self.options.board_width):
                if y < len(self.board) and self.board[y][x] is not None:
                    piece = self.board[y][x]
                    print(f'{color_map[piece]}██{Style.RESET_ALL}', end='')
                else:
                    print('  ', end='')
            print('│', end='')

            if len(piece_info):
                print(piece_info.pop())
            else:
                print()

        print('└' + '──' * self.options.board_width + '┘')
        print(f'  Score: {self.score}')
        print(f'  Combo: {self.combo}')
        print(f'  B2B: {"Yes" if self.b2b else "No"}')
        print(f'  Pieces: {self.pieces_placed}')
        print(f'  Hold: {self.held or "Empty"}')

        print(f'\nGarbage queued: {len(self.garbage_queue)}')
        self.board = t_board