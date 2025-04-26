import pygame 
import random


pygame.init()

# Game window
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Get home kitty!")

# Colors will remove once everything is done 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Loading in sprite sheet!
SPRITE_SHEET = pygame.image.load("Kitty.png").convert_alpha()


#  New Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
FRAME_COUNT = 4 # 4 frames in walk cycle
ANIMATION_SPEED = 5 # might change based on everything else
PLAYER_JUMP = -15
GRAVITY = 1

PLAYER_FRAMES = []
for i in range(FRAME_COUNT):
    frame = SPRITE_SHEET.subsurface(
        (i * PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
    )
    PLAYER_FRAMES.append(frame)

# Obstacle settings
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 30, 50
OBSTACLE_SPEED = 7

class Player:
    def __init__(self):
        self.frames = PLAYER_FRAMES
        self.current_frame = 0
        self.animation_counter = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, HEIGHT - PLAYER_HEIGHT - 10)
        self.velocity = 0
        self.on_ground = True

    def updated_animation(self):  #animated while on ground
        if self.on_ground:
            self.animation_counter += 1
            if self.animation_counter >= ANIMATION_SPEED:
                self.animation_counter = 0
                self.current_frame = (self.current_frame + 1) % FRAME_COUNT
                self.image = self.frames[self.current_frame]
        

    def jump(self):
        if self.on_ground:
            self.velocity = PLAYER_JUMP
            self.on_ground = False
            self.current_frame = 0
            self.image = self.frames[self.current_frame]

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        if self.rect.bottom >= HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
            self.on_ground = True
            self.velocity = 0
        

        self.updated_animation()
class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH, HEIGHT - OBSTACLE_HEIGHT - 10, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        self.active = True
        self.passed = False  # Tracks if obstacle was passed

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.active = False

def main():
    clock = pygame.time.Clock()
    fps = 60

    player = Player()
    obstacles = []
    spawn_timer = 0
    score = 0

    running = True
    while running:
        clock.tick(fps)
        spawn_timer += 1  # <-- Indent everything under the loop!

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Spawn obstacles every 60 frames (~1 second at 60 FPS)
        if spawn_timer >= 60:
            obstacles.append(Obstacle())
            spawn_timer = 0  # Reset timer

        # Update player and obstacles
        player.update()
        for obstacle in obstacles:
            obstacle.update()

        # Check collisions
        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.rect):
                running = False  # End game on collision

        # Update score when passing obstacles
        for obstacle in obstacles:
            if not obstacle.passed and obstacle.rect.right < player.rect.left:
                score += 1
                obstacle.passed = True

        # Remove off-screen obstacles
        obstacles = [obs for obs in obstacles if obs.active]

        # Draw everything
        WIN.fill(WHITE)
        pygame.draw.rect(WIN, BLACK, (0, HEIGHT-10, WIDTH, 10))  # Ground
        WIN.blit(player.image, player.rect)  # Player

        for obstacle in obstacles:
            pygame.draw.rect(WIN, BLACK, obstacle.rect)

        # Draw score text
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        WIN.blit(text, (10, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()