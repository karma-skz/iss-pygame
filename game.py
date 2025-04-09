import pygame
import random
import os

pygame.init()

# Use the user's screen resolution
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

# Set fullscreen mode
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Phineas and Isabella Game")

# Font for displaying text
font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 72)

# Load background image
try:
    background_image = pygame.image.load(os.path.join("assets", "images", "background.jpg"))
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except:
    background_image = None

# List of available characters
character_list = [
    {"name": "Phineas", "file": "phineas.png", "color": (0, 255, 0)},
    {"name": "Ferb", "file": "ferb.png", "color": (0, 0, 255)},
    {"name": "Isabella", "file": "isabella.png", "color": (255, 105, 180)},
    {"name": "Candace", "file": "candace.png", "color": (255, 0, 0)},
    {"name": "Perry", "file": "perry.png", "color": (0, 200, 200)},
]

def select_characters():
    # Draw background first
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((0, 0, 0))
    
    # Add a semi-transparent overlay for better text visibility
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    title = title_font.render("Select Your Characters", True, (255, 255, 255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//8))
    
    instructions1 = font.render("Player 1: Use LEFT/RIGHT arrows to select, ENTER to confirm", True, (255, 255, 255))
    instructions2 = font.render("Player 2: Use A/D keys to select, SPACE to confirm", True, (255, 255, 255))
    
    screen.blit(instructions1, (WIDTH//2 - instructions1.get_width()//2, HEIGHT//4))
    screen.blit(instructions2, (WIDTH//2 - instructions2.get_width()//2, HEIGHT//4 + 40))
    
    # Load all character images
    character_images = []
    for char in character_list:
        try:
            img = pygame.image.load(os.path.join("assets", "images", char["file"]))
            # Scale all images to same height
            scale_ratio = 100 / img.get_height()
            img = pygame.transform.scale(img, (int(img.get_width() * scale_ratio), 100))
            character_images.append(img)
        except:
            # Use a placeholder if image not found
            placeholder = pygame.Surface((50, 100))
            placeholder.fill(char["color"])
            character_images.append(placeholder)
    
    player1_selection = 0
    player2_selection = 1  # Default to different character
    
    player1_confirmed = False
    player2_confirmed = False
    
    while not (player1_confirmed and player2_confirmed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            
            if event.type == pygame.KEYDOWN:
                # Player 1 controls
                if not player1_confirmed:
                    if event.key == pygame.K_LEFT:
                        player1_selection = (player1_selection - 1) % len(character_list)
                        # Ensure players don't select same character
                        if player1_selection == player2_selection:
                            player1_selection = (player1_selection - 1) % len(character_list)
                    elif event.key == pygame.K_RIGHT:
                        player1_selection = (player1_selection + 1) % len(character_list)
                        if player1_selection == player2_selection:
                            player1_selection = (player1_selection + 1) % len(character_list)
                    elif event.key == pygame.K_RETURN:
                        player1_confirmed = True
                
                # Player 2 controls
                if not player2_confirmed:
                    if event.key == pygame.K_a:
                        player2_selection = (player2_selection - 1) % len(character_list)
                        if player2_selection == player1_selection:
                            player2_selection = (player2_selection - 1) % len(character_list)
                    elif event.key == pygame.K_d:
                        player2_selection = (player2_selection + 1) % len(character_list)
                        if player2_selection == player1_selection:
                            player2_selection = (player2_selection + 1) % len(character_list)
                    elif event.key == pygame.K_SPACE:
                        player2_confirmed = True
                
                if event.key == pygame.K_ESCAPE:
                    return None, None
        
        # Clear the selection area
        selection_rect = pygame.Rect(0, HEIGHT//2, WIDTH, HEIGHT//2)
        pygame.draw.rect(screen, (0, 0, 0), selection_rect)
        
        # Display character options
        spacing = WIDTH // (len(character_list) + 1)
        for i, (char, img) in enumerate(zip(character_list, character_images)):
            x_pos = (i + 1) * spacing - img.get_width()//2
            
            # Highlight selected characters
            if i == player1_selection or i == player2_selection:
                pygame.draw.rect(screen, (50, 50, 50), 
                                (x_pos - 10, HEIGHT//2 - 10, 
                                img.get_width() + 20, img.get_height() + 60))
            
            # Draw character image
            screen.blit(img, (x_pos, HEIGHT//2))
            
            # Draw character name
            name_text = font.render(char["name"], True, char["color"])
            screen.blit(name_text, (x_pos + img.get_width()//2 - name_text.get_width()//2, 
                                  HEIGHT//2 + img.get_height() + 10))
            
            # Mark confirmed selection
            if i == player1_selection and player1_confirmed:
                confirm_text = font.render("Player 1", True, (255, 255, 0))
                screen.blit(confirm_text, (x_pos + img.get_width()//2 - confirm_text.get_width()//2, 
                                        HEIGHT//2 + img.get_height() + 40))
            
            if i == player2_selection and player2_confirmed:
                confirm_text = font.render("Player 2", True, (255, 255, 0))
                screen.blit(confirm_text, (x_pos + img.get_width()//2 - confirm_text.get_width()//2, 
                                        HEIGHT//2 + img.get_height() + 40))
        
        pygame.display.flip()
    
    return character_list[player1_selection], character_list[player2_selection]

def show_home_screen(winner=None):
    # Draw background first
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((0, 0, 0))
    
    # Add a semi-transparent overlay for better text visibility
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    # Display title
    title = font.render("Phineas and Isabella Game", True, (255, 255, 255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
    
    # Display winner if game ended
    if winner:
        winner_text = font.render(f"{winner} wins!", True, (255, 255, 0))
        screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2, HEIGHT//3))
    
    # Display instructions
    instructions = font.render("Press ENTER to start game", True, (255, 255, 255))
    screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT//2))
    
    pygame.display.flip()
    
    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    return False
    return True

def game_loop(player1_char, player2_char):
    # Load images
    try:
        player1_image = pygame.image.load(os.path.join("assets", "images", player1_char["file"]))
    except:
        player1_image = pygame.Surface((50, 100))
        player1_image.fill(player1_char["color"])
    
    try:
        player2_image = pygame.image.load(os.path.join("assets", "images", player2_char["file"]))
    except:
        player2_image = pygame.Surface((50, 100))
        player2_image.fill(player2_char["color"])

    # Scale players to similar size if needed
    target_height = 100
    p1_scale = target_height / player1_image.get_height()
    p2_scale = target_height / player2_image.get_height()
    
    player1_image = pygame.transform.scale(player1_image, 
                                         (int(player1_image.get_width() * p1_scale), 
                                          target_height))
    
    player2_image = pygame.transform.scale(player2_image, 
                                         (int(player2_image.get_width() * p2_scale), 
                                          target_height))
    
    # Store original images for flipping
    player1_image_right = player1_image
    player1_image_left = pygame.transform.flip(player1_image, True, False)
    player2_image_right = player2_image
    player2_image_left = pygame.transform.flip(player2_image, True, False)
    
    # Default facing directions
    player1_facing_right = True
    player2_facing_right = False

    p_width = player1_image.get_width()
    p_height = player1_image.get_height()
    
    i_width = player2_image.get_width()
    i_height = player2_image.get_height()

    player1_x = 0
    player1_y = 0
    player1_vx = 20
    player1_vy = 0
    player1_can_jump = True
    player1_jump_cooldown = 0

    # Add player2's position and velocity
    player2_x = WIDTH - i_width
    player2_y = 0
    player2_vx = 20
    player2_vy = 0
    player2_can_jump = True
    player2_jump_cooldown = 0

    gravity = 900  # Increased for more realistic physics
    jump_force = -600  # Stronger jump
    jump_cooldown_time = 0.3  # Can't jump again for this many seconds

    clock = pygame.time.Clock()

    # Separate rectangle colors by player
    player1_rects = []
    player2_rects = []

    # Separate scores for both players
    player1_score = 0
    player2_score = 0
    
    running = True
    while running:
        dt = clock.tick(60) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return None

        keys = pygame.key.get_pressed()

        # Player 1 - store old position for collision detection
        old_player1_x = player1_x

        # Player 1 controls (arrow keys + space)
        if keys[pygame.K_SPACE] and player1_can_jump:
            player1_vy = jump_force
            player1_can_jump = False
            player1_jump_cooldown = jump_cooldown_time

        if keys[pygame.K_RIGHT]:
            player1_x += player1_vx
            player1_facing_right = True
        if keys[pygame.K_LEFT]:
            player1_x -= player1_vx
            player1_facing_right = False
        
        # Player 2 - store old position for collision detection
        old_player2_x = player2_x
        
        # Player 2 controls (WASD)
        if keys[pygame.K_w] and player2_can_jump:
            player2_vy = jump_force
            player2_can_jump = False
            player2_jump_cooldown = jump_cooldown_time
        
        if keys[pygame.K_d]:
            player2_x += player2_vx
            player2_facing_right = True
        if keys[pygame.K_a]:
            player2_x -= player2_vx
            player2_facing_right = False

        screen.fill((0, 0, 0))

        # Update jump cooldowns
        if not player1_can_jump:
            player1_jump_cooldown -= dt
            if player1_jump_cooldown <= 0:
                player1_can_jump = True
            
        if not player2_can_jump:
            player2_jump_cooldown -= dt
            if player2_jump_cooldown <= 0:
                player2_can_jump = True

        # Spawn rectangles for Player 1 - decreased frequency
        if random.randint(0, 2000) > 1950:  # Changed from 1897 to 1950
            player1_rects.append(pygame.rect.Rect(WIDTH, random.randint(0, HEIGHT), 10, 100))
        
        # Spawn rectangles for Player 2 - decreased frequency
        if random.randint(0, 2000) > 1950:  # Changed from 1897 to 1950
            player2_rects.append(pygame.rect.Rect(WIDTH, random.randint(0, HEIGHT), 10, 100))
        
        # Draw and move player 1's rectangles
        for rect in player1_rects[:]:
            pygame.draw.rect(screen, player1_char["color"], rect)
            rect.x -= 5
            
            # Remove rectangles that are off screen
            if rect.right < 0:
                player1_rects.remove(rect)
        
        # Draw and move player 2's rectangles
        for rect in player2_rects[:]:
            pygame.draw.rect(screen, player2_char["color"], rect)
            rect.x -= 5
            
            # Remove rectangles that are off screen
            if rect.right < 0:
                player2_rects.remove(rect)

        # Create player rectangles for collision detection
        player1_rect = pygame.rect.Rect(player1_x, player1_y, p_width, p_height)
        player2_rect = pygame.rect.Rect(player2_x, player2_y, i_width, i_height)
        
        # Check for collision between players
        if player1_rect.colliderect(player2_rect):
            # Revert to old positions to prevent overlap
            player1_x = old_player1_x
            player2_x = old_player2_x
            
            # Recreate the rectangles with the updated positions
            player1_rect = pygame.rect.Rect(player1_x, player1_y, p_width, p_height)
            player2_rect = pygame.rect.Rect(player2_x, player2_y, i_width, i_height)

        # Check Player 1 collisions with rectangles
        for rect in player1_rects[:]:
            if player1_rect.colliderect(rect):
                player1_rects.remove(rect)
                player1_score += 1
        
        # Check Player 2 collisions
        for rect in player2_rects[:]:
            if player2_rect.colliderect(rect):
                player2_rects.remove(rect)
                player2_score += 1

        # Choose the correct image based on direction
        current_player1_image = player1_image_right if player1_facing_right else player1_image_left
        current_player2_image = player2_image_right if player2_facing_right else player2_image_left
        
        # Draw players with correct orientation
        screen.blit(current_player1_image, (player1_x, player1_y))
        screen.blit(current_player2_image, (player2_x, player2_y))

        # Update Player 1 physics with more realistic jump
        player1_vy += gravity * dt
        player1_y += player1_vy * dt

        # Ground collision for Player 1
        if player1_y > HEIGHT - p_height:
            player1_y = HEIGHT - p_height
            player1_vy = 0
            player1_can_jump = True  # Can jump when on ground
            
        # Ceiling collision for Player 1
        if player1_y < 0:
            player1_y = 0
            player1_vy = 0
        
        # Update Player 2 physics
        player2_vy += gravity * dt
        player2_y += player2_vy * dt

        # Ground collision for Player 2
        if player2_y > HEIGHT - i_height:
            player2_y = HEIGHT - i_height
            player2_vy = 0
            player2_can_jump = True  # Can jump when on ground
            
        # Ceiling collision for Player 2
        if player2_y < 0:
            player2_y = 0
            player2_vy = 0
        
        # Keep characters within screen bounds horizontally
        player1_x = max(0, min(player1_x, WIDTH - p_width))
        player2_x = max(0, min(player2_x, WIDTH - i_width))

        # Display scores during gameplay
        player1_score_text = font.render(f"{player1_char['name']}: {player1_score}", True, player1_char["color"])
        player2_score_text = font.render(f"{player2_char['name']}: {player2_score}", True, player2_char["color"])
        
        screen.blit(player1_score_text, (10, 10))
        screen.blit(player2_score_text, (WIDTH - player2_score_text.get_width() - 10, 10))

        pygame.display.flip()
        
        # Check if any player reached 50 points
        if player1_score >= 50:
            return player1_char["name"]
        if player2_score >= 50:
            return player2_char["name"]

    return None

# Main game loop
running = True
winner = None

while running:
    # Show home screen
    if not show_home_screen(winner):
        running = False
        break
    
    # Select characters
    player1_char, player2_char = select_characters()
    if player1_char is None or player2_char is None:
        running = False
        break
    
    # Run the game
    winner = game_loop(player1_char, player2_char)
    
    if winner is None:
        running = False

print("Game exited")
pygame.quit()