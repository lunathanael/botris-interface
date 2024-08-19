from __future__ import annotations

from collections import deque
from typing import Any, Deque, Dict, List, Literal, Optional

import colorama
from colorama import Back, Fore, Style
from PIL import Image, ImageDraw, ImageFont

from botris.interface import Command, GameState, PublicGarbageLine

from .models import (
    Board,
    ClearEvent,
    DamageTankedEvent,
    Event,
    GameOverEvent,
    GarbageLine,
    Move,
    Options,
    Piece,
    PieceData,
    PiecePlacedEvent,
    ScoreData,
    ScoreInfo,
    Statistics,
)
from .move_generator import generate_moves
from .pieces import generate_bag, get_piece_matrix
from .utils import (
    _check_collision,
    _place_piece,
    calculate_score,
    check_immobile,
    check_pc,
    clear_lines,
    create_piece,
    generate_garbage,
    get_board_avg_height,
    get_board_bumpiness,
    get_board_heights,
    move_drop,
    move_left,
    move_right,
    place_piece,
    process_garbage,
    rotate_ccw,
    rotate_cw,
    sonic_drop,
    sonic_left,
    sonic_right,
)


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

    dangerously_drop_piece(self, piece_data: PieceData) -> List[Event]:
        Drops a piece on the board without checking for collisions.

    queue_attack(self, attack: int) -> None:
        Queue an attack to be sent to the player.

    queue_garbage(self, hole_indices: List[int]) -> None:
        Queue garbage lines to be sent to the player.

    queue_garbage_lines(self, garbage_lines: List[GarbageLine]) -> None:
        Queue the given garbage lines to be sent to the player.

    get_board_stats(self) -> Statistics:
        Calculates and returns the statistics of the game board.

    render_board(self, render_current: bool=True) -> None:
        Renders the game board and displays relevant information.

    draw_board(self, render_current: bool=True) -> Image:
        Draws the game board and returns an image.

    generate_moves(self, include_held: bool=True, include_queue: bool=True, algo: Literal['bfs', 'dfs', 'dijk', 'dijk-short']='bfs') -> Dict[PieceData, List[Move]]:
        Generate a dictionary of possible moves.
    """

    def __init__(self, options: dict[str, Any] | None = None):
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
        self.held: Piece | None = None
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

    def copy(self) -> TetrisGame:
        """
        Creates a copy of the given Tetris game instance.

        Returns:
        --------
        TetrisGame
            A new instance of TetrisGame copied from the given instance.
        """
        tgs: TetrisGame = TetrisGame(self.options.dict())
        tgs.board = [row.copy() for row in self.board]
        tgs.queue = deque([piece for piece in list(self.queue)])
        tgs.garbage_queue = deque([garbage.copy() for garbage in self.garbage_queue])
        tgs.held = self.held
        tgs.current = self.current.copy()
        tgs.is_immobile = self.is_immobile
        tgs.can_hold = self.can_hold
        tgs.combo = self.combo
        tgs.b2b = self.b2b
        tgs.score = self.score
        tgs.pieces_placed = self.pieces_placed
        tgs.garbage_cleared = self.garbage_cleared
        tgs.dead = self.dead
        return tgs

    @classmethod
    def from_game_state(
        cls, game_state: GameState, options: dict[str, Any] | None = None
    ) -> TetrisGame:
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
        self.garbage_queue = deque(
            generate_garbage(
                game_state.garbageQueued,
                self.options.garbage_messiness,
                self.options.board_width,
            )
        )
        self.held = Piece.from_str(game_state.held) if game_state.held else None
        self.current = PieceData(
            piece=Piece.from_str(game_state.current.piece),
            x=game_state.current.x,
            y=game_state.current.y,
            rotation=game_state.current.rotation,
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
        self.current = self.next_piece()
        self.is_immobile = False
        self.can_hold = True
        self.combo = 0
        self.b2b = False
        self.score = 0
        self.pieces_placed = 0
        self.garbage_cleared = 0
        self.dead = False

    def place_piece(self, piece_data: PieceData) -> Board:
        """
        Places the given piece on the game board.

        Parameters:
        --------
        piece_data : PieceData
            The piece data to place on the game board.

        Returns:
        --------
        Board
            The updated game board with the piece placed.
        """
        _place_piece(self.board, piece_data, self.options.board_width)
        return self.board

    def next_piece(self) -> PieceData:
        """
        Returns the next piece from the queue.

        Returns:
        --------
        PieceData
            The newly spawned piece.
        """
        piece: Piece = self.queue.popleft()
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

    def execute_command(self, command: Command) -> list[Event]:
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

    def execute_commands(self, commands: list[Command]) -> list[Event]:
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
        moves: list[Move] = [Move.from_command(command) for command in commands]
        return self.execute_moves(moves)

    def execute_moves(self, moves: list[Move]) -> list[Event]:
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
        events: list[Event] = []

        moves.append(Move.hard_drop)
        for move in moves:
            if self.dead:
                break
            new_events = self.execute_move(move)
            events.extend(new_events)
            if move == Move.hard_drop:
                break
        return events

    def execute_move(self, move: Move) -> list[Event]:
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

        events: list[Event] = []

        match move:
            case Move.move_left:
                test_piece: PieceData | None = move_left(
                    self.board, self.current, self.options.board_width
                )
                if test_piece is not None:
                    self.current = test_piece
            case Move.move_right:
                test_piece: PieceData | None = move_right(
                    self.board, self.current, self.options.board_width
                )
                if test_piece is not None:
                    self.current = test_piece
            case Move.drop:
                test_piece: PieceData | None = move_drop(
                    self.board, self.current, self.options.board_width
                )
                if test_piece is not None:
                    self.current = test_piece
            case Move.sonic_left:
                test_piece: PieceData = sonic_left(
                    self.board, self.current, self.options.board_width
                )
                self.current = test_piece
            case Move.sonic_right:
                test_piece: PieceData = sonic_right(
                    self.board, self.current, self.options.board_width
                )
                self.current = test_piece
            case Move.sonic_drop:
                test_piece: PieceData = sonic_drop(
                    self.board, self.current, self.options.board_width
                )
                self.current = test_piece
            case Move.rotate_cw:
                test_piece: PieceData | None = rotate_cw(
                    self.board, self.current, self.options.board_width
                )
                if test_piece is not None:
                    self.current = test_piece
                    self.is_immobile = check_immobile(
                        self.board, self.current, self.options.board_width
                    )
            case Move.rotate_ccw:
                test_piece: PieceData | None = rotate_ccw(
                    self.board, self.current, self.options.board_width
                )
                if test_piece is not None:
                    self.current = test_piece
                    self.is_immobile = check_immobile(
                        self.board, self.current, self.options.board_width
                    )
            case Move.hold:
                if not self.can_hold:
                    return events

                new_held: Piece = self.current.piece
                if self.held:
                    self.queue.appendleft(self.held)
                    self.held = self.current.piece
                self.current = self.next_piece()

                self.held = new_held
                self.can_hold = False
                self.is_immobile = check_immobile(
                    self.board, self.current, self.options.board_width
                )

                if _check_collision(
                    self.board,
                    self.current.piece,
                    self.current.x,
                    self.current.y,
                    self.current.rotation,
                    self.options.board_width,
                ):
                    self.dead = True
                    events.append(GameOverEvent())
            case Move.hard_drop:
                initial_piece_state: PieceData = self.current.copy()

                self.current: PieceData = sonic_drop(
                    self.board, self.current, self.options.board_width
                )

                final_piece_state: PieceData = self.current.copy()

                self.board = _place_piece(
                    self.board, self.current, self.options.board_width
                )
                self.board, cleared_lines = clear_lines(self.board)
                cleared: int = len(cleared_lines)
                for line in cleared_lines:
                    if "G" in line["blocks"]:
                        self.garbage_cleared += 1

                pc = check_pc(self.board)

                score_info = ScoreInfo(
                    pc=pc,
                    lines_cleared=len(cleared_lines),
                    is_immobile=self.is_immobile,
                    b2b=self.b2b,
                    combo=self.combo,
                )

                score_data: ScoreData = calculate_score(
                    score_info, self.options.attack_table, self.options.combo_table
                )

                self.combo = score_data.combo
                self.b2b = score_data.b2b

                self.score += score_data.score
                self.pieces_placed += 1

                attack = score_data.score
                cancelled: int = min(len(self.garbage_queue), attack)
                for _ in range(cancelled):
                    self.garbage_queue.popleft()
                attack -= cancelled

                tanked_lines: list[int] = []
                if cleared == 0:
                    self.board, tanked_lines = process_garbage(
                        self.board, self.garbage_queue, self.options.board_width
                    )

                events.append(
                    PiecePlacedEvent(
                        initial=initial_piece_state, final=final_piece_state
                    )
                )

                if score_data.clear_name:
                    events.append(
                        ClearEvent(
                            clearName=score_data.clear_name,
                            allSpin=score_data.all_spin,
                            b2b=score_data.b2b,
                            combo=score_data.combo,
                            pc=pc,
                            attack=attack,
                            cancelled=cancelled,
                            piece=final_piece_state,
                            clearedLines=cleared_lines,
                        )
                    )

                if tanked_lines:
                    events.append(DamageTankedEvent(holeIndices=tanked_lines))

                self.current = self.next_piece()
                self.can_hold = True
                self.is_immobile = check_immobile(
                    self.board, self.current, self.options.board_width
                )

                if _check_collision(
                    self.board,
                    self.current.piece,
                    self.current.x,
                    self.current.y,
                    self.current.rotation,
                    self.options.board_width,
                ):
                    self.dead = True
                    events.append(GameOverEvent())
            case _:
                raise ValueError(f"Invalid move: {move}")

        return events

    def dangerously_drop_piece(self, piece_data: PieceData) -> List[Event]:
        """
        Drops a piece on the board without checking for collisions.

        Parameters:
        --------
        piece_data : PieceData
            The piece data to drop on the board.

        Returns:
        --------
        List[Event]
            A list of events generated by dropping the piece.

        Raises:
        --------
        ValueError
            If the move cannot be executed when the game is dead.
        """
        events: List[Event] = []

        if self.dead:
            raise ValueError("Cannot act when dead")

        if self.current.piece != piece_data.piece:
            if not self.can_hold:
                raise ValueError("Cannot hold twice in a row")

            new_held: Piece = self.current.piece
            if self.held:
                self.queue.appendleft(self.held)
                self.held = self.current.piece
            self.current = self.next_piece()

            if self.current.piece != piece_data.piece:
                raise ValueError(
                    "Neither Current nor Held/Next piece does not match piece data"
                )

            self.held = new_held
            self.can_hold = False
            self.is_immobile = check_immobile(
                self.board, self.current, self.options.board_width
            )

            if _check_collision(
                self.board,
                self.current.piece,
                self.current.x,
                self.current.y,
                self.current.rotation,
                self.options.board_width,
            ):
                self.dead = True
                events.append(GameOverEvent())
                return events

        initial_piece_state: PieceData = self.current.copy()

        self.current = piece_data

        final_piece_state: PieceData = self.current.copy()

        self.board = _place_piece(self.board, self.current, self.options.board_width)
        self.board, cleared_lines = clear_lines(self.board)
        cleared: int = len(cleared_lines)
        for line in cleared_lines:
            if "G" in line["blocks"]:
                self.garbage_cleared += 1

        pc = check_pc(self.board)

        score_info = ScoreInfo(
            pc=pc,
            lines_cleared=len(cleared_lines),
            is_immobile=self.is_immobile,
            b2b=self.b2b,
            combo=self.combo,
        )

        score_data: ScoreData = calculate_score(
            score_info, self.options.attack_table, self.options.combo_table
        )

        self.combo = score_data.combo
        self.b2b = score_data.b2b

        self.score += score_data.score
        self.pieces_placed += 1

        attack = score_data.score
        cancelled: int = min(len(self.garbage_queue), attack)
        for _ in range(cancelled):
            self.garbage_queue.popleft()
        attack -= cancelled

        tanked_lines: list[int] = []
        if cleared == 0:
            self.board, tanked_lines = process_garbage(
                self.board, self.garbage_queue, self.options.board_width
            )

        events.append(
            PiecePlacedEvent(initial=initial_piece_state, final=final_piece_state)
        )

        if score_data.clear_name:
            events.append(
                ClearEvent(
                    clearName=score_data.clear_name,
                    allSpin=score_data.all_spin,
                    b2b=score_data.b2b,
                    combo=score_data.combo,
                    pc=pc,
                    attack=attack,
                    cancelled=cancelled,
                    piece=final_piece_state,
                    clearedLines=cleared_lines,
                )
            )

        if tanked_lines:
            events.append(DamageTankedEvent(holeIndices=tanked_lines))

        self.current = self.next_piece()
        self.can_hold = True
        self.is_immobile = check_immobile(
            self.board, self.current, self.options.board_width
        )

        if _check_collision(
            self.board,
            self.current.piece,
            self.current.x,
            self.current.y,
            self.current.rotation,
            self.options.board_width,
        ):
            self.dead = True
            events.append(GameOverEvent())

        return events

    def queue_attack(self, attack: int) -> None:
        """
        Queue an attack to be sent to the player.

        Parameters:
        --------
        attack : int
            The number of garbage lines to send to the player.
        """
        public_garbage_lines: List[PublicGarbageLine] = [
            PublicGarbageLine(delay=self.options.garbage_delay) for _ in range(attack)
        ]
        garbage_lines: List[GarbageLine] = generate_garbage(
            public_garbage_lines,
            self.options.garbage_messiness,
            self.options.board_width,
        )
        self.queue_garbage_lines(garbage_lines)

    def queue_garbage(self, hole_indices: list[int]) -> None:
        """
        Queue garbage lines to be sent to the player.

        Parameters:
        --------
        hole_indices : List[int]
            A list of indices representing the holes in the player's board.
        """
        self.garbage_queue.extend(
            [
                GarbageLine(delay=self.options.garbage_delay, index=i)
                for i in hole_indices
            ]
        )

    def queue_garbage_lines(self, garbage_lines: list[GarbageLine]) -> None:
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
        representation: str = ""
        rendered_board = [
            ["." if cell is None else cell for cell in row] for row in self.board
        ]
        rendered_board.reverse()
        for row in rendered_board:
            representation += "".join(row) + "\n"
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

    def render_board(self, render_current: bool = True) -> None:
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
            "I": Fore.CYAN,
            "O": Fore.YELLOW,
            "T": Fore.MAGENTA,
            "S": Fore.GREEN,
            "Z": Fore.RED,
            "J": Fore.BLUE,
            "L": Fore.WHITE,
            "G": Fore.BLACK + Back.WHITE,
        }

        piece_info = []

        piece_info.append("Queue:")
        for i, piece in enumerate(list(self.queue)[:6]):
            if i > 0:
                piece_info.append("")
            piece_matrix = get_piece_matrix(piece, 0)
            for row in piece_matrix[::-1]:
                piece_info.append(
                    "    "
                    + "".join(
                        [
                            f"{color_map[cell]}██{Style.RESET_ALL}" if cell else "  "
                            for cell in row
                        ]
                    )
                )

        piece_info = [piece for piece in reversed(piece_info)]

        print("┌" + "──" * self.options.board_width + "┐")

        for y in range(self.options.board_height - 1, -1, -1):
            print("│", end="")
            for x in range(self.options.board_width):
                if y < len(t_board) and t_board[y][x] is not None:
                    piece = t_board[y][x]
                    print(f"{color_map[piece]}██{Style.RESET_ALL}", end="")
                else:
                    print("  ", end="")
            print("│", end="")

            if len(piece_info):
                print(piece_info.pop())
            else:
                print()

        print("└" + "──" * self.options.board_width + "┘")
        print(f"  Score: {self.score}")
        print(f"  Combo: {self.combo}")
        print(f'  B2B: {"Yes" if self.b2b else "No"}')
        print(f"  Pieces: {self.pieces_placed}")
        print(f'  Hold: {self.held or "Empty"}')

        print(f"\nGarbage queued: {len(self.garbage_queue)}")

    def generate_moves(
        self,
        include_held: bool = True,
        include_queue: bool = True,
        algo: Literal["bfs", "dfs", "dijk", "dijk-short"] = "bfs",
    ) -> dict[PieceData, list[Move]]:
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
        held: Piece | None = self.held if include_held else None
        first_piece: Piece | None = self.queue[0] if include_queue else None
        alternative: Piece | None = first_piece if held is None else held
        return generate_moves(
            self.board,
            self.current.piece,
            alternative,
            self.options.board_height,
            self.options.board_width,
            algo,
        )

    def draw_board(self) -> Image:
        """
        Draws the game board as an image.

        Returns:
        --------
        Image
            The image of the game board.
        """
        color_map = {
            "I": (0, 255, 255),
            "O": (255, 255, 0),
            "T": (128, 0, 128),
            "S": (0, 128, 0),
            "Z": (255, 0, 0),
            "J": (0, 0, 255),
            "L": (255, 255, 255),
            "G": (0, 0, 0),
        }

        queue_width: int = 40
        block_size: int = 10
        border_width: int = 2
        font_size: int = 8

        board_width_px = self.options.board_width * block_size
        board_height = max(self.options.board_height, 20)
        board_height_px = board_height * block_size

        img_width = board_width_px + queue_width
        img_height = board_height_px

        img = Image.new("RGB", (img_width, img_height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.fontmode = "L"

        for y in range(board_height):
            if y >= len(self.board):
                break
            for x in range(self.options.board_width):
                if self.board[y][x] is not None:
                    color = color_map[self.board[y][x]]
                    block_x = x * block_size
                    block_y = (board_height - y - 1) * block_size
                    block_rect = (
                        block_x + border_width,
                        block_y + border_width,
                        block_x + block_size - border_width,
                        block_y + block_size - border_width,
                    )
                    draw.rectangle(block_rect, fill=color)

        queue_x = board_width_px
        queue_y = 0
        queue_width_px = queue_width - border_width
        queue_height_px = border_width + font_size + 10 + block_size * 12
        queue_rect = (
            queue_x + border_width,
            queue_y + border_width,
            queue_x + queue_width_px,
            queue_y + queue_height_px,
        )
        draw.rectangle(queue_rect, fill=(64, 64, 64))

        queue_text_x = queue_x + border_width + 5
        queue_text_y = queue_y + border_width + 5
        queue_text = "Queue:"
        font = ImageFont.load_default(font_size)
        draw.text(
            (queue_text_x, queue_text_y), queue_text, fill=(255, 255, 255), font=font
        )

        queue_block_size = block_size // 2
        queue_block_x = queue_x + border_width + 5
        queue_block_y = queue_text_y + font_size + 5
        for piece in reversed(list(self.queue)[:6]):
            piece_matrix = get_piece_matrix(piece, 0)
            for y, row in enumerate(piece_matrix[::-1]):
                for x, cell in enumerate(row):
                    if cell:
                        color = color_map[piece.value]
                        block_x = queue_block_x + x * queue_block_size
                        block_y = queue_block_y + y * queue_block_size
                        block_rect = (
                            block_x + border_width,
                            block_y + border_width,
                            block_x + queue_block_size - border_width,
                            block_y + queue_block_size - border_width,
                        )
                        draw.rectangle(block_rect, fill=color)
            queue_block_y += queue_block_size * 4

        held_x = board_width_px
        held_y = queue_height_px
        held_width_px = queue_width_px
        held_height_px = board_height_px - queue_height_px
        held_rect = (
            held_x + border_width,
            held_y + border_width,
            held_x + held_width_px,
            held_y + held_height_px,
        )
        draw.rectangle(held_rect, fill=(32, 32, 32))
        held_x = queue_x + border_width + 5
        held_y = queue_block_y + 5
        held_text = "Hold:"
        draw.text((held_x, held_y), held_text, fill=(255, 255, 255), font=font)

        if self.held:
            held_block_x = held_x
            held_block_y = held_y + font_size + 5
            held_piece_matrix = get_piece_matrix(self.held, 0)
            for y, row in enumerate(held_piece_matrix[::-1]):
                for x, cell in enumerate(row):
                    if cell:
                        color = color_map[self.held.value]
                        block_x = held_block_x + x * queue_block_size
                        block_y = held_block_y + y * queue_block_size
                        block_rect = (
                            block_x + border_width,
                            block_y + border_width,
                            block_x + queue_block_size - border_width,
                            block_y + queue_block_size - border_width,
                        )
                        draw.rectangle(block_rect, fill=color)

        current_x = self.current.x * block_size
        current_y = (self.options.board_height - self.current.y - 1) * block_size
        current_piece_matrix = get_piece_matrix(
            self.current.piece, self.current.rotation
        )
        for y, row in enumerate(current_piece_matrix[::-1]):
            for x, cell in enumerate(row):
                if cell:
                    color = color_map[self.current.piece.value]
                    block_x = current_x + x * block_size
                    block_y = current_y + y * block_size
                    block_rect = (
                        block_x + border_width,
                        block_y + border_width,
                        block_x + block_size - border_width,
                        block_y + block_size - border_width,
                    )
                    draw.rectangle(block_rect, fill=color)

        return img

    @property
    def game_over(self):
        return self.dead
