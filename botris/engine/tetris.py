from __future__ import annotations

from collections import deque
from typing import Any, Deque, Dict, List, Literal, Optional

import colorama
from colorama import Back, Fore, Style

from botris.interface import Command, GameState

from .models import (Board, ClearEvent, DamageTankedEvent, Event,
                     GameOverEvent, GarbageLine, Move, Options, Piece,
                     PieceData, PiecePlacedEvent, ScoreData, ScoreInfo,
                     Statistics)
from .move_generator import generate_moves
from .pieces import generate_bag, get_piece_matrix
from .utils import (_check_collision, calculate_score, check_collision,
                    check_immobile, check_pc, clear_lines, create_piece,
                    generate_garbage, get_board_avg_height,
                    get_board_bumpiness, get_board_heights, move_drop,
                    move_left, move_right, place_piece, process_garbage,
                    rotate_ccw, rotate_cw, sonic_drop, sonic_left, sonic_right)


class TetrisGame:
    """
    A class to represent a Tetris game.

    Attributes:
    -----------
    options : Options
        Configuration options for the game.
    board : Board
        The current state of the game board.
    queue : Deque[Piece]
        The queue of upcoming pieces.
    garbage_queue : Deque[GarbageLine]
        The queue of incoming garbage lines.
    held : Optional[Piece]
        The currently held piece.
    current : PieceData
        The current active piece data.
    is_immobile : bool
        Flag indicating if the current piece is immobile.
    can_hold : bool
        Flag indicating if the player can hold a piece.
    combo : int
        The current combo count.
    b2b : bool
        Flag indicating if the player is in a back-to-back state.
    score : int
        The current score of the player.
    pieces_placed : int
        The number of pieces placed in the game.
    garbage_cleared : int
        The number of garbage lines cleared.
    dead : bool
        Flag indicating if the game is over.

    Methods:
    --------
    __init__(self, options: Optional[Dict[str, Any]]=None):
        Initializes the Tetris game with the given options.
    
    from_game_state(cls, game_state: GameState, options: Optional[Dict[str, Any]]=None) -> TetrisGame:
        Creates a Tetris game instance from a given game state.

    reset(self) -> None:
        Resets the state of the Tetris game.
    
    spawn_piece(self) -> PieceData:
        Spawns a new piece on the game board.

    get_public_state(self) -> GameState:
        Returns the public state of the game.

    execute_command(self, command: Command) -> List[Event]:
        Executes a command and returns a list of events.

    execute_commands(self, commands: List[Command]) -> List[Event]:
        Executes a list of commands and returns a list of events.

    execute_moves(self, moves: List[Move]) -> List[Event]:
        Executes a list of moves and returns a list of events.

    execute_move(self, move: Move) -> List[Event]:
        Executes the specified move and returns a list of events.

    queue_garbage(self, hole_indices: List[int]) -> None:
        Queue garbage lines to be sent to the player.

    queue_garbage_lines(self, garbage_lines: List[GarbageLine]) -> None:
        Queue the given garbage lines to be sent to the player.

    get_board_stats(self) -> Statistics:
        Calculates and returns the statistics of the game board.

    render_board(self, render_current: bool=True) -> None:
        Renders the game board and displays relevant information.

    generate_moves(self, include_held: bool=True, include_queue: bool=True, algo: Literal['bfs', 'dfs', 'dijk', 'dijk-short']='bfs') -> Dict[PieceData, List[Move]]:
        Generate a dictionary of possible moves.
    """

    def __init__(self, options: Optional[Dict[str, Any]]=None):
        """
        Initializes the Tetris game with the given options.

        Parameters:
        -----------
        options : Optional[Dict[str, Any]]
            Configuration options for the game.
        """
        self.options: Options = Options(**(options or {}))
        
        self.board: Board = None
        self.queue: Deque[Piece] = None
        self.garbage_queue: Deque[GarbageLine] = None
        self.held: Optional[Piece] = None
        self.current: PieceData = None
        self.is_immobile: bool = None
        self.can_hold: bool = None
        self.combo: int = None
        self.b2b: bool = None
        self.score: int = None
        self.pieces_placed: int = None
        self.garbage_cleared: int = None
        self.dead: bool = None

        self.reset()

    @classmethod
    def from_game_state(cls, game_state: GameState, options: Optional[Dict[str, Any]]=None) -> TetrisGame:
        """
        Creates a Tetris game instance from a given game state.

        Parameters:
        -----------
        game_state : GameState
            The public interface state of the game to initialize from.
        options : Optional[Dict[str, Any]]
            Configuration options for the game.

        Returns:
        --------
        TetrisGame
            A new instance of TetrisGame initialized with the given game state.
        """
        self: TetrisGame = cls(options)
        
        self.board = game_state.board
        self.queue = deque([Piece.from_str(piece) for piece in game_state.queue])
        self.garbage_queue = deque(generate_garbage(game_state.garbageQueued, self.options.garbage_messiness, self.options.board_width))
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
        self.garbage_cleared = game_state.garbageCleared
        self.dead = game_state.dead

        if len(self.queue) < 6:
            self.queue.extend(generate_bag())

        return self

    def reset(self) -> None:
        """
        Resets the state of the Tetris game.

        This method resets the board, queues, held piece, current piece, immobility status,
        hold availability, combo count, back-to-back status, score, pieces placed count,
        garbage cleared count, and death status.
        """
        self.board = []
        self.queue = deque(generate_bag())
        self.garbage_queue = deque([])
        self.held = None
        self.current = self.spawn_piece()
        self.is_immobile = False
        self.can_hold = True
        self.combo = 0
        self.b2b = False
        self.score = 0
        self.pieces_placed = 0
        self.garbage_cleared = 0
        self.dead = False

    def spawn_piece(self) -> PieceData:
        """
        Spawns a new piece on the game board.

        Returns:
        --------
        PieceData
            The newly spawned piece.
        """
        piece = self.queue.popleft()
        if len(self.queue) < 6:
            self.queue.extend(generate_bag())
        return create_piece(piece, self.options.board_height, self.options.board_width)

    def get_public_state(self) -> GameState:
        return GameState(
            board=self.board,
            queue=[piece.value for piece in list(self.queue)][:6],
            garbageQueued=[garbage.public() for garbage in list(self.garbage_queue)],
            held=self.held.value if self.held else None,
            current=self.current.public(),
            canHold=self.can_hold,
            combo=self.combo,
            b2b=self.b2b,
            score=self.score,
            piecesPlaced=self.pieces_placed,
            garbageCleared=self.garbage_cleared,
            dead=self.dead,
        )
    
    def execute_command(self, command: Command) -> List[Event]:
        """
        Executes a command and returns a list of events.

        Parameters:
        --------
        command : Command
            The command to execute.

        Returns:
        --------
        List[Event]
            A list of events generated by the command execution.
        """
        return self.execute_move(Move.from_command(command))
    
    def execute_commands(self, commands: List[Command]) -> List[Event]:
        """
        Executes a list of commands and returns a list of events.

        Parameters:
        --------
        commands : List[Command]
            A list of commands to execute.

        Returns:
        --------
        List[Event]
            A list of events generated by executing the commands.
        """
        moves: List[Move] = [Move.from_command(command) for command in commands]
        return self.execute_moves(moves)

    def execute_moves(self, moves: List[Move]) -> List[Event]:
        """
        Executes a list of moves and returns a list of events.

        Parameters:
        --------
        moves : List[Move]
            A list of moves to execute.

        Returns:
        --------
        List[Event]
            A list of events generated by executing the moves.
        """
        events: List[Event] = []

        moves.append(Move.hard_drop)
        for move in moves:
            if self.dead:
                break
            new_events = self.execute_move(move)
            events.extend(new_events)
            if move == Move.hard_drop:
                break
        return events

    def execute_move(self, move: Move) -> List[Event]:
        """
        Executes the specified move and returns a list of events that occurred during the move.

        Parameters:
        --------
        move : Move
            The move to execute.

        Returns:
        --------
        List[Event]
            A list of events that occurred during the move.

        Raises:
        --------
        ValueError
            If the move cannot be executed when the game is dead.
        """
        if self.dead:
            raise ValueError("Cannot act when dead")

        events: List[Event] = []

        match move:
            case Move.move_left:
                test_piece: Optional[PieceData] = move_left(self.board, self.current, self.options.board_width)
                if test_piece is not None:
                    self.current = test_piece
            case Move.move_right:
                test_piece: Optional[PieceData] = move_right(self.board, self.current, self.options.board_width)
                if test_piece is not None:
                    self.current = test_piece
            case Move.drop:
                test_piece: Optional[PieceData] = move_drop(self.board, self.current, self.options.board_width)
                if test_piece is not None:
                    self.current = test_piece
            case Move.sonic_left:
                test_piece: PieceData = sonic_left(self.board, self.current, self.options.board_width)
                self.current = test_piece
            case Move.sonic_right:
                test_piece: PieceData = sonic_right(self.board, self.current, self.options.board_width)
                self.current = test_piece
            case Move.sonic_drop:
                test_piece: PieceData = sonic_drop(self.board, self.current, self.options.board_width)
                self.current = test_piece
            case Move.rotate_cw:
                test_piece: Optional[PieceData] = rotate_cw(self.board, self.current, self.options.board_width)
                if test_piece is not None:
                    self.current = test_piece
                    self.is_immobile = check_immobile(self.board, self.current, self.options.board_width)
            case Move.rotate_ccw:
                test_piece: Optional[PieceData] = rotate_ccw(self.board, self.current, self.options.board_width)
                if test_piece is not None:
                    self.current = test_piece
                    self.is_immobile = check_immobile(self.board, self.current, self.options.board_width)
            case Move.hold:
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
            case Move.hard_drop:
                initial_piece_state: PieceData = self.current.copy()
                
                self.current: PieceData = sonic_drop(self.board, self.current, self.options.board_width)

                final_piece_state: PieceData = self.current.copy()

                self.board = place_piece(self.board, self.current, self.options.board_width)
                self.board, cleared_lines = clear_lines(self.board)
                cleared: int = len(cleared_lines)
                for line in cleared_lines:
                    if 'G' in line['blocks']:
                        self.garbage_cleared += 1


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
                for _ in range(cancelled):
                    self.garbage_queue.popleft()
                attack -= cancelled

                tanked_lines: List[int] = []
                if cleared == 0:
                    self.board, tanked_lines = process_garbage(self.board, self.garbage_queue, self.options.board_width)

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
                raise ValueError(f"Invalid move: {move}")

        return events

    def queue_garbage(self, hole_indices: List[int]) -> None:
        """
        Queue garbage lines to be sent to the player.

        Parameters:
        --------
        hole_indices : List[int]
            A list of indices representing the holes in the player's board.
        """
        self.garbage_queue.extend([GarbageLine(delay=self.options.garbage_delay, index=i) for i in hole_indices])

    def queue_garbage_lines(self, garbage_lines: List[GarbageLine]) -> None:
        """
        Queue the given garbage lines to be sent to the player.

        Parameters:
        --------
        garbage_lines : List[GarbageLine]
            A list of GarbageLine objects representing the lines to be sent.
        """
        self.garbage_queue.extend(garbage_lines)

    def __str__(self) -> str:
        """
        Returns a string representation of the Tetris board.

        Returns:
        --------
        str
            The string representation of the Tetris board.
        """
        representation: str = ''
        rendered_board = [['.' if cell is None else cell for cell in row] for row in self.board]
        rendered_board.reverse()
        for row in rendered_board:
            representation += ''.join(row) + '\n'
        return representation

    def get_board_stats(self) -> Statistics:
        """
        Calculates and returns the statistics of the game board.

        Returns:
        --------
        Statistics
            An instance of the Statistics class containing the calculated statistics.
        """
        return Statistics(
            heights=get_board_heights(self.board, self.options.board_width),
            bumpiness=get_board_bumpiness(self.board, self.options.board_width),
            avg_height=get_board_avg_height(self.board, self.options.board_width),
        )

    def render_board(self, render_current: bool=True) -> None:
        """
        Renders the game board and displays relevant information such as score, combo, and held piece.

        Parameters:
        --------
        render_current : bool
            Determines whether to render the current piece on the board, defaults to True.
        """
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

    def generate_moves(self, include_held: bool=True, include_queue: bool=True, algo: Literal['bfs', 'dfs', 'dijk', 'dijk-short']='bfs') -> Dict[PieceData, List[Move]]:
        """
        Generate a dictionary of possible moves.

        Parameters:
        --------
        include_held : bool
            Whether to include the held piece in the moves. Defaults to True.
        include_queue : bool
            Whether to include the first piece in the queue in the moves. Defaults to True.
        algo : Literal['bfs', 'dfs', 'dijk', 'dijk-short']
            The algorithm to use for generating moves. Defaults to 'bfs'.

        Returns:
        --------
        Dict[PieceData, List[Move]]
            A dictionary where the keys are PieceData objects representing each piece, and the values are lists of possible Move objects for each piece.
        """
        held: Optional[Piece] = self.held if include_held else None
        first_piece: Optional[Piece] = self.queue[0] if include_queue else None
        alternative: Optional[Piece] = first_piece if held is None else held
        return generate_moves(self.board, self.current.piece, alternative, self.options.board_height, self.options.board_width, algo)