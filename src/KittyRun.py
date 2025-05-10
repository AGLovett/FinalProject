import pygame 
import random


pygame.init()
#reminder use PISKEL for pxiel art 
# Game window
WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Get home kitty!")



# Loading in sprite sheet!
SPRITE_SHEET = pygame.image.load("Kitty.png").convert_alpha()

# loading in background !
BACKGROUND_IMG = pygame.image.load("background.png").convert()
# matching game height
BG_WIDTH = BACKGROUND_IMG.get_width()
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (BG_WIDTH, HEIGHT))

#loading ground image
GROUND_IMG = pygame.image.load("ground.png").convert_alpha()
GROUND_IMG = pygame.transform.scale(GROUND_IMG, (WIDTH, 10))
GROUND_HEIGHT = GROUND_IMG.get_height()


#loading obstacle imagies
OBSTACLE_IMAGES = [
    pygame.image.load("mailbox.png").convert_alpha(),
    pygame.image.load("trash.png").convert_alpha(),
    pygame.image.load("gnome.png").convert_alpha()
]

#  New Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
FRAME_COUNT = 4 # 4 frames in walk cycle
ANIMATION_SPEED = 3 # might change based on everything else
PLAYER_JUMP = -15
GRAVITY = 1
# Obstacle settings and background 
BACKGROUND_SCROLL_SPEED = 3
OBSTACLE_SPEED = 6
GROUND_SCROLL_SPEED = OBSTACLE_SPEED

PLAYER_FRAMES = []
for i in range(FRAME_COUNT):
    frame = SPRITE_SHEET.subsurface(
        (i * PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
    )
    PLAYER_FRAMES.append(frame)




class Ground:
    def __init__(self, speed):
        self.x1 = 0
        self.x2 = WIDTH
        self.speed = speed
        self.image = GROUND_IMG


    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 + WIDTH <= 0:
            self.x1 = self.x2 + WIDTH
        if self.x2 + WIDTH <= 0:
            self.x2 = self.x1 + WIDTH

    def draw(self, surface):
        surface.blit(self.image, (self.x1, HEIGHT - GROUND_HEIGHT))
        surface.blit(self.image, (self.x2, HEIGHT - GROUND_HEIGHT))

class Background:
    def __init__(self, speed):
        self.x1 = 0
        self.x2 = BG_WIDTH
        self.speed = speed 

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 + BG_WIDTH <= 0:
            self.x1 = self.x2 + BG_WIDTH
        if self.x2 + BG_WIDTH <= 0:
            self.x2 = self.x1 + BG_WIDTH

    def draw(self, surface):
        surface.blit(BACKGROUND_IMG, (self.x1, 0))
        surface.blit(BACKGROUND_IMG, (self.x2, 0))


class Player:
    def __init__(self):
        self.frames = PLAYER_FRAMES
        self.current_frame = 0
        self.animation_counter = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, HEIGHT - PLAYER_HEIGHT - GROUND_HEIGHT)
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

        if self.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.on_ground = True
            self.velocity = 0
        

        self.updated_animation()

class Obstacle:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT - GROUND_HEIGHT
        self.rect.left = WIDTH
        self.active = True
        self.passed = False  # Tracks if obstacle was passed

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < -50:
            self.active = False


def game_over(screen, score):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 74)

    game_over_text = font.render("Game Over Kitty!", True, 255, 0, 0)
    screen.blit(game_over_text, (WIDTH//2 - 140, HEIGHT//2 -100))

    #Final score
    score_font = pygame.font.Font(None, 50)
    score_text = score_font.render(f"Meow Final Score is: {score}", True, (0,0,0))
    screen.blit(score_text, (WIDTH//2 - 120, HEIGHT//2))
 

def main():
    clock = pygame.time.Clock()
    fps = 60

    player = Player()
    background = Background(BACKGROUND_SCROLL_SPEED)
    obstacles = []
    spawn_timer = 0 
    score = 0
    ground = Ground(GROUND_SCROLL_SPEED)

    running = True
    while running:
        clock.tick(fps)
        spawn_timer += 1 

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        ground.update()
        background.update()

        player.update()
        # Spawn obstacles every 60 frames (~1 second at 60 FPS)
        if spawn_timer >= 60:
            #making obstacles more fun
            if not obstacles or obstacles[-1].rect.right < WIDTH -200:
                obstacles.append(Obstacle(random.choice(OBSTACLE_IMAGES)))
                spawn_timer = 0  # Reset timer

        
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
        background.draw(WIN)
        ground.draw(WIN)
        WIN.blit(player.image, player.rect)  # Player

        for obstacle in obstacles:
            WIN.blit(obstacle.image, obstacle.rect)

        # Draw score text
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, (0,0,0))
        WIN.blit(text, (10, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()