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

# ==========================================================
#  🔍 DEBUG — garante que estamos no diretório certo 
# ==========================================================
print("DEBUG: Current working dir =", os.getcwd())

# ==========================================================
#  Inicializa o PyGame
# ==========================================================
pygame.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS DO JOGO
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape")

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS
# ----------------------------------------------------------
ASSETS = {
    "background": "fundo_espacial.png",
    "player": "nave001.png",
    "meteor": "meteoro001.png",
    "sound_point": "classic-game-action-positive-5-224402.mp3",
    "sound_hit": "stab-f-01-brvhrtz-224599.mp3",
    "music": "distorted-future-363866.mp3"
}

# ----------------------------------------------------------
#  FUNÇÕES ROBUSTAS DE CARREGAMENTO
# ----------------------------------------------------------

def find_file_case_insensitive(dirname, filename):
    try:
        for entry in os.listdir(dirname):
            if entry.lower() == filename.lower():
                return os.path.join(dirname, entry)
    except Exception:
        pass
    return None

def load_image(filename, fallback_color, size=None):
    base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    candidate = os.path.join(base_dir, filename)

    if not os.path.exists(candidate):
        alt = find_file_case_insensitive(base_dir, filename)
        if alt:
            candidate = alt

    if os.path.exists(candidate):
        try:
            print(f"DEBUG: Carregando imagem -> {candidate}")
            img = pygame.image.load(candidate).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except Exception as e:
            print(f"ERRO AO CARREGAR {candidate}: {e}")

    print(f"DEBUG: Usando fallback para '{filename}' (não encontrado)")
    surf = pygame.Surface(size or (50, 50))
    surf.fill(fallback_color)
    return surf

def load_sound(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()
    candidate = os.path.join(base_dir, filename)

    if os.path.exists(candidate):
        print(f"DEBUG: Carregando som -> {candidate}")
        return pygame.mixer.Sound(candidate)

    print(f"DEBUG: som '{filename}' não encontrado — ignorado.")
    return None

# ----------------------------------------------------------
# 🖼️ CARREGAMENTO DE IMAGENS E SONS
# ----------------------------------------------------------
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (80, 60))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])

if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

# ----------------------------------------------------------
# 🖥️ TELA INSERT COIN
# ----------------------------------------------------------
clock = pygame.time.Clock()

def insert_coin_screen():
    blink = True
    blink_timer = 0
    font_big = pygame.font.Font(None, 80)
    running_insert = True

    while running_insert:
        screen.blit(background, (0, 0))

        # piscar texto
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

            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # avança para próxima tela

# ----------------------------------------------------------
# 🖥️ TELA DE SELEÇÃO DE FASE
# ----------------------------------------------------------

def select_phase_screen():
    font_big = pygame.font.Font(None, 60)
    font_small = pygame.font.Font(None, 40)

    options = [
        ("FÁCIL", 200, (0, 255, 0)),
        ("MÉDIO", 300, (255, 255, 0)),
        ("DIFÍCIL", 400, (255, 0, 0))
    ]

    while True:
        screen.blit(background, (0, 0))

        title = font_big.render("SELECIONE A FASE", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for text, y, color in options:
            label = font_small.render(text, True, color)
            rect = label.get_rect(center=(WIDTH//2, y))

            # hover
            if rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, (255, 255, 255), rect.inflate(20, 10), 2)

            screen.blit(label, rect)

        pygame.display.flip()
        clock.tick(FPS)

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text, y, color in options:
                    label = font_small.render(text, True, color)
                    rect = label.get_rect(center=(WIDTH//2, y))
                    if rect.collidepoint(mouse_x, mouse_y):
                        return text.lower()  # "fácil", "médio", "difícil"

# ----------------------------------------------------------
# 🕹️ LOOP DE JOGO (FASE PADRÃO POR ENQUANTO)
# ----------------------------------------------------------

def play_game(level):

    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    player_speed = 7

    meteor_list = []
    for _ in range(5):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-500, -40)
        meteor_list.append(pygame.Rect(x, y, 40, 40))

    meteor_speed = 5
    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        clock.tick(FPS)
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # movimento lateral
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        # movimentação dos meteoros
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
                    running = False

        # desenha
        screen.blit(player_img, player_rect)
        for meteor in meteor_list:
            screen.blit(meteor_img, meteor)

        text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()

    # fim da fase
    return score

# ----------------------------------------------------------
# 🏁 TELA DE FIM
# ----------------------------------------------------------

def end_screen(score):
    pygame.mixer.music.stop()
    screen.fill((20, 20, 20))
    font = pygame.font.Font(None, 48)

    end_text = font.render("Fim de jogo! Pressione qualquer tecla.", True, WHITE)
    final_score = font.render(f"Pontuação final: {score}", True, WHITE)
    screen.blit(end_text, (150, 260))
    screen.blit(final_score, (250, 300))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False

# ----------------------------------------------------------
# 🚀 INÍCIO DO JOGO
# ----------------------------------------------------------

insert_coin_screen()
fase = select_phase_screen()
pontos = play_game(fase)
end_screen(pontos)

pygame.quit()
