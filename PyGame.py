import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1000
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Constants
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 15
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 60
GRAVITY = 0.5
JUMP_STRENGTH = 15
MOVE_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Sounds
welcome_sound = pygame.mixer.Sound('boing-spring-mouth-harp-04-20-13-4-103346.mp3')
jump_sound = pygame.mixer.Sound('Jump sound effect.mp3')
death_sound = pygame.mixer.Sound('retro-video-game-death-95730.mp3')
win_sound = pygame.mixer.Sound('Victory Sound Effect.mp3')

# Sound Volume
jump_sound.set_volume(0.2)
death_sound.set_volume(0.5)
win_sound.set_volume(0.5)

# Images
platform_image = pygame.image.load("cloud platform.png")
player_image = pygame.image.load("player.png")
background_image = None



def load_visuals(level):
    global background_image, platform_image, player_image

    if level == "One":
        background_image = pygame.image.load("mountain_img.jpg")
    elif level == "Two":
        background_image = pygame.image.load("Cloud_img.jpg")
    elif level == "Three":
        background_image = pygame.image.load("Space_img.webp")
    else:
        background_image = WHITE

    # Scale images to fit screen size
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    platform_image = pygame.transform.scale(platform_image, (PLATFORM_WIDTH, PLATFORM_HEIGHT))
    player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))



class Platform:
    def __init__(self, x, y, width=PLATFORM_WIDTH):
        self.rect = pygame.Rect(x, y, width, PLATFORM_HEIGHT)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True


    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.on_ground = False
            jump_sound.play()


    def move(self, keys, platforms):
        if keys[pygame.K_LEFT]:
            self.rect.x -= MOVE_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.rect.x += MOVE_SPEED
            self.facing_right = True
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        self.check_collision(platforms)


    def check_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True


    def draw(self, screen):
            image_to_draw = pygame.transform.flip(player_image, not self.facing_right, False)
            screen.blit(image_to_draw, self.rect)



def generate_platforms(num_platforms):
    platforms = []
    base_y = SCREEN_HEIGHT - PLATFORM_HEIGHT  # First platform at the very bottom of the screen
    spacing = SCREEN_HEIGHT // (num_platforms + 1)

    for i in range(1, num_platforms + 1):
        x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        y = base_y - (i * spacing)
        platforms.append(Platform(x, y))
    return platforms



def game_loop(level, platform_count):

    load_visuals(level)

    platforms = generate_platforms(platform_count)
    bottom_platform = platforms[0]
    player = Player(bottom_platform.rect.x + (PLATFORM_WIDTH - PLAYER_WIDTH) // 2, bottom_platform.rect.y - PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        keys = pygame.key.get_pressed()
        player.move(keys, platforms)

        if player.rect.top > SCREEN_HEIGHT:  # Check if player falls off screen
            game_over = True
        elif player.rect.top <= 0:  # Player reaches top of screen
            break

        # Draw the background
        SCREEN.blit(background_image, (0, 0))

        # Draw platforms
        for platform in platforms:
            SCREEN.blit(platform_image, platform.rect)

        # Draw player
        player.draw(SCREEN)

        pygame.display.flip()
        clock.tick(60)

    if game_over:
        display_message("Game Over", RED, death_sound)



def display_message(text, color, sound):
    sound.play()
    SCREEN.fill(color)
    font = pygame.font.Font(None, 30)
    message = font.render(text, True, WHITE)
    SCREEN.blit(message, ((SCREEN_WIDTH - message.get_width()) // 2, SCREEN_HEIGHT // 2))

    if color == (22, 122, 24):
        quit_text = font.render("Press C to Continue", True, WHITE)
        SCREEN.blit(quit_text, ((SCREEN_WIDTH - quit_text.get_width()) // 2, SCREEN_HEIGHT // 2 + 50))
    else:
        quit_text = font.render("Press ESC to Quit", True, WHITE)
        SCREEN.blit(quit_text, ((SCREEN_WIDTH - quit_text.get_width()) // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()

    stay = True

    while stay:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                stay = False




display_message("Use the arrow keys to move and ESC to quit", (22, 122, 24), welcome_sound)

levels = [("One", 10), ("Two", 8), ("Three", 6)]
for level_name, platform_count in levels:
    game_loop(level_name, platform_count)
display_message("You Won! Congratulations!", BLUE, win_sound)

print("Thank you for playing!")
