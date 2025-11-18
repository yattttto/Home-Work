import pygame
import sys
import os

pygame.init()

# Параметры окна
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Artis Impact - Lite")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (70, 130, 180)

# Настройки
class Settings:
    def __init__(self):
        self.volume = 50  # 0–100
        self.resolution = (800, 600)
        self.fullscreen = False

settings = Settings()

# Локации / мб изоброжения 
LOCATIONS = {
    "forest": (34, 139, 34),    # зелёный
    "desert": (210, 180, 140),  # бежевый
    "city": (105, 105, 105),    # серый
}
current_location = "forest"

# мой кубик
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.size = 40
        self.speed = 5

    def move(self, dx, dy):
        self.x = max(0, min(SCREEN_WIDTH - self.size, self.x + dx))
        self.y = max(0, min(SCREEN_HEIGHT - self.size, self.y + dy))

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.size, self.size))

player = Player()

# Шрифты
font = pygame.font.SysFont(None, 36)

# Состояния игры
STATE_MENU = "menu"
STATE_SETTINGS = "settings"
STATE_GAME = "game"
current_state = STATE_MENU

# Кнопки простык
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        text_surf = font.render(self.text, True, WHITE)
        surface.blit(text_surf, (self.rect.centerx - text_surf.get_width() // 2,
                                 self.rect.centery - text_surf.get_height() // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Кнопки
play_button = Button(300, 200, 200, 50, "Играть")
settings_button = Button(300, 270, 200, 50, "Настройки")
back_button = Button(300, 400, 200, 50, "Назад")

location_buttons = [
    Button(100, 100, 150, 50, "Лес"),
    Button(100, 170, 150, 50, "Пустыня"),
    Button(100, 240, 150, 50, "Город"),
]

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == STATE_MENU:
                if play_button.is_clicked(mouse_pos):
                    current_state = STATE_GAME
                elif settings_button.is_clicked(mouse_pos):
                    current_state = STATE_SETTINGS

            elif current_state == STATE_SETTINGS:
                if back_button.is_clicked(mouse_pos):
                    current_state = STATE_MENU
                # Простой выбор локации из настроек
                for i, btn in enumerate(location_buttons):
                    if btn.is_clicked(mouse_pos):
                        current_location = list(LOCATIONS.keys())[i]

        # Движение персонажа (в игре)
        if current_state == STATE_GAME:
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -player.speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = player.speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -player.speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = player.speed
            player.move(dx, dy)

    # Отрисовка
    if current_state == STATE_MENU:
        screen.fill(BLACK)
        play_button.draw(screen)
        settings_button.draw(screen)

    elif current_state == STATE_SETTINGS:
        screen.fill(BLACK)
        back_button.draw(screen)
        title = font.render("Выберите локацию:", True, WHITE)
        screen.blit(title, (100, 50))
        for btn in location_buttons:
            btn.draw(screen)

    elif current_state == STATE_GAME:
        # Фон по текущей локации
        bg_color = LOCATIONS[current_location]
        screen.fill(bg_color)
        player.draw(screen)

        
        hint = font.render("ESC — меню", True, WHITE)
        screen.blit(hint, (10, 10))

        # ESC — вернуться в меню
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            current_state = STATE_MENU

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()