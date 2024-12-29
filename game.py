import random
import time
import pygame
import sys
import random

# Constants

TILE_SIZE = 60
FPS = 60
WHITE = (255, 255, 255)
#RED = (255, 0, 0)
#BLUE = (0, 0, 255)
BLACK = (0,0,0)

# Colors
RED = (255, 0, 0)
BLUE = (0, 50, 250)


# Genetic Algorithm Constants
POPULATION_SIZE = 20
GENERATIONS = 50
MUTATION_RATE = 0.1


# Constants
GRID_COLOR = (150, 130, 60)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)

BOARD_SIZE = 8
TILE_SIZE = 60
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 40



class Piece:
    def __init__(self, rank, player):
        self.rank = rank  # Rank can be an integer or string based on piece type
        self.revealed = False
        self.move_history = []
        self.player = player
        self.is_movable = True  # Default to movable

        # Set immobility for Bomb and flag
        if self.rank == 'B' or self.rank == 'F':
            self.is_movable = False

    def __str__(self):
        return str(self.rank) if self.revealed else "?"

    def __repr__(self):
        return f"Piece({self.rank}, {self.player})"
    
    def __hash__(self):
        return hash((self.rank, self.player))

    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.compare(other) == 0
        return False

    def __lt__(self, other):
        if isinstance(other, Piece):
            return self.compare(other) < 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Piece):
            return self.compare(other) <= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Piece):
            return self.compare(other) > 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Piece):
            return self.compare(other) >= 0
        return NotImplemented

    def compare(self, other):
        """
        Compare two pieces based on their rank (either string or int).
        Returns:
        -1 if self is less than other,
         0 if equal,
         1 if self is greater than other.
        """
        # Handle comparison with 'B' (Bomb) and 'F' (Flag)
        if isinstance(self.rank, int) and isinstance(other.rank, int):
            # Integer vs Integer
            return self.rank - other.rank
        elif isinstance(self.rank, int) and isinstance(other.rank, str):
            if other.rank == 'B':
                # Bomb beats all ranks except 3
                return -1 if self.rank != 3 else 0
            elif other.rank == 'F':
                # Flag beats all ranks
                return 1
        elif isinstance(self.rank, str) and isinstance(other.rank, int):
            if self.rank == 'B':
                # Bomb beats all ranks except 3
                return 1 if other != 3 else 0
            elif self.rank == 'F':
                # Flag beats all ranks
                return -1
        elif isinstance(self.rank, str) and isinstance(other.rank, str):
            # String vs String comparison ('F' vs 'B')
            if self.rank == 'F' and other.rank == 'B':
                return 1
            elif self.rank == 'B' and other.rank == 'F':
                return -1
            return 0

        return 0

def print_board_setup(board):
    print("Initial Board Setup:")
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            if piece:
                position = f"({row}, {col})"
                print(f"Player: {piece.player}, Rank: {piece.rank}, Position: {position}")
            else:
                print(f"Player: {piece.player}, Rank: - , Position: {position}")

def is_within_bounds(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE


def generate_possible_moves(piece_position, board):
    x, y = piece_position
    moves = []
    piece = board[x][y]

    # Check if the piece is movable
    if not piece.is_movable:
        return moves  # Return empty moves if the piece is immovable

    # Movement offsets: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    if piece.player == "Human":
        # Red pieces (player) can move to rows 0-4 (decreasing row count)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check for moving up (decreasing row count)
            if dx == -1 and is_within_bounds(nx, ny):
                if board[nx][ny] is None or board[nx][ny].player != piece.player:
                    moves.append((nx, ny))

            # Check for lateral movement (left/right)
            elif dx == 0 and is_within_bounds(nx, ny):
                if board[nx][ny] is None or board[nx][ny].player != piece.player:
                    moves.append((nx, ny))

    else:
        # Blue pieces (AI) can move to rows 5-7 (increasing row count)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check for moving down (increasing row count)
            if dx == 1 and is_within_bounds(nx, ny):
                if board[nx][ny] is None or board[nx][ny].player != piece.player:
                    moves.append((nx, ny))

            # Check for lateral movement (left/right)
            elif dx == 0 and is_within_bounds(nx, ny):
                if board[nx][ny] is None or board[nx][ny].player != piece.player:
                    moves.append((nx, ny))

    return moves


def player_move(start, end, board):
    attacker = board[start[0]][start[1]]
    defender = board[end[0]][end[1]]
    
    if defender and defender.player != attacker.player:
        print(f"Attack! {attacker.rank} attacks {defender.rank}")
        winner = resolve_attack(attacker, defender)
        print(winner)
        if winner:
            if winner == attacker:
                # The attacker wins
                board[end[0]][end[1]] = winner  # Move the winning attacker to the defender's position
                print(f"{winner.rank} wins the battle! {winner.rank} revealed!")
                board[start[0]][start[1]] = None  # Clear the attacker's original position
            else:
                # The defender wins
                board[end[0]][end[1]] = defender  # Defender remains in place
                board[start[0]][start[1]] = None  # Remove the attacker from the board
                print(f"{defender.rank} wins the battle! {defender.rank} remains in position.")

            if winner.player == "Human":
                update_revealed_ranks(winner,end) 
                print("Revealed Human Pieces :")
            
        else:
            print("received none now removing")
            # Both pieces are eliminated in case of a tie
            board[start[0]][start[1]] = None  # Clear the attacker's position
            board[end[0]][end[1]] = None  # Clear the defender's position
            print("Both pieces are eliminated!")
            
    else:
        # Move the piece to an empty cell if there's no attack
        board[end[0]][end[1]] = attacker  

    # Clear the start position only if it's a valid move or an attack where no battle occurs
    if defender is None:
        board[start[0]][start[1]] = None  
    
    if attacker.player == "Human" and attacker.rank in revealed_human_ranks:
        update_revealed_ranks(attacker, end)
 


def ai_turn(board):
    best_move = find_best_move(board)
    if best_move:
        (start, end) = best_move
        attacker = board[start[0]][start[1]]
        defender = board[end[0]][end[1]]
        
        if defender and defender.player != attacker.player:
            print(f"AI Attack! {attacker.rank} attacks {defender.rank}")
            winner = resolve_attack(attacker, defender)
             
            if winner:
                if winner == attacker:
                    # The attacker wins
                    board[end[0]][end[1]] = winner  # Move the winning attacker to the defender's position
                    print(f"{winner.rank} wins the battle! {winner.rank} revealed!")
                    board[start[0]][start[1]] = None  # Clear the attacker's original position
                else:
                    # The defender wins
                    board[end[0]][end[1]] = defender  # Defender remains in place
                    board[start[0]][start[1]] = None  # Remove the attacker from the board
                    print(f"{defender.rank} wins the battle! {defender.rank} remains in position.")
            
                if winner.player == "Human":
                    update_revealed_ranks(winner, end) 
                    print("Revealed Human Pieces :")
            else:
                print("received none now removing")
                # Both pieces are eliminated in case of a tie
                board[start[0]][start[1]] = None  # Clear the attacker's position
                board[end[0]][end[1]] = None  # Clear the defender's position
                print("Both pieces are eliminated!")

        else:
            board[end[0]][end[1]] = attacker  # Move the piece to an empty cell
        
        board[start[0]][start[1]] = None  # Clear the start position


revealed_human_ranks = {}


def resolve_attack(attacker, defender):
    # Flag capture scenario
    if defender.rank == "F":
        print(f"{attacker.player}'s {attacker.rank} captures the Flag! Game over.")
        display_game_over(attacker.player)
        return attacker  # Game over, return attacker as the winner

    # Reveal ranks for visibility
    attacker.revealed = True
    defender.revealed = True

        # Bomb vs. Miner scenario
    if defender.rank == "B":
        if attacker.rank == 3:  # Miner rank
            print("Miner defuses the Bomb!")
            return attacker  # Miner wins and defuses the bomb
        else:
            print(f"{attacker.player}'s {attacker.rank} hits the Bomb and is removed.")
            return defender  # Bomb wins; attacker is removed

    # Spy vs. General scenario
    if attacker.rank == 1 and defender.rank == 6:  # Spy and General ranks
        print("Spy uses charm to defeat the General!")
        return attacker  # Spy wins against General

    # Standard rank comparison for other cases
    if isinstance(attacker.rank, int) and isinstance(defender.rank, int):
        if attacker.rank < defender.rank:
            print(f"{attacker.player}'s {attacker.rank} is defeated by {defender.player}'s {defender.rank}.")
            return defender  # Defender wins
        elif attacker.rank > defender.rank:
            print(f"{attacker.player}'s {attacker.rank} defeats {defender.player}'s {defender.rank}.")
            return attacker  # Attacker wins
        else:
            print(f"Both {attacker.rank} and {defender.rank} are eliminated in a tie.")
            print("returning none")
            return None  # Both pieces are removed

    # Invalid case fallback
    print("Invalid attack scenario.")
    return None


def player_turn(start, end, board):
    piece = board[start[0]][start[1]]
    if piece and (end in generate_possible_moves(start, board)):
        player_move(start, end, board)
    else:
        print("Invalid move. Try again.")

revealed_human_ranks = {}