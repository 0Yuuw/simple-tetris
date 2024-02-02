import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
GRID_SIZE = 30
BOARD_WIDTH, BOARD_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
FPS = 8

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SHAPES_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128)]

# Define game variables
board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
current_shape = None
current_shape_pos = [0, 0]
score = 0

# Font setup
font = pygame.font.Font(None, 36)

# Function to draw the board
def draw_board(screen):
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            if board[row][col] != 0:
                pygame.draw.rect(screen, SHAPES_COLORS[board[row][col] - 1],
                                 (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
                pygame.draw.rect(screen, WHITE, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

# Function to draw the current shape
def draw_current_shape(screen):
    if current_shape is not None:
        shape_color = SHAPES_COLORS[SHAPES.index(current_shape)]
        for row in range(len(current_shape)):
            for col in range(len(current_shape[row])):
                if current_shape[row][col] == 1:
                    pygame.draw.rect(screen, shape_color,
                                     ((current_shape_pos[1] + col) * GRID_SIZE, (current_shape_pos[0] + row) * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE), 0)
                    pygame.draw.rect(screen, WHITE,
                                     ((current_shape_pos[1] + col) * GRID_SIZE, (current_shape_pos[0] + row) * GRID_SIZE,
                                      GRID_SIZE, GRID_SIZE), 1)

# Function to check if the current shape can be placed at the specified position
def is_valid_position():
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if current_shape[row][col] == 1:
                if current_shape_pos[0] + row >= BOARD_HEIGHT or current_shape_pos[1] + col < 0 or \
                        current_shape_pos[1] + col >= BOARD_WIDTH or board[current_shape_pos[0] + row][
                    current_shape_pos[1] + col] != 0:
                    return False
    return True

# Function to place the current shape on the board
def place_shape():
    global current_shape_pos, current_shape, score, board
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if current_shape[row][col] == 1:
                board[current_shape_pos[0] + row][current_shape_pos[1] + col] = SHAPES.index(current_shape) + 1

    # Clear lines on the board
    lines_cleared = 0
    for row in range(BOARD_HEIGHT):
        if all(board[row]):
            del board[row]
            board.insert(0, [0] * BOARD_WIDTH)
            lines_cleared += 1

    # Update the score based on lines cleared
    if lines_cleared == 1:
        score += 40
    elif lines_cleared == 2:
        score += 100
    elif lines_cleared == 3:
        score += 300
    elif lines_cleared == 4:
        score += 1200

    current_shape_pos = [0, BOARD_WIDTH // 2]
    current_shape = random.choice(SHAPES)
    if not is_valid_position():
        end_game()

# Function to handle the end of the game
def end_game():
    global game_over
    game_over = True

# Function to draw text on the screen
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Initialize game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

running = True
start_screen = True
game_over = False
current_shape = random.choice(SHAPES)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if start_screen:
        # Draw Start Screen
        screen.fill(BLACK)
        draw_text("Tetris", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text("Press SPACE to start", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Press ESC to exit", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)

        if keys[pygame.K_SPACE]:
            start_screen = False

    elif not game_over:
        # Game logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if keys[pygame.K_LEFT]:
            current_shape_pos[1] -= 1
            if not is_valid_position():
                current_shape_pos[1] += 1
        if keys[pygame.K_RIGHT]:
            current_shape_pos[1] += 1
            if not is_valid_position():
                current_shape_pos[1] -= 1
        if keys[pygame.K_DOWN]:
            current_shape_pos[0] += 1
            if not is_valid_position():
                current_shape_pos[0] -= 1
                place_shape()

        # Move the shape down automatically
        current_shape_pos[0] += 1
        if not is_valid_position():
            current_shape_pos[0] -= 1
            place_shape()

        # Draw everything
        screen.fill(BLACK)
        draw_board(screen)
        draw_current_shape(screen)

    else:
        # Draw End Screen
        screen.fill(BLACK)
        draw_text("Game Over", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text("Score: {}".format(score), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Press R to restart", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
        draw_text("Press ESC to exit", WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.3)

        if keys[pygame.K_r]:
            # Reset the game state
            game_over = False
            current_shape_pos = [0, BOARD_WIDTH // 2]
            current_shape = random.choice(SHAPES)
            score = 0
            board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

        elif keys[pygame.K_ESCAPE]:
            running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
quit()
