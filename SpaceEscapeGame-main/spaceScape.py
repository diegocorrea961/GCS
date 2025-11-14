##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.3                      ###
##############################################################
### Objetivo: desviar dos meteoros que caem.               ###
### Cada colisão tira uma vida. Sobreviva o máximo que     ###
### conseguir!                                             ###
##############################################################
### Prof. Filipo Novo Mor - github.com/ProfessorFilipo     ###
##############################################################

import pygame
import random
import os

# Inicialização
pygame.init()

# Configurações do jogo
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("Space Escape")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Arquivos de mídia
ASSETS = {
    "background": "fundo_espacial.png",
    "player": "nave001.png",
    "meteor": "meteoro001.png",
    "sound_point": "classic-game-action-positive-5-224402.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",

    "music_tela": "music_tela.mp3",
    "music_facil": "music_facil.mp3",
    "music_medio": "musica_medio.mp3",
    "music_dificil": "musica_dificil.mp3",
}

# Funções auxiliares
def find_file_case_insensitive(dirname, filename):
    try:
        for entry in os.listdir(dirname):
            if entry.lower() == filename.lower():
                return os.path.join(dirname, entry)
    except:
        pass
    return None

def load_image(filename, fallback_color, size=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filename)

    if not os.path.exists(filepath):
        alt = find_file_case_insensitive(base_dir, filename)
        if alt:
            filepath = alt

    if os.path.exists(filepath):
        try:
            img = pygame.image.load(filepath).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except:
            pass

    surf = pygame.Surface(size or (50, 50))
    surf.fill(fallback_color)
    return surf

def load_sound(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filename)

    if os.path.exists(filepath):
        return pygame.mixer.Sound(filepath)
    return None

def play_music(filename, volume=0.4):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filename)

    if os.path.exists(filepath):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

# Carregar imagens e sons
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)

background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])

# TELA: INSERT COIN
def insert_coin_screen():
    play_music(ASSETS["music_tela"])

    font_big = pygame.font.Font(None, 80)
    blink = True
    blink_timer = 0

    while True:
        screen.blit(background, (0, 0))

        blink_timer += clock.get_time()
        if blink_timer > 500:
            blink = not blink
            blink_timer = 0

        title = font_big.render("INSERT COIN", True, WHITE)
        if blink:
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 40))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return

# TELA: SELEÇÃO DE FASE
def select_phase_screen():
    # play_music(ASSETS["music_tela"]) # removido para musica não reiniciar

    font_big = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 40)

    options = [
        ("FÁCIL", 250, "music_facil"),
        ("MÉDIO", 330, "music_medio"),
        ("DIFÍCIL", 410, "music_dificil")
    ]

    while True:
        screen.blit(background, (0, 0))

        title = font_big.render("SELECIONE A FASE", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for text, y, music_key in options:
            label = font_small.render(text, True, WHITE)
            rect = label.get_rect(center=(WIDTH//2, y))

            if rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, WHITE, rect.inflate(20, 10), 2)

            screen.blit(label, rect)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text, y, music_key in options:
                    label = font_small.render(text, True, WHITE)
                    rect = label.get_rect(center=(WIDTH//2, y))
                    if rect.collidepoint(mouse_x, mouse_y):
                        return music_key

# LOOP DO JOGO
def play_game(level_music_key):
    play_music(ASSETS[level_music_key])

    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    player_speed = 7

    meteor_list = [pygame.Rect(random.randint(0, WIDTH-40), random.randint(-500,-40), 40, 40) for _ in range(5)]
    meteor_speed = 5

    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)

    while True:
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        for meteor in meteor_list:
            meteor.y += meteor_speed

            if meteor.y > HEIGHT:
                meteor.y = random.randint(-100, -40)
                meteor.x = random.randint(0, WIDTH - meteor.width)
                score += 1
                if sound_point:
                    sound_point.play()

            if meteor.colliderect(player_rect):
                lives -= 1
                meteor.y = random.randint(-100, -40)
                meteor.x = random.randint(0, WIDTH - meteor.width)
                if sound_hit:
                    sound_hit.play()
                if lives <= 0:
                    return score

        screen.blit(player_img, player_rect)
        for meteor in meteor_list:
            screen.blit(meteor_img, meteor)

        text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()

# TELA FINAL
def end_screen(score):
    pygame.mixer.music.stop()
    screen.fill((20, 20, 20))
    font = pygame.font.Font(None, 48)

    end_text = font.render("Fim de jogo! Pressione qualquer tecla.", True, WHITE)
    final_score = font.render(f"Pontuação final: {score}", True, WHITE)

    screen.blit(end_text, (150, 260))
    screen.blit(final_score, (250, 300))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                return

# Fluxo principal
insert_coin_screen()
fase_escolhida = select_phase_screen()
pontuacao = play_game(fase_escolhida)
end_screen(pontuacao)

pygame.quit()
