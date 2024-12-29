import random
import time
import pygame
import sys

import random
# Constants
from ai_player import Chromosome, calculate_fitness, crossover, mutate, genetic_algorithm
from ai_player import update_revealed_ranks, evaluate_move, find_best_move
from ai_player import POPULATION_SIZE, GENERATIONS, MUTATION_RATE

import pygame
import sys
from ui import draw_board, display_game_over, animate_move, draw_button, button_clicked, arrange_troops, play_screen
from ui import TILE_SIZE, FPS, WHITE, RED, BLUE, BLACK, POPULATION_SIZE, GENERATIONS, MUTATION_RATE, GRID_COLOR, BUTTON_COLOR, BUTTON_HOVER_COLOR, BOARD_SIZE, BUTTON_WIDTH, BUTTON_HEIGHT

from game import Piece, print_board_setup, is_within_bounds, generate_possible_moves, player_move, ai_turn, resolve_attack, player_turn


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

revealed_human_ranks = {}



# Main game function
import pygame
import sys
import time

# Main game function
def main():
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE * TILE_SIZE, BOARD_SIZE * TILE_SIZE))
    pygame.display.set_caption("Stratego Game")
    clock = pygame.time.Clock()

    # Step 1: Show the Play Screen and wait for "Go" button click
    play_screen()  # Call play screen function

    # After the "Go" button is clicked, move to the arrange_troops screen
    board_ai = genetic_algorithm().board_config
    print("BOARD_AI\n")
    print(board_ai)
    
    # Use the arrange_troops function to arrange the human player's board
    board_human = arrange_troops()
    print("BOARD_HUMAN\n")
    print(board_human)
    
    # Merge the AI board (first two rows) with the human board (last two rows)
    board = board_ai[:6] + board_human[6:]
    
    print("Combined Board Setup:")
    print(board)
    print("\n\nTYPE :",board[2][1])
    
    player_turn_indicator = True  # True means it's the player's turn
    start_pos = None  # Initialize the starting position

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Player's turn logic
            if player_turn_indicator:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    selected_tile = (mouse_y // TILE_SIZE, mouse_x // TILE_SIZE)
                    piece = board[selected_tile[0]][selected_tile[1]]
                    if piece and piece.player == "Human":
                        start_pos = selected_tile  # Store the starting position
                        print(f"Selected piece: {piece.rank}")
                        possible_moves = generate_possible_moves(start_pos, board)
                        print(f"Possible moves: {possible_moves}")  # Print possible moves
                    elif start_pos and selected_tile != start_pos:
                        end_pos = selected_tile
                        player_turn(start_pos, end_pos, board)
                        player_turn_indicator = False  # Switch to AI's turn
                        start_pos = None  # Reset start position after move

        if not player_turn_indicator:  # AI's turn
            time.sleep(1)
            ai_turn(board)
            player_turn_indicator = True  # Switch back to player's turn

        screen.fill((240,240,240))
        
        # Draw the board, passing the combined board setup
        draw_board(screen, board)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
