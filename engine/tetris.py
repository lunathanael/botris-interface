from __future__ import annotations

from collections import deque
from typing import (TYPE_CHECKING, Any, Deque, Dict, List, Literal, Optional,
                    TypedDict)

import colorama
from colorama import Back, Fore, Style

from interface.models import GameState

from .models import (Board, ClearEvent, Command, DamageTankedEvent, Event,
                     GameOverEvent, Options, Piece, PieceData,
                     PiecePlacedEvent, ScoreData, ScoreInfo, Statistics)
from .pieces import I_WALLKICKS, WALLKICKS, generate_bag, get_piece_matrix
from .utils import (add_garbage, calculate_score, check_collision, _check_collision,
                    check_immobile, check_pc, clear_lines, generate_garbage,
                    get_board_avg_height, get_board_bumpiness,
                    get_board_heights, place_piece, create_piece, move_left, move_right, move_drop, sonic_left, sonic_right, sonic_drop, rotate_cw, rotate_ccw)
from .move_generator import generate_moves


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
        # convert 'I' to Piece.I, and etc for queue
        self.queue = deque([Piece.from_str(piece) for piece in game_state.queue])
        self.garbage_queue = generate_garbage(game_state.garbageQueued, self.options.garbage_messiness, self.options.board_width)
        self.held = Piece.from_str(game_state.held) if game_state.held else None
        self.current = PieceData(
            piece=Piece.from_str(game_state.current.piece),
            x=game_state.current.x,
            y=game_state.current.y,
            rotation=game_state.current.rotation
        )

        self.is_immobile = False
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

    def spawn_piece(self) -> PieceData:
        piece = self.queue.popleft()
        if len(self.queue) < 6:
            self.queue.extend(generate_bag())
        return create_piece(piece, self.options.board_height, self.options.board_width)

    def get_public_state(self) -> GameState:
        return GameState(
            board=self.board,
            queue=[piece.value for piece in list(self.queue)][:6],
            garbageQueued=len(self.garbage_queue),
            held=self.held.value if self.held else None,
            current=self.current.__dict__(),
            canHold=self.can_hold,
            combo=self.combo,
            b2b=self.b2b,
            score=self.score,
            piecesPlaced=self.pieces_placed,
            dead=self.dead,
        )

    def execute_commands(self, commands: List[Command]) -> List[Event]:
        """
        Execute List of commands until harddrop
        """
        events: List[Event] = []

        commands.append('hard_drop')
        for command in commands:
            if self.dead:
                break
            new_events = self.execute_command(command)
            events.extend(new_events)
            if command in ['hard_drop', 'hard_down']:
                break
        return

    def execute_command(self, command: Command) -> List[Event]:
        if self.dead:
            raise ValueError("Cannot act when dead")

        events: List[Event] = []

        match command:
            case 'move_left':
                test_piece: Optional[PieceData] = move_left(self.board, self.current, self.options.board_width)
                if test_piece is not None:
                    self.current = test_piece
            case 'move_right':
                test_piece: Optional[PieceData] = move_right(self.board, self.current, self.options.board_width)
                if test_piece is not None:
                    self.current = test_piece
            case 'drop':
                test_piece: Optional[PieceData] = move_drop(self.board, self.current, self.options.board_width)
                if test_piece is not None:
                    self.current = test_piece
            case 'sonic_left':
                test_piece: PieceData = sonic_left(self.board, self.current, self.options.board_width)
                self.current = test_piece
            case 'sonic_right':
                test_piece: PieceData = sonic_right(self.board, self.current, self.options.board_width)
                self.current = test_piece
            case 'sonic_drop':
                test_piece: PieceData = sonic_drop(self.board, self.current, self.options.board_width)
                self.current = test_piece
            case 'rotate_cw':
                test_piece: Optional[PieceData] = rotate_cw(self.board, self.current, self.options.board_width)
                if test_piece is not None:
                    self.current = test_piece
                    self.is_immobile = check_immobile(self.board, self.current, self.options.board_width)
            case 'rotate_ccw':
                test_piece: Optional[PieceData] = rotate_ccw(self.board, self.current, self.options.board_width)
                if test_piece is not None:
                    self.current = test_piece
                    self.is_immobile = check_immobile(self.board, self.current, self.options.board_width)
            case 'hold':
                if not self.can_hold:
                    return events

                new_held = self.current.piece
                if self.held:
                    self.queue.appendleft(self.held)
                    self.held = self.current.piece
                self.current = self.spawn_piece()
                
                self.held = new_held
                self.can_hold = False
                self.is_immobile = check_immobile(self.board, self.current, self.options.board_width)
                
                if _check_collision(self.board, self.current.piece, self.current.x, self.current.y, self.current.rotation, self.options.board_width):
                    self.dead = True
                    events.append(GameOverEvent())
            case 'hard_drop':
                initial_piece_state: PieceData = self.current.copy()
                
                self.current: PieceData = sonic_drop(self.board, self.current, self.options.board_width)

                final_piece_state: PieceData = self.current.copy()

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
            case _:
                raise ValueError(f"Invalid command: {command}")

        return events

    def queue_garbage(self, hole_indices: List[int]) -> None:
        self.garbage_queue.extend(hole_indices)

    def __str__(self) -> str:
        representation: str = ''
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

    def render_board(self, render_current: bool=True) -> None:
        if render_current:
            t_board = place_piece(self.board, self.current, self.options.board_width)
        else:
            t_board = self.board
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
        for i, piece in enumerate(list(self.queue)[:6]):
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
                if y < len(t_board) and t_board[y][x] is not None:
                    piece = t_board[y][x]
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

    def generate_moves(self, include_held: bool=True, include_queue: bool=True) -> Dict[PieceData, List[Command]]:
        held: Optional[Piece] = self.held if include_held else None
        first_piece: Optional[Piece] = self.queue[0] if include_queue else None
        alternative: Optional[Piece] = first_place if held is None else held
        return generate_moves(self.board, self.current.piece, alternative, self.options.board_height, self.options.board_width)