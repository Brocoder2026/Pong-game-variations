# DEPENDENCIES
import pygame as pyg

# ///// MODE INPUT BEFORE WINDOW LAUNCH /////
print("=== WELCOME TO PONG ===")
print("Select Game Mode:")
print("1: 2 Player Local (2P)")
print("2: Player vs CPU (CPU)")
print("3: Player vs THE WALL (WALL)")

mode_choice = input("Enter choice (1, 2, or 3): ").strip()

# Default to 2P if they enter something invalid
game_mode = "2P"
if mode_choice == "2":
    game_mode = "CPU"
elif mode_choice == "3":
    game_mode = "WALL"

print(f"Launching {game_mode} mode...")

# ///// NOW INITIALIZE PYGAME SAFELY /////
pyg.init()

WIDTH = 800
HEIGHT = 600
screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption(f"PONG - Mode: {game_mode}")
clock = pyg.time.Clock()

running = True
speed = 8

player = pyg.Rect(10, 200, 25, 100)
opponent = pyg.Rect(WIDTH - 35, 200, 25, 100)
ball = pyg.Rect(400, 300, 25, 25)

ball_speed_x = 5
ball_speed_y = 5

player_score = 0
opponent_score = 0
winner = None

# CPU Configuration
cpu_speed = 6 

# ADJUST FOR THE WALL MODE
if game_mode == "WALL":
    opponent.y = 0
    opponent.height = HEIGHT  # The paddle becomes the literal wall

font = pyg.font.Font(None, 60)
win_font = pyg.font.Font(None, 160)

# ///// GAME LOOP /////
while running:
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
            
    if winner is None:
        # ///// CONTROLS & AI LOGIC /////
        keys = pyg.key.get_pressed()
        
        # Player 1 (Always Active)
        if keys[pyg.K_w]: player.y -= speed
        if keys[pyg.K_s]: player.y += speed

        # Mode Checks
        if game_mode == "2P":
            if keys[pyg.K_UP]: opponent.y -= speed
            if keys[pyg.K_DOWN]: opponent.y += speed
        elif game_mode == "CPU":
            # Smooth tracking AI
            if opponent.centery < ball.centery:
                opponent.y += cpu_speed
            elif opponent.centery > ball.centery:
                opponent.y -= cpu_speed

        # ///// BOUNDARIES /////
        if player.top < 0: player.top = 0
        if player.bottom > HEIGHT: player.bottom = HEIGHT
        
        if game_mode != "WALL": 
            if opponent.top < 0: opponent.top = 0
            if opponent.bottom > HEIGHT: opponent.bottom = HEIGHT

        # ///// BALL MOVEMENT /////
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # ///// TOP / BOTTOM COLLISION /////
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y = -ball_speed_y

        # ///// SCORING /////
        if ball.left <= 0:
            opponent_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x = 5
        if ball.right >= WIDTH:
            player_score += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            ball_speed_x = -5

        # ///// PADDLE COLLISION /////
        if player.colliderect(ball):
            ball_speed_x = -ball_speed_x
            
        if opponent.colliderect(ball):
            ball_speed_x = -ball_speed_x
            if game_mode == "WALL":
                ball_speed_x -= 1  # Continuous acceleration wall mechanic!

        # ///// WINNER CAPS /////
        if player_score >= 20:
            winner = "PLAYER 1 WINS!"
        if opponent_score >= 20:
            winner = "GAME OVER" if game_mode in ["CPU", "WALL"] else "PLAYER 2 WINS!"

    # ///// DRAW /////
    screen.fill((30, 60, 60))

    if winner:
        win_text = win_font.render(winner, True, (255, 255, 255))
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))
    else:
        score_text = font.render(f"{player_score}   {opponent_score}", True, (255, 255, 255))
        screen.blit(score_text, (350, 30))

        pyg.draw.rect(screen, (0, 255, 255), player)
        
        opp_color = (255, 0, 50) if game_mode == "WALL" else (0, 5, 255)
        pyg.draw.rect(screen, opp_color, opponent)
        
        pyg.draw.rect(screen, (255, 255, 255), ball)

    pyg.display.flip()
    clock.tick(60)

pyg.quit()
