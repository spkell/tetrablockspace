


def ShowGoal(font, FONT_COLOR, DIM_COLORS, goal_pos, screen):
    """Show the goal position in the top left corner of the screen"""
    
    # Add goal text at the top with different colors for each coordinate
    base_text = font.render("Goal: ", True, FONT_COLOR)
    x_text = font.render("X:" + str(goal_pos[0]), True, DIM_COLORS['X'])  # Red
    y_text = font.render(" Y:" + str(goal_pos[1]), True, DIM_COLORS['Y'])  # Green
    z_text = font.render(" Z:" + str(goal_pos[2]), True, DIM_COLORS['Z'])  # Blue
    t_text = font.render(" T:" + str(goal_pos[3]), True, DIM_COLORS['T'])  # Yellow

    # Calculate positions and blit each segment
    x_pos = 10
    y_pos = 10
    screen.blit(base_text, (x_pos, y_pos))
    x_pos += base_text.get_width()
    screen.blit(x_text, (x_pos, y_pos))
    x_pos += x_text.get_width()
    screen.blit(y_text, (x_pos, y_pos))
    x_pos += y_text.get_width()
    screen.blit(z_text, (x_pos, y_pos))
    x_pos += z_text.get_width()
    screen.blit(t_text, (x_pos, y_pos))


def ShowPosition(font, FONT_COLOR, player_pos, screen, DIM_COLORS, current_plane):
    """Show the player's position right under the goal position"""
    base_text = font.render("Pos: ", True, FONT_COLOR)
    x_text = font.render("X:" + str(player_pos[0]), True, DIM_COLORS['X'])  # Red
    y_text = font.render(" Y:" + str(player_pos[1]), True, DIM_COLORS['Y'])  # Green
    z_text = font.render(" Z:" + str(player_pos[2]), True, DIM_COLORS['Z'])  # Blue
    t_text = font.render(" T:" + str(player_pos[3]), True, DIM_COLORS['T'])  # Yellow
    plane_text = font.render(" | Plane:" + current_plane, True, FONT_COLOR)

    # Calculate positions and blit each segment
    x_pos = 10
    y_pos = 40  # Position below goal text
    screen.blit(base_text, (x_pos, y_pos))
    x_pos += base_text.get_width()
    screen.blit(x_text, (x_pos, y_pos))
    x_pos += x_text.get_width()
    screen.blit(y_text, (x_pos, y_pos))
    x_pos += y_text.get_width()
    screen.blit(z_text, (x_pos, y_pos))
    x_pos += z_text.get_width()
    screen.blit(t_text, (x_pos, y_pos))
    x_pos += t_text.get_width()
    screen.blit(plane_text, (x_pos, y_pos))




def ShowInstructions(pygame,SCREEN_WIDTH, SCREEN_HEIGHT, screen, font, FONT_COLOR, WHITE, BLACK, small_font):

        instructions_box = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(screen, WHITE, instructions_box, 0, 10)
        pygame.draw.rect(screen, BLACK, instructions_box, 2)

        instruction_text = [
            "Welcome to the 4D Maze!",
            "Use arrow keys to move.",
            "Use 1-6 to switch planes (XY, XZ, XT, YZ, YT, ZT).",
            "Find your way to the goal!",
            "Press 'i' to close this menu."
        ]

        y_offset = 0
        for line in instruction_text:
            text_surface = small_font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(instructions_box.centerx, instructions_box.centery + y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += 30

