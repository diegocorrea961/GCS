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
import json
import time

#contornar textos
def outline_text(text, font, color, outline_color):
    base = font.render(text, True, color)
    outline = font.render(text, True, outline_color)

    surf = pygame.Surface((base.get_width() + 4, base.get_height() + 4), pygame.SRCALPHA)

    # contorno nas 4 direções
    surf.blit(outline, (2, 0))
    surf.blit(outline, (0, 2))
    surf.blit(outline, (4, 2))
    surf.blit(outline, (2, 4))

    surf.blit(base, (2, 2))
    return surf


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
    "music_medio": "music_medio.mp3",
    "music_dificil": "music_dificil.mp3",

    # imagens de fundo por fase
    "bg_facil": "imgfundo_facil.png",
    "bg_medio": "imgfundo_medio.png",
    "bg_dificil": "imgfundo_dificil.png",

    # telas finais
    "img_gameover": "img_gameover.png",
    "img_vitoria": "img_vitoria.png",
}

SCORES_FILE = "scores.json"

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
        except Exception as e:
            print(f"Erro ao carregar imagem {filepath}: {e}")

    surf = pygame.Surface(size or (50, 50))
    surf.fill(fallback_color)
    return surf

def load_sound(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filename)

    if os.path.exists(filepath):
        try:
            return pygame.mixer.Sound(filepath)
        except Exception as e:
            print(f"Erro ao carregar som {filepath}: {e}")
    return None

def play_music(filename, volume=0.4):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, filename)

    try:
        pygame.mixer.music.stop()
        if os.path.exists(filepath):
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        else:
            print(f"[AVISO] Música não encontrada: {filepath}")
    except Exception as e:
        print(f"Erro ao tocar música {filepath}: {e}")

# Funções para salvar/carregar scores
def load_scores():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, SCORES_FILE)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "last_facil": 0,
        "last_medio": 0,
        "last_dificil": 0,
        "high_facil": 0,
        "high_medio": 0,
        "high_dificil": 0
    }

def save_scores(scores):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, SCORES_FILE)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(scores, f, indent=2)
    except Exception as e:
        print(f"Erro ao salvar scores: {e}")

# Carregar imagens e sons
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
YELLOW = (240, 220, 70)

background_menu = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (80, 60))

# ⚠️ Carregar sprites animados do meteoro
meteor_frames = [
    load_image("img_met1.png", RED, (40, 40)),
    load_image("img_met2.png", RED, (40, 40)),
    load_image("img_met3.png", RED, (40, 40)),
    load_image("img_met4.png", RED, (40, 40)),
]

# Imagens finais
img_gameover = load_image(ASSETS["img_gameover"], (20,20,20), (WIDTH, HEIGHT))
img_vitoria = load_image(ASSETS["img_vitoria"], (20,20,20), (WIDTH, HEIGHT))

# efeitos sonoros
sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])
if sound_point:
    sound_point.set_volume(0.2)
if sound_hit:
    sound_hit.set_volume(0.1)

# fundos das fases
bg_facil_img = load_image(ASSETS["bg_facil"], (0,0,0), (WIDTH, HEIGHT))
bg_medio_img = load_image(ASSETS["bg_medio"], (0,0,30), (WIDTH, HEIGHT))
bg_dificil_img = load_image(ASSETS["bg_dificil"], (40,0,0), (WIDTH, HEIGHT))

scores = load_scores()

# ---------- TELA INSERT COIN ----------
def insert_coin_screen():
    # tocar a música das telas (não reiniciará ao entrar na seleção)
    play_music(ASSETS["music_tela"])

    font_big = pygame.font.Font(None, 80)
    font_small = pygame.font.Font(None, 20)

    blink = True
    blink_timer = 0

    strong_yellow = (255, 240, 50)
    outline_color = (0, 0, 0)  # contorno preto

    while True:
        screen.blit(background_menu, (0, 0))

        blink_timer += clock.get_time()
        if blink_timer > 500:
            blink = not blink
            blink_timer = 0

        # ---------- TEXTO COM CONTORNO ----------
        def render_with_outline(text, font, text_color, outline_color):
            base = font.render(text, True, text_color)
            outline = font.render(text, True, outline_color)

            surf = pygame.Surface((base.get_width()+4, base.get_height()+4), pygame.SRCALPHA)

            # desenha contorno em 4 direções
            surf.blit(outline, (2-2, 2))   # esquerda
            surf.blit(outline, (2+2, 2))   # direita
            surf.blit(outline, (2, 2-2))   # cima
            surf.blit(outline, (2, 2+2))   # baixo

            # texto por cima
            surf.blit(base, (2, 2))
            return surf
        # ----------------------------------------

        # Título blinking
        if blink:
            title = render_with_outline("INSERT COIN", font_big, strong_yellow, outline_color)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 40))

        # Mensagem "pressione espaço"
        msg = render_with_outline("PRESSIONE ESPAÇO", font_small, WHITE, outline_color)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 + 120))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # agora SOMENTE a tecla espaço inicia
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


# ---------- SELEÇÃO DE FASE ----------
def select_phase_screen():
    font_title = pygame.font.Font(None, 70)
    font_btn = pygame.font.Font(None, 50)
    font_score = pygame.font.Font(None, 30)

    # Botões alinhados na horizontal
    btn_y = 300
    spacing = 220

    options = [
        ("FÁCIL", WIDTH//2 - spacing, "facil", bg_facil_img, "music_facil", (20, 200, 20)),     # verde
        ("MÉDIO", WIDTH//2,          "medio", bg_medio_img, "music_medio", (230, 230, 40)),   # amarelo
        ("DIFÍCIL", WIDTH//2 + spacing, "dificil", bg_dificil_img, "music_dificil", (220, 50, 50)),  # vermelho
    ]

    while True:
        screen.blit(background_menu, (0, 0))

        # Título contornado
        title = outline_text("SELECIONE A FASE", font_title, (255, 255, 0), (0, 0, 0))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for text, x, key, bg_img, music_key, color in options:
            # Botão
            btn_surface = outline_text(text, font_btn, color, (0, 0, 0))
            btn_rect = btn_surface.get_rect(center=(x, btn_y))

            # Hover – contorno branco
            if btn_rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, (255, 255, 255), btn_rect.inflate(20, 10), 3)

            screen.blit(btn_surface, btn_rect)

            # SCORE abaixo
            score_value = scores.get("last_" + key, 0)
            score_text = outline_text(f"Score: {score_value}", font_score, (255, 255, 255), (0, 0, 0))

            score_rect = score_text.get_rect(center=(x, btn_y + 50))
            screen.blit(score_text, score_rect)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text, x, key, bg_img, music_key, color in options:
                    btn_surface = outline_text(text, font_btn, color, (0, 0, 0))
                    btn_rect = btn_surface.get_rect(center=(x, btn_y))
                    if btn_rect.collidepoint(mouse_x, mouse_y):
                        return key


# ---------- PARÂMETROS DAS FASES ----------
def get_level_params(level_key):
    if level_key == "facil":
        return (2, 3, 1000, 8, 1, 300, bg_facil_img, ASSETS["music_facil"])
    elif level_key == "medio":
        return (2, 6, 800, 12, 2, 250, bg_medio_img, ASSETS["music_medio"])
    else:
        return (5, 9, 600, 20, 3, 200, bg_dificil_img, ASSETS["music_dificil"])

# ---------- LOOP DO JOGO ----------
def play_game(level_key):
    min_speed, max_speed, spawn_interval, max_meteoros, points_per, victory_target, bg_img, music_file = get_level_params(level_key)

    play_music(music_file)

    player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
    player_speed = 7

    meteor_list = []
    lasers = []

    lives = 10
    score = 0

    font = pygame.font.Font(None, 36)
    spawn_acc = 0

    while True:
        dt = clock.tick(FPS)
        spawn_acc += dt

        screen.blit(bg_img, (0, 0))

        # eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                lx = player_rect.centerx
                ly = player_rect.top
                lasers.append({'rect': pygame.Rect(lx-4, ly-20, 8, 20), 'speed': 12})

        # movimento nave
        mx, my = pygame.mouse.get_pos()
        player_rect.centerx = mx
        if player_rect.left < 0: player_rect.left = 0
        if player_rect.right > WIDTH: player_rect.right = WIDTH

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]: player_rect.x += player_speed

        # spawn meteoro
        if spawn_acc >= spawn_interval and len(meteor_list) < max_meteoros:
            spawn_acc = 0
            rect = pygame.Rect(random.randint(0, WIDTH-40), random.randint(-200, -40), 40, 40)
            meteor_list.append({'rect': rect, 'speed': random.randint(min_speed, max_speed), 'frame': 0, 'frame_time': 0})

        # atualizar lasers
        for laser in list(lasers):
            laser['rect'].y -= laser['speed']
            if laser['rect'].bottom < 0:
                lasers.remove(laser)

        # atualizar meteoros
        for meteor in list(meteor_list):
            meteor['rect'].y += meteor['speed']

            # animação
            meteor['frame_time'] += dt
            if meteor['frame_time'] >= 100:
                meteor['frame_time'] = 0
                meteor['frame'] = (meteor['frame'] + 1) % len(meteor_frames)

            # colisão laser
            hit = False
            for laser in list(lasers):
                if meteor['rect'].colliderect(laser['rect']):
                    meteor_list.remove(meteor)
                    lasers.remove(laser)
                    score += points_per
                    if sound_point: sound_point.play()
                    hit = True
                    break
            if hit: continue

            # passar da tela
            if meteor['rect'].y > HEIGHT:
                lives -= 1
                meteor['rect'].y = random.randint(-200, -40)
                meteor['rect'].x = random.randint(0, WIDTH-40)
                meteor['speed'] = random.randint(min_speed, max_speed)
                if lives <= 0:
                    return score, "lose"

            # colisão nave
            if meteor['rect'].colliderect(player_rect):
                lives -= 1
                meteor['rect'].y = random.randint(-200, -40)
                meteor['rect'].x = random.randint(0, WIDTH-40)
                meteor['speed'] = random.randint(min_speed, max_speed)
                if sound_hit: sound_hit.play()
                if lives <= 0:
                    return score, "lose"

        # desenhar lasers
        for laser in lasers:
            pygame.draw.rect(screen, (0, 255, 255), laser['rect'])

        # desenhar nave
        screen.blit(player_img, player_rect)

        # desenhar meteoros
        for meteor in meteor_list:
            frame = meteor_frames[meteor['frame']]
            screen.blit(frame, meteor['rect'])

        # HUD
        text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
        screen.blit(text, (10, 10))

        if score >= victory_target:
            return score, "win"

        pygame.display.flip()

# ---------- TELA FINAL ----------
def end_screen(score, result, level_key):
    pygame.mixer.music.stop()

    # fundo já contém "GAME OVER" ou "VITÓRIA"
    img = img_vitoria if result == "win" else img_gameover
    screen.blit(img, (0, 0))

    # textos inferiores
    pontos_txt = f"Pontuação final: {score}"
    subtitulo = "PRESSIONE ESPAÇO PARA VOLTAR"

    font_pts = pygame.font.Font(None, 40)   # menor
    font_sub = pygame.font.Font(None, 38)

    def draw_text_outline(font, text, color, x, y):
        outline_color = (0, 0, 0)
        offsets = [(-2,0),(2,0),(0,-2),(0,2)]
        for ox, oy in offsets:
            s = font.render(text, True, outline_color)
            screen.blit(s, (x + ox, y + oy))
        s = font.render(text, True, color)
        screen.blit(s, (x, y))

    # posições mais para baixo
    y_points = HEIGHT // 2 + 80
    y_sub = HEIGHT // 2 + 150

    # desenhar pontuação
    draw_text_outline(
        font_pts, pontos_txt, (255, 255, 255),
        WIDTH//2 - font_pts.size(pontos_txt)[0]//2,
        y_points
    )

    # desenhar "pressione espaço"
    draw_text_outline(
        font_sub, subtitulo, (255, 230, 0),
        WIDTH//2 - font_sub.size(subtitulo)[0]//2,
        y_sub
    )

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                return


# ---------- LOOP PRINCIPAL ----------
while True:
    insert_coin_screen()
    fase_escolhida = select_phase_screen()
    pontos, resultado = play_game(fase_escolhida)
    end_screen(pontos, resultado, fase_escolhida)