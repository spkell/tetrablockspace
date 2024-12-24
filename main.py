import pygame
import sys
import json
from typing import List, Tuple
from datetime import datetime
from pathlib import Path
import re  # Add this to the imports at the top

from components.text import ShowGoal, ShowPosition, ShowInstructions

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT_COLOR = (50, 50, 50)
GOAL_COLOR = (0, 255, 0)  # Green

# Block size and grid dimensions
BLOCK_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 10

# At the top of the file, add these constants
PLANES = {
    'XY': {'dims': (0, 1), 'fixed': (2, 3)},  # dims = moving dims, fixed = static dims
    'XZ': {'dims': (0, 2), 'fixed': (1, 3)},
    'XT': {'dims': (0, 3), 'fixed': (1, 2)},
    'YZ': {'dims': (1, 2), 'fixed': (0, 3)},
    'YT': {'dims': (1, 3), 'fixed': (0, 2)},
    'ZT': {'dims': (2, 3), 'fixed': (0, 1)}
}

WALL_COLOR = BLACK
PATH_COLOR = WHITE
PLAYER_COLOR = RED

# Add after pygame.init()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24) # Add a smaller font for instructions

# Add after other constants
LEADERBOARD_FILE = 'leaderboard.json'

# Add these color constants after the other color definitions
DIM_COLORS = {
    'X': (255, 0, 0),    # Red
    'Y': (0, 255, 0),    # Green
    'Z': (0, 0, 255),    # Blue
    'T': (200, 200, 0)   # Yellow
}

# Add these constants near the top with other constants
MENU_SCROLL_SPEED = 20  # Pixels per scroll
LEVELS_PER_PAGE = 8
BUTTON_HEIGHT = 80


def load_level(filename: str) -> dict:
    """Load level data from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)


def is_valid_position(pos: List[int], walls: List[List[int]]) -> bool:
    """Check if a 4D position is valid (not a wall)."""
    return tuple(pos) not in set(tuple(wall) for wall in walls)


def initialize_game(level_data):
    """Initialize game state from level data"""
    walls = level_data['walls']
    start_pos = level_data['start']
    goal_pos = level_data['goal']
    DIMENSION_SIZE = level_data['size']  # Get size from level data
    
    # Initialize MAZE with the correct dimensions from level data
    MAZE = [[[[0 for t in range(DIMENSION_SIZE)]
              for z in range(DIMENSION_SIZE)]
             for y in range(DIMENSION_SIZE)]
            for x in range(DIMENSION_SIZE)]
    return walls, start_pos, goal_pos, DIMENSION_SIZE, MAZE


# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("4D Maze Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()


def draw_maze(player_pos, walls, goal_pos, DIMENSION_SIZE, current_plane, steps_taken, show_instructions):
    """Draw the current 2D plane of the maze."""
    screen.fill(WHITE)
    
    # Calculate the maximum space available for the maze
    TOP_MARGIN = 100  # Space for text at top
    BOTTOM_MARGIN = 50  # Space for text at bottom
    available_height = SCREEN_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    available_width = SCREEN_WIDTH - 40  # 20px margin on each side
    
    # Calculate block size based on available space and grid dimensions
    BLOCK_SIZE = min(
        available_width // DIMENSION_SIZE,
        available_height // DIMENSION_SIZE
    )
    
    # Calculate starting position to center the maze
    start_x = (SCREEN_WIDTH - (BLOCK_SIZE * DIMENSION_SIZE)) // 2
    start_y = TOP_MARGIN

    ShowGoal(font, FONT_COLOR, DIM_COLORS, goal_pos, screen)
    ShowPosition(font, FONT_COLOR, player_pos, screen, DIM_COLORS, current_plane)
    
    
    # Check win condition
    if player_pos == goal_pos:
        win_text = f"YOU WIN! Steps taken: {steps_taken}"
        win_surface = font.render(win_text, True, (0, 255, 0))
        text_rect = win_surface.get_rect(center=(SCREEN_WIDTH/2, 50))
        screen.blit(win_surface, text_rect)
    
    moving_dims = PLANES[current_plane]['dims']
    fixed_dims = PLANES[current_plane]['fixed']
    
    # Map dimension indices to XYZT
    dim_map = {0: 'X', 1: 'Y', 2: 'Z', 3: 'T'}
    
    # Get colors for horizontal and vertical borders based on current plane
    horiz_color = DIM_COLORS[dim_map[moving_dims[0]]]  # First dimension color
    vert_color = DIM_COLORS[dim_map[moving_dims[1]]]   # Second dimension color
    
    # Draw the colored borders
    border_thickness = 3
    # Horizontal borders (top and bottom)
    pygame.draw.rect(screen, horiz_color, 
        (start_x - border_thickness, 
         start_y - border_thickness,
         BLOCK_SIZE * DIMENSION_SIZE + border_thickness * 2,
         border_thickness))
    pygame.draw.rect(screen, horiz_color,
        (start_x - border_thickness,
         start_y + BLOCK_SIZE * DIMENSION_SIZE,
         BLOCK_SIZE * DIMENSION_SIZE + border_thickness * 2,
         border_thickness))
    
    # Vertical borders (left and right)
    pygame.draw.rect(screen, vert_color,
        (start_x - border_thickness,
         start_y - border_thickness,
         border_thickness,
         BLOCK_SIZE * DIMENSION_SIZE + border_thickness * 2))
    pygame.draw.rect(screen, vert_color,
        (start_x + BLOCK_SIZE * DIMENSION_SIZE,
         start_y - border_thickness,
         border_thickness,
         BLOCK_SIZE * DIMENSION_SIZE + border_thickness * 2))
    
    # Convert walls to a set for O(1) lookup instead of O(n)
    wall_set = set(tuple(wall) for wall in walls)
    
    # Draw grid
    for i in range(DIMENSION_SIZE):
        for j in range(DIMENSION_SIZE):
            pos = [0, 0, 0, 0]
            pos[moving_dims[0]] = i
            pos[moving_dims[1]] = j
            pos[fixed_dims[0]] = player_pos[fixed_dims[0]]
            pos[fixed_dims[1]] = player_pos[fixed_dims[1]]
            
            # Calculate screen position using new start_x and start_y
            x = start_x + (i * BLOCK_SIZE)
            y = start_y + (j * BLOCK_SIZE)
            
            # Draw cell
            if pos == goal_pos:
                color = GOAL_COLOR
            else:
                color = PATH_COLOR if tuple(pos) not in wall_set else WALL_COLOR
            
            pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)
            
            # Draw player
            if pos == player_pos:
                pygame.draw.rect(screen, PLAYER_COLOR, 
                    (x + BLOCK_SIZE//4, y + BLOCK_SIZE//4, 
                     BLOCK_SIZE//2, BLOCK_SIZE//2))

    # Add steps counter to the display
    steps_text = f"Steps: {steps_taken}"
    steps_surface = font.render(steps_text, True, FONT_COLOR)
    screen.blit(steps_surface, (SCREEN_WIDTH - 150, 10))

    # Draw instructions popup if requested
    if show_instructions:
        ShowInstructions(pygame,SCREEN_WIDTH, SCREEN_HEIGHT, screen, font, FONT_COLOR, WHITE, BLACK, small_font)

    return


def move_player(player_pos, steps_taken, direction, current_plane, DIMENSION_SIZE, walls):
    """Move the player within the current 2D plane."""

    (dh, dv) = direction
    moving_dims = PLANES[current_plane]['dims']
    
    # Apply movement to the correct dimensions based on current plane
    new_pos = player_pos.copy()
    new_pos[moving_dims[0]] += dh
    new_pos[moving_dims[1]] += dv
    
    # Check boundaries
    if all(0 <= new_pos[d] < DIMENSION_SIZE for d in moving_dims):
        # Check if the new position is valid in the maze
        if is_valid_position(new_pos, walls):
            player_pos = new_pos
            steps_taken += 1  # Increment steps when movement is successful
    return player_pos, steps_taken


def switch_plane(current_plane, new_plane):
    """Switch to a different 2D plane while maintaining position."""
    if new_plane in PLANES:
        current_plane = new_plane
    return current_plane


def load_leaderboard():
    """Load leaderboard from JSON file."""
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"levels": {}}  # Simple levels dictionary


def save_leaderboard(leaderboard):
    """Save leaderboard to JSON file."""
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=4)


def add_score(steps, level_id):
    """Add new score to leaderboard."""

    # Load and update leaderboard
    leaderboard = load_leaderboard()
    if level_id not in leaderboard["levels"]:
        leaderboard["levels"][level_id] = []

    top5 = leaderboard["levels"][level_id][:5]
    istop5 = any(steps < score["steps"] for score in top5) or len(top5) < 5

    # Get player name if theyre in the top 5
    if istop5:
        pygame.display.set_caption("Enter Your Name")
        name = ""
        name_entered = False
    
    
        while not name_entered:
            screen.fill(WHITE)
            text = font.render("Enter your name: " + name, True, BLACK)
            screen.blit(text, (SCREEN_WIDTH//4, SCREEN_HEIGHT//2))
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name:
                        name_entered = True
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 20 and event.unicode.isprintable():
                        name += event.unicode
    
        # Add new score
        leaderboard["levels"][level_id].append({
            "name": name,
            "steps": steps,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Sort and keep top 5 for this level
    leaderboard["levels"][level_id].sort(key=lambda x: x["steps"])
    leaderboard["levels"][level_id] = leaderboard["levels"][level_id][:5]
    
    save_leaderboard(leaderboard)
    return


def reset_game(start_pos):
    """Reset the game state."""
    player_pos = start_pos.copy()
    steps_taken = 0
    current_plane = 'XY'
    show_instructions = False  # Changed to False by default
    score_added = False
    return player_pos, steps_taken, current_plane, show_instructions, score_added


def show_leaderboard(leaderboard, level_id):
    """Display the leaderboard."""
    screen.fill(WHITE)
    
    title = font.render(f"Top 5 Scores - Level {level_id}", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH//4, 50))
    
    y = 120
    if level_id in leaderboard["levels"]:
        for i, score in enumerate(leaderboard["levels"][level_id], 1):
            text = f"{i}. {score['name']}: {score['steps']} steps - {score['date']}"
            score_text = font.render(text, True, BLACK)
            screen.blit(score_text, (50, y))
            y += 50
    
    restart_text = font.render("Press SPACE to play again", True, BLACK)
    screen.blit(restart_text, (SCREEN_WIDTH//4, SCREEN_HEIGHT - 100))
    pygame.display.flip()


def natural_sort_key(path):
    """Convert string with numbers into tuple of strings and integers for natural sorting."""
    parts = re.split('([0-9]+)', path.stem)
    return [int(part) if part.isdigit() else part.lower() for part in parts]


def draw_menu():
    """Draw the level selection menu with leaderboard info and scrolling support."""
    screen.fill(WHITE)
    title = font.render("4D Maze - Level Select", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH//4, 50))

    # Add scroll_offset as a static variable to track scrolling
    if not hasattr(draw_menu, 'scroll_offset'):
        draw_menu.scroll_offset = 0

    leaderboard = load_leaderboard()
    
    # Scan levels directory for available levels
    levels_path = Path("levels")
    level_files = sorted(levels_path.glob("*.json"), key=natural_sort_key)  # Natural sort by filename
    
    # Calculate maximum scroll offset
    max_scroll = max(0, (len(level_files) - LEVELS_PER_PAGE) * BUTTON_HEIGHT)
    draw_menu.scroll_offset = min(max_scroll, max(0, draw_menu.scroll_offset))

    # Create a clipping rectangle for the scrollable area
    scroll_area = pygame.Rect(0, 120, SCREEN_WIDTH, LEVELS_PER_PAGE * BUTTON_HEIGHT)
    screen.set_clip(scroll_area)

    y = 120 - draw_menu.scroll_offset
    
    for level_file in level_files:
        level_id = level_file.stem

        # Skip drawing if button is completely outside visible area
        if y + BUTTON_HEIGHT < 120 or y > 120 + (LEVELS_PER_PAGE * BUTTON_HEIGHT):
            y += BUTTON_HEIGHT
            continue

        # Load level data to get difficulty and size
        with open(level_file, 'r') as f:
            level_data = json.load(f)
        
        # Get top score if available
        top_score = "No scores yet"
        if level_id in leaderboard.get("levels", {}):
            if leaderboard["levels"][level_id]:
                top_player = leaderboard["levels"][level_id][0]
                top_score = f"Best: {top_player['name']} - {top_player['steps']} steps"
        
        # Draw level button and info
        button_rect = pygame.Rect(SCREEN_WIDTH//4, y, SCREEN_WIDTH//2, 60)
        pygame.draw.rect(screen, (200, 200, 200), button_rect)
        pygame.draw.rect(screen, BLACK, button_rect, 2)
        
        level_text = f"{level_id.replace('_', ' ').title()} - {level_data['size']}x{level_data['size']}x{level_data['size']}x{level_data['size']} - Difficulty: {level_data['difficulty']}"
        text = font.render(level_text, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH//4 + 10, y + 10))
        
        score_text = font.render(top_score, True, FONT_COLOR)
        screen.blit(score_text, (SCREEN_WIDTH//4 + 10, y + 35))
        
        y += BUTTON_HEIGHT

    # Reset clipping
    screen.set_clip(None)

    # Draw scroll indicators if needed
    if draw_menu.scroll_offset > 0:
        pygame.draw.polygon(screen, BLACK, [
            (SCREEN_WIDTH - 30, 100),
            (SCREEN_WIDTH - 20, 90),
            (SCREEN_WIDTH - 10, 100)
        ])
    if draw_menu.scroll_offset < max_scroll:
        pygame.draw.polygon(screen, BLACK, [
            (SCREEN_WIDTH - 30, SCREEN_HEIGHT - 20),
            (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 10),
            (SCREEN_WIDTH - 10, SCREEN_HEIGHT - 20)
        ])

    pygame.display.flip()
    return level_files, scroll_area


def main():
    running = True
    in_menu = True
    current_level = None
    score_added = False  # Track if the score has been added
    player_pos = None
    walls = None
    start_pos = None
    goal_pos = None
    DIMENSION_SIZE = None
    MAZE = None
    current_plane = 'XY'
    steps_taken = 0
    game_won = False
    show_instructions = False  # Initialize as False

    while running:
        if in_menu:
            screen.fill(WHITE)
            level_files, scroll_area = draw_menu()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    player_pos, steps_taken, current_plane, show_instructions, score_added = reset_game(start_pos)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mouse_pos = pygame.mouse.get_pos()
                        if scroll_area.collidepoint(mouse_pos):
                            # Adjust y position for scroll offset
                            adjusted_y = mouse_pos[1] + draw_menu.scroll_offset - 120
                            level_index = adjusted_y // BUTTON_HEIGHT
                            
                            if 0 <= level_index < len(level_files):
                                level_file = level_files[level_index]
                                level_data = load_level(level_file)
                                walls, start_pos, goal_pos, DIMENSION_SIZE, MAZE = initialize_game(level_data)
                                player_pos = start_pos.copy()
                                current_level = level_file.stem
                                in_menu = False
                                game_won = False
                                show_instructions = False
                    
                    elif event.button == 4:  # Mouse wheel up
                        draw_menu.scroll_offset = max(0, draw_menu.scroll_offset - MENU_SCROLL_SPEED)
                    elif event.button == 5:  # Mouse wheel down
                        draw_menu.scroll_offset += MENU_SCROLL_SPEED
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    player_pos, steps_taken, current_plane, show_instructions, score_added = reset_game(start_pos)
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # return to menu
                        in_menu = True
                        player_pos, steps_taken, current_plane, show_instructions, score_added = reset_game(start_pos)
                        
                    elif event.key == pygame.K_i:  # Toggle instructions with 'i' key
                        show_instructions = not show_instructions
                    
                    # Movement code (one block movement on key press)
                    if event.key == pygame.K_UP:
                        player_pos, steps_taken = move_player(player_pos, steps_taken, (0, -1), current_plane, DIMENSION_SIZE, walls)
                    if event.key == pygame.K_DOWN:
                        player_pos, steps_taken = move_player(player_pos, steps_taken, (0, 1), current_plane, DIMENSION_SIZE, walls)
                    if event.key == pygame.K_LEFT:
                        player_pos, steps_taken = move_player(player_pos, steps_taken, (-1, 0), current_plane, DIMENSION_SIZE, walls)
                    if event.key == pygame.K_RIGHT:
                        player_pos, steps_taken = move_player(player_pos, steps_taken, (1, 0), current_plane, DIMENSION_SIZE, walls)
                
            if not game_won:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_1]: current_plane = switch_plane(current_plane, 'XY')
                if keys[pygame.K_2]: current_plane = switch_plane(current_plane, 'XZ')
                if keys[pygame.K_3]: current_plane = switch_plane(current_plane, 'XT')
                if keys[pygame.K_4]: current_plane = switch_plane(current_plane, 'YZ')
                if keys[pygame.K_5]: current_plane = switch_plane(current_plane, 'YT')
                if keys[pygame.K_6]: current_plane = switch_plane(current_plane, 'ZT')
                
                # Check win condition and handle score/leaderboard display
                if player_pos == goal_pos:
                    game_won = True
                    add_score(steps_taken, current_level)
                    show_leaderboard(load_leaderboard(), current_level)
                else:
                    draw_maze(player_pos, walls, goal_pos, DIMENSION_SIZE, current_plane, steps_taken, show_instructions)

            if game_won:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    player_pos, steps_taken, current_plane, show_instructions, score_added = reset_game(start_pos)
                    game_won = False


        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()