import random
import time
import pygame
import sys

import random
from game import Piece


import pygame


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


# Assuming constants like BOARD_SIZE, TILE_SIZE, WHITE, RED, BLUE, etc. are defined elsewhere in your code

# Function to draw the board in the main game window
def draw_board(screen, board):
    print(board[3][0])  # Debugging: print the piece in row 3, column 0
    print(board[0][0])  # Debugging: print the piece in row 0, column 0

    # Load background image (assumed to be loaded during the Game class initialization)
    background = pygame.image.load('bkg.png').convert()
    background = pygame.transform.scale(background, (BOARD_SIZE * TILE_SIZE, BOARD_SIZE * TILE_SIZE))

    # Blit the background to the screen
    screen.blit(background, (0, 0))

    # Define the font once, outside the loop, for efficiency
    font = pygame.font.Font(None, 36)

    # Colors for grid lines and border
    GRID_COLOR = (150, 130, 60)  # Lighter brown for grid lines
    BORDER_COLOR = (150, 130, 60)  # Darker brown for the border

    # Dimensions for the board
    board_width = BOARD_SIZE * TILE_SIZE
    board_height = BOARD_SIZE * TILE_SIZE

    # Draw the border outside the grid (thicker border)
    #border_thickness = 8
    #pygame.draw.rect(screen, BORDER_COLOR, (-border_thickness, -border_thickness, board_width + 2 * border_thickness, board_height + 2 * border_thickness), border_thickness)

    # Draw the grid and pieces
    for row in range(BOARD_SIZE):
        print("\n BOARD[ROW] = ", board[row])  # Debugging: print the row data
        for col in range(BOARD_SIZE):
            piece = board[row][col]
            color = WHITE

            # Determine the color and text based on piece properties
            if piece:
                color = RED if piece.player == "Human" else BLUE
                # Show rank for revealed pieces or for unrevealed red pieces; hide for unrevealed blue pieces
                if piece.revealed or (piece.player == "Human" and not piece.revealed):
                    text = str(piece.rank)
                else:
                    text = "?"

                # Draw the rectangle for the piece
                piece_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                piece_surface.set_alpha(200)  # Set transparency level (0-255)
                piece_surface.fill(color)
                screen.blit(piece_surface, (col * TILE_SIZE, row * TILE_SIZE))

                # Render and display the piece text
                text_surface = font.render(text, True, WHITE if piece.revealed else BLACK)
                screen.blit(text_surface, (col * TILE_SIZE + 20, row * TILE_SIZE + 10))

            # Draw the grid line with lighter brown color
            pygame.draw.rect(screen, GRID_COLOR, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

            # Tooltip logic: Show rank info when hovering over a piece
            mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
            if piece and (piece.revealed or (piece.player == "Human" and not piece.revealed)):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if rect.collidepoint(mouse_pos):
                    # Show tooltip with rank on a white background
                    tooltip_text = f"Rank: {piece.rank}"
                    tooltip_surface = font.render(tooltip_text, True, BLACK)
                    tooltip_background = pygame.Surface((tooltip_surface.get_width() + 6, tooltip_surface.get_height() + 4))
                    tooltip_background.fill(WHITE)

                    # Position tooltip above or below piece
                    tooltip_x = col * TILE_SIZE + TILE_SIZE // 2
                    tooltip_y = row * TILE_SIZE - 25 if row > 0 else row * TILE_SIZE + TILE_SIZE + 10
                    tooltip_rect = tooltip_surface.get_rect(center=(tooltip_x, tooltip_y))

                    # Draw tooltip background and then text
                    screen.blit(tooltip_background, (tooltip_rect.x - 3, tooltip_rect.y - 2))
                    screen.blit(tooltip_surface, tooltip_rect)

    # Draw the "STRATEGO" text at the bottom of the board (centered)
    text_surface = font.render("STRATEGO", True, pygame.Color("black"))
    screen.blit(text_surface, ((BOARD_SIZE * TILE_SIZE) // 2 - text_surface.get_width() // 2,
                               BOARD_SIZE * TILE_SIZE + 10))

    # Update the display after drawing everything
    pygame.display.flip()



def display_game_over(winner):
    pygame.init()

    # Load background images
    image1 = pygame.image.load('redwin.png').convert()  # Background when AI wins
    image2 = pygame.image.load('bluewin.png').convert()  # Background when Human wins

    # Set the window size based on your desired dimensions or the image size
    screen = pygame.display.set_mode((600, 400))  # Adjust the window size here
    pygame.display.set_caption("Game Over")

    # Choose the background based on the winner
    if winner == "AI":
        background = pygame.transform.scale(image2, (600, 400))  # Adjust size as needed
    else:
        background = pygame.transform.scale(image1, (600, 400))  # Adjust size as needed

    # Font and text setup
    font = pygame.font.Font(None, 36)
    exit_button_text = font.render("Exit", True, (0, 0, 0))  # Black text for exit button
    exit_button_rect = exit_button_text.get_rect(topright=(570, 10))  # Position the exit button at the top right

    # Create a grey background for the exit button
    exit_button_bg = pygame.Surface((exit_button_rect.width + 10, exit_button_rect.height + 10))
    exit_button_bg.fill((169, 169, 169))  # Grey color

    # Draw the background and text on the screen
    screen.blit(background, (0, 0))  # Blit the background image
    screen.blit(exit_button_bg, exit_button_rect.topleft)  # Blit the grey background for the exit button
    screen.blit(exit_button_text, exit_button_rect)  # Blit the exit button text

    pygame.display.flip()

    # Event handling loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):  # Check if the Exit button is clicked
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()
revealed_human_ranks = {}


def animate_move(start, end, piece, board):
    board[start[0]][start[1]] = None
    board[end[0]][end[1]] = piece
    piece.move_history.append(start)
    if len(piece.move_history) > 5:
        piece.move_history.pop(0)

# Draw button with hover effect
def draw_button(screen, text, color, hover_color, rect):
    font = pygame.font.Font(None, 30)
    mouse_pos = pygame.mouse.get_pos()
    button_color = hover_color if rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, button_color, rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def button_clicked(rect):
    return rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]


def arrange_troops():
    RED = pygame.Color(255, 0, 0)  # Define the RED color constant

    background = pygame.image.load('bkg.png').convert()
    background = pygame.transform.scale(background, (BOARD_SIZE * TILE_SIZE, BOARD_SIZE * TILE_SIZE))

    screen = pygame.display.set_mode((BOARD_SIZE * TILE_SIZE, BOARD_SIZE * TILE_SIZE + BUTTON_HEIGHT + 10))
    pygame.display.set_caption('Troop Arrangement')
    
    # Initial game state with some pieces for the human player, arranged in a 2D list format
    human_pieces = [
        [Piece(2, "Human"), Piece(2, "Human"), Piece(2, "Human"), Piece(2, "Human"),
         Piece(2, "Human"), Piece(2, "Human"), Piece(3, "Human"), Piece(3, "Human")],
        [Piece(5, "Human"), Piece(6, "Human"), Piece(4, "Human"), Piece('4', "Human"),
         Piece(1, "Human"), Piece('F', "Human"), Piece('B', "Human"), Piece('B',"Human")],
    ] + [[None] * BOARD_SIZE for _ in range(BOARD_SIZE - 2)]

    dragged_piece = None
    drag_pos = None
    is_dragging = False
    running = True
    screen_width = BOARD_SIZE * TILE_SIZE
    screen_height = BOARD_SIZE * TILE_SIZE + BUTTON_HEIGHT + 10
    
    done_button_rect = pygame.Rect((screen_width * 3 // 4 - BUTTON_WIDTH // 2, screen_height - BUTTON_HEIGHT - 5, BUTTON_WIDTH, BUTTON_HEIGHT))

    while running:
        # First, fill the screen with the specified color
        screen.fill(pygame.Color(240,240,240))

        # Then, draw the background image on top of the colored screen
        screen.blit(background, (0, 0))

        # Draw the board and pieces
        font = pygame.font.Font(None, 36)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = human_pieces[row][col]
                if piece:
                    piece_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    piece_surface.set_alpha(200)  # Set transparency level (0-255)
                    piece_surface.fill(RED)  # Use the RED color constant
                    screen.blit(piece_surface, (col * TILE_SIZE, row * TILE_SIZE))

                    # Render and display the rank text
                    text_surface = font.render(str(piece.rank), True, pygame.Color("white"))
                    screen.blit(text_surface, (col * TILE_SIZE + 20, row * TILE_SIZE + 10))

        # Draw grid lines on top of the pieces
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                pygame.draw.rect(screen, pygame.Color(150,130,60),
                                 (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

        # Draw the dragged piece
        if dragged_piece:
            piece_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            piece_surface.set_alpha(150)
            piece_surface.fill(RED)  # Use the RED color constant
            screen.blit(piece_surface, drag_pos)
            text_surface = font.render(str(dragged_piece.rank), True, pygame.Color("white"))
            screen.blit(text_surface, (drag_pos[0] + 20, drag_pos[1] + 10))

        # Draw the bottom UI text and button
        font = pygame.font.Font(None, 30)
        text = "Position your Forces!"
        text_surface = font.render(text, True, pygame.Color("black"))
        text_x = screen_width // 4 - text_surface.get_width() // 2
        text_y = screen_height - BUTTON_HEIGHT - 10
        screen.blit(text_surface, (text_x, text_y + 10))
        draw_button(screen, "Onward", pygame.Color("gray"), pygame.Color("black"), done_button_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_clicked(done_button_rect):
                    running = False  # Exit the loop if "Done" is clicked
                else:
                    x, y = mouse_pos
                    col, row = x // TILE_SIZE, y // TILE_SIZE
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and human_pieces[row][col]:
                        dragged_piece = human_pieces[row][col]
                        human_pieces[row][col] = None
                        is_dragging = True
                        drag_pos = mouse_pos
            elif event.type == pygame.MOUSEMOTION and is_dragging:
                drag_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and is_dragging:
                x, y = pygame.mouse.get_pos()
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and human_pieces[row][col] is None:
                    human_pieces[row][col] = dragged_piece
                dragged_piece = None
                is_dragging = False

        pygame.display.flip()

    return human_pieces  # Return the final 2D board configuration


def play_screen():
    pygame.init()

    # Set the window size (use appropriate dimensions for your game)
    screen = pygame.display.set_mode((600, 400))  # Adjust size to fit your background image
    pygame.display.set_caption("Stratego Game")

    # Load background image for the play screen
    background_image = pygame.image.load('play5.png').convert()  # Replace with your image path
    background_image = pygame.transform.scale(background_image, (600, 400))  # Scale the background image

    # Set up the "Begin" button
    font = pygame.font.Font(None, 36)
    begin_button_text = font.render("BEGIN", True, (0, 0, 0))  # Black text for the Begin button
    begin_button_rect = begin_button_text.get_rect()  # Create a rect for text sizing

    # Create a grey background for the "Begin" button, with padding
    button_width = begin_button_rect.width + 40
    button_height = begin_button_rect.height + 20
    begin_button_bg = pygame.Surface((button_width, button_height))
    begin_button_bg.fill((240,240,240))  # Grey color for the button

    # Position the button at bottom-right corner, centered text
    button_x = 540 - button_width // 2
    button_y = 370 - button_height // 2
    begin_button_rect.center = (button_x + button_width // 2, button_y + button_height // 2)

    # Draw the background and button
    screen.blit(background_image, (0, 0))  # Blit the background image
    screen.blit(begin_button_bg, (button_x, button_y))  # Blit the grey background for the button
    screen.blit(begin_button_text, begin_button_rect)  # Center the text on the button

    pygame.display.flip()

    # Event handling loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click was inside the "Begin" button area
                if pygame.Rect(button_x, button_y, button_width, button_height).collidepoint(event.pos):
                    return  # Proceed to the arrange_troops screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Allow quitting with ESC key
                    pygame.quit()
                    sys.exit()
