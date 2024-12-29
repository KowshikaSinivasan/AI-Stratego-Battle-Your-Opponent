import random
import time
import pygame
import sys
import random

from game import Piece


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


class Chromosome:
    BOARD_SIZE = 8
    def __init__(self, board_config=None):
        # Chromosome contains both AI and Human board configuration
        self.board_config = board_config if board_config else self.random_config()
        self.fitness = 0

    def random_config(self):
        board = [[None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]

        # AI Fixed rows
        ai_row_0 = ['B', 'F', 2, 2, 1, 5, 3, 4]
        ai_row_1 = [2, 2, 2, 2, 6, 3, 4, 'B']
        
        # Human Fixed rows
        human_row_7 = ['B', 'F', 2, 2, 1, 5, 3, 4]
        human_row_6 = [2, 2, 2, 2, 6, 3, 4, 'B']

        # Place AI pieces in randomized columns within the fixed row structure
        board[0] = [Piece(rank, 'AI') for rank in random.sample(ai_row_0, len(ai_row_0))]
        board[1] = [Piece(rank, 'AI') for rank in random.sample(ai_row_1, len(ai_row_1))]

        # Place Human pieces in randomized columns within the fixed row structure
        board[6] = [Piece(rank, 'Human') for rank in random.sample(human_row_6, len(human_row_6))]
        board[7] = [Piece(rank, 'Human') for rank in random.sample(human_row_7, len(human_row_7))]

        return board
    
def is_adjacent_to_flag(row, col, chromosome):
    """Check if a given cell is adjacent to the AI's flag."""
    flag_position = None
    for r in range(2):  # Only search AI's first two rows
        for c in range(Chromosome.BOARD_SIZE):
            piece = chromosome.board_config[r][c]
            if piece and piece.player == "AI" and piece.rank == 'F':
                flag_position = (r, c)
                break
    if flag_position:
        # Check if the piece is one row away or one column away, but not both
        row_diff = abs(flag_position[0] - row)
        col_diff = abs(flag_position[1] - col)
        return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)
    return False

def is_near_bomb_zone(position, chromosome):
    """Check if a Miner is near any AI bombs."""
    row, col = position
    for r in range(2):  # Only search AI's first two rows
        for c in range(Chromosome.BOARD_SIZE):
            piece = chromosome.board_config[r][c]
            if piece and piece.player == "AI" and piece.rank == 'B':
                if abs(r - row) <= 1 and abs(c - col) <= 1:
                    return True
    return False

def calculate_fitness(chromosome):
    fitness = 0
    
    # Iterate through the entire board
    for row in range(Chromosome.BOARD_SIZE):
        for col in range(Chromosome.BOARD_SIZE):
            piece = chromosome.board_config[row][col]
            
            if piece and piece.player == "AI":
                if piece.rank == 'F':
                    fitness += 100  # Reward flag protection
                elif piece.rank == 'B' and is_adjacent_to_flag(row, col, chromosome):
                    fitness += 30  # Reward bombs adjacent to flag

                if piece.rank in [2, 4]:  # Scouts or Sergeants (AI)
                    if row == 1:  # Reward for AI being in row 1 (closer to opponent)
                        fitness += 20
                    elif row == 0:  # Penalize for AI being too far back (row 0)
                        fitness -= 10

                if piece.rank == 3:  # Miner (AI)
                    if is_near_bomb_zone((row, col), chromosome):
                        fitness += 20  # Reward Miners near bombs

                if piece.rank == 1:  # Spy (AI)
                    fitness -= row * 3  # Penalize Spy near frontlines
                
            elif piece and piece.player == "Human":
                if piece.rank == 'F':
                    fitness += 100  # Reward flag protection
                elif piece.rank == 'B' and is_adjacent_to_flag(row, col, chromosome):
                    fitness += 30  # Reward bombs adjacent to flag

                if piece.rank in [2, 4]:  # Scouts or Sergeants (Human)
                    if row == 6:  # Reward for human being in row 6 (closer to opponent)
                        fitness += 20
                    elif row == 7:  # Penalize for human being too far back (row 7)
                        fitness -= 10

                if piece.rank == 3:  # Miner (Human)
                    if is_near_bomb_zone((row, col), chromosome):
                        fitness += 20  # Reward Miners near bombs

                if piece.rank == 1:  # Spy (Human)
                    fitness -= row * 3  # Penalize Spy near frontlines

    chromosome.fitness = fitness

def crossover(parent1, parent2):
    child_config = [[None for _ in range(Chromosome.BOARD_SIZE)] for _ in range(Chromosome.BOARD_SIZE)]
    
    # Iterate through each row
    for row in range(Chromosome.BOARD_SIZE):
        # Randomly select one of the parents' rows for the child
        if random.random() < 0.5:
            # Select row from parent1
            child_config[row] = parent1.board_config[row].copy()
        else:
            # Select row from parent2
            child_config[row] = parent2.board_config[row].copy()

    return Chromosome(child_config)

def mutate(chromosome):
    if random.random() < MUTATION_RATE:
        ai_positions_row_0 = [(0, j) for j in range(Chromosome.BOARD_SIZE)]
        ai_positions_row_1 = [(1, j) for j in range(Chromosome.BOARD_SIZE)]
        random.shuffle(ai_positions_row_0)
        random.shuffle(ai_positions_row_1)
        
        # Mutate AI rows by swapping pieces within rows
        pos1, pos2 = ai_positions_row_0[:2]
        chromosome.board_config[pos1[0]][pos1[1]], chromosome.board_config[pos2[0]][pos2[1]] = \
            chromosome.board_config[pos2[0]][pos2[1]], chromosome.board_config[pos1[0]][pos1[1]]

        pos1, pos2 = ai_positions_row_1[:2]
        chromosome.board_config[pos1[0]][pos1[1]], chromosome.board_config[pos2[0]][pos2[1]] = \
            chromosome.board_config[pos2[0]][pos2[1]], chromosome.board_config[pos1[0]][pos1[1]]

        human_positions_row_6 = [(6, j) for j in range(Chromosome.BOARD_SIZE)]
        human_positions_row_7 = [(7, j) for j in range(Chromosome.BOARD_SIZE)]
        random.shuffle(human_positions_row_6)
        random.shuffle(human_positions_row_7)

        # Mutate Human rows by swapping pieces within rows
        pos1, pos2 = human_positions_row_6[:2]
        chromosome.board_config[pos1[0]][pos1[1]], chromosome.board_config[pos2[0]][pos2[1]] = \
            chromosome.board_config[pos2[0]][pos2[1]], chromosome.board_config[pos1[0]][pos1[1]]

        pos1, pos2 = human_positions_row_7[:2]
        chromosome.board_config[pos1[0]][pos1[1]], chromosome.board_config[pos2[0]][pos2[1]] = \
            chromosome.board_config[pos2[0]][pos2[1]], chromosome.board_config[pos1[0]][pos1[1]]
        

def genetic_algorithm():
    population = [Chromosome() for _ in range(POPULATION_SIZE)]

    for gen in range(GENERATIONS):
        for chrom in population:
            calculate_fitness(chrom)

        population.sort(key=lambda x: x.fitness, reverse=True)
        population = population[:POPULATION_SIZE // 2]

        while len(population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(population[:POPULATION_SIZE // 4], 2)
            child = crossover(parent1, parent2)
            mutate(child)
            population.append(child)

        print(f"Generation {gen+1} - Best Fitness: {population[0].fitness}")

    return population[0]

revealed_human_ranks = {}

def update_revealed_ranks(piece, piece_position):
    """ Update knowledge of revealed ranks if an AI piece successfully attacks a human piece. """
    if piece and piece.player == "Human":
        # Record the revealed rank of the human piece
        revealed_human_ranks[piece.rank] = piece_position

def get_adjacent_positions(position):
    """Returns valid adjacent board positions to the given location."""
    x, y = position
    # Generate adjacent positions and filter those within board boundaries
    return [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if is_within_bounds(x + dx, y + dy)]

def is_near_flag_zone(position):
    """Determines if the given position is near the opponent's flag zone."""
    # Assuming opponent's flag zone is in rows 0-2; adjust if needed
    return 0 <= position[0] <= 2

def is_in_vulnerable_position(board,position):
    x, y = position
    # Here, we define a "vulnerable position" as one that is near an enemy piece or close to an unknown piece.
    # This is for situations where we want to intentionally expose weaker pieces like spies or scouts.
    
    enemy_player = "Human"  # AI is playing against the human
    
    # Check if the position is next to an enemy piece (adjacent squares)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Skip the current position
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]):  # Check if within board bounds
                piece = board[nx][ny]
                if piece and piece.player == enemy_player:  # If there's an enemy piece here
                    return True
    return False

def is_near_enemy_troops(board,position):
    x, y = position
    enemy_player = "Human"  # AI is playing against the human
    
    # Check the 8 adjacent positions (up, down, left, right, and diagonals)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue  # Skip the current position
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]):  # Check if within board bounds
                piece = board[nx][ny]
                if piece and piece.player == enemy_player:  # If there's an enemy piece here
                    return True
    return False


def evaluate_move(move, piece, board, start_position):
    x, y = move  # Unpack the end position (potential move)
    target_piece = board[x][y] if board[x][y] else None  # Get target piece if it exists
    
    score = 0

    # 1. Aggressive Behavior for Rank 4/5 Pieces (Strong pieces)
    if piece.rank in [4, 5]:  # Stronger pieces like Major (4) or General (5)
        if target_piece:  # If there's a target piece
            if target_piece.player == "Human":  # Target enemy pieces
                score += 90  # Neutral but still a valid move
                
        # Encourage strong pieces to move into enemy territory
        if x > start_position[0]:  # Moving towards the enemy flag zone
            score += 50  # Big reward for advancing aggressively
        elif x == start_position[0]:  # Same row, penalize lateral movement
            score -= 10

    # 2. Spy vs. Marshall Strategy (Keep the spy cautious)
    if piece.rank == 1:  # Spy
        if target_piece and target_piece.player == "Human" and target_piece.rank == 6:  # Target is Marshall
            score += 50  # Prioritize moves that target the Marshall
        else:
            score -= 10  # Discourage risky moves for the Spy

    # 3. Miner vs. Bomb Strategy
    elif piece.rank == 3:  # Miner
        if target_piece and target_piece.player == "Human" and (target_piece.rank == "B" or is_near_flag_zone(move)):
            score += 50  # Miners targeting bombs get a higher score
        elif is_near_flag_zone(move):
            score += 30  # Encourage Miners to explore potential flag zones near bombs

    # 4. Bomb and Flag-Proximity Heuristic
    if target_piece and target_piece.rank == "B":
        score += 20  # Assume potential Flag nearby if Bomb found
        for adj in get_adjacent_positions(move):
            if is_within_bounds(x, y):
                adj_piece = board[adj[0]][adj[1]]
                if not adj_piece or adj_piece.player == "AI":
                    score += 10  # Reward moves that close in around Bomb locations

    # 5. Handling Known and Unknown Human Ranks
    if target_piece and target_piece.player == "Human":
        # Check if the target piece's position is in the revealed dictionary
        for human_rank, pos in revealed_human_ranks.items():
            if pos == move:  # If the position of the target piece is revealed
                comparison_result = piece.compare(target_piece)
                if comparison_result > 0:
                    score += 70  # Favor moves where AI has a higher rank
                elif comparison_result < 0:
                    score -= 50  # Discourage moves where AI is at a disadvantage
                else:
                    score += 45  # Neutral for same-rank encounters
                break
        else:  # If the position is not revealed
            if piece.rank in [2, 3, 6]:
                score += 70  # Prefer using lower-ranked pieces for scouting
            elif piece.rank in [5, 4]:
                score -= 10  # Avoid sending the General into uncertain attacks
            else:
                score += 30  # Moderate risk if it's neither high nor low rank
            if is_near_flag_zone(move):
                score += 10  # Take risk if near enemy's flag zone
            elif is_near_flag_zone(start_position):
                score -= 10  # Avoid risky moves near own flag zone

    # 6. Penalize Risk for Revealed Pieces
    if piece.revealed:
        score -= 10  # Reduce score for revealed pieces in risky moves

    # 7. Encourage Exploratory Moves for Specific Pieces
    if piece.rank in [2, 3, 6] and is_near_enemy_troops(board, start_position):
        score += 100  # Encourage scouts and miners to explore enemy territory
    elif piece.rank in [5, 4] and is_near_enemy_troops(board, start_position):
        score -= 20  # Avoid sending higher-ranked pieces too far ahead unless necessary

    # 8. Favor Vulnerable Pieces in the Opponent's Weak Zones
    if piece.rank in [1, 2, 3] and is_in_vulnerable_position(board, move):
        score += 70  # Allow pieces in weak positions to explore opponent's vulnerable zones

    # 9. High Priority for Left/Right Movements in Rows 6/7 (Exploration in Enemy Territory)
    if start_position[0] in [7]:  # If the piece is in rows 6/7, enemy territory
        if move[1] != start_position[1]:  # If there is a left/right movement
            score += 100  # Give a big reward for moving left or right in enemy territory
        else:
            score -= 5  # Penalize vertical movements in enemy territory
    else:
        # 5. Prefer Moves Toward the Opponent’s Flag Zone
        if x > start_position[0]:  # Moving up towards the human flag zone
            score += 70  # Reward for advancing
        elif x == start_position[0]:  # Same row
            score -= 20  # Penalize left-right moves
    return score


def find_best_move(board):
    best_move = None
    max_score = float('-inf')
    
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            piece = board[i][j]
            if piece and piece.player == "AI":
                possible_moves = generate_possible_moves((i, j), board)
                
                for move in possible_moves:
                    # Call evaluate_move with the starting position and the piece
                    score = evaluate_move(move, piece, board, (i, j))
                    
                    if score > max_score:
                        max_score = score
                        best_move = ((i, j), move)
    
    return best_move


