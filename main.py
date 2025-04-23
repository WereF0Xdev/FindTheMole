import random
import pygame
from pygame import Rect, Surface

# ─────────────────────── CONFIG ────────────────────────── #
GRID_SIZE   = 8
SQ_SIZE     = 80
GAP         = 2
ATTEMPTS    = 5

LIGHT       = (240, 217, 181)
DARK        = (181, 136, 99)
MOLE_COLOR  = (250, 80, 80)
BG_COLOR    = (205, 205, 205)
TEXT_COLOR  = (15, 15, 15)
HOVER_COLOR = (255, 255, 0, 60)
FONT_NAME   = "arial"
# ───────────────────────────────────────────────────────── #

HEADER_H  = 80
WIN_W     = GRID_SIZE * SQ_SIZE
WIN_H     = GRID_SIZE * SQ_SIZE + HEADER_H

pygame.init()
screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Find the Mole")
clock = pygame.time.Clock()

try:
    font_big  = pygame.font.SysFont(FONT_NAME, 27, bold=True)
    font_small = pygame.font.SysFont(FONT_NAME, 24)
except Exception:
    font_big  = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)

def new_game():
    return {
        "mole": (random.randrange(GRID_SIZE), random.randrange(GRID_SIZE)),
        "revealed": set(),
        "attempts": ATTEMPTS,
        "state": "playing",
    }

game = new_game()

def square_at_pos(mx, my):
    if my < HEADER_H:
        return None
    col = mx // SQ_SIZE
    row = (my - HEADER_H) // SQ_SIZE
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        return row, col
    return None

def square_rect(row, col):
    return Rect(col*SQ_SIZE, HEADER_H + row*SQ_SIZE, SQ_SIZE, SQ_SIZE)

def draw_board():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = square_rect(r, c)
            base = LIGHT if (r+c) % 2 == 0 else DARK
            pygame.draw.rect(screen, base, rect)
            pygame.draw.rect(screen, (0,0,0), rect, GAP)

            if (r, c) in game["revealed"] and (r, c) != game["mole"]:
                shade = tuple(max(0, x-50) for x in base)
                pygame.draw.rect(screen, shade, rect)

    if game["state"] in ("won", "lost"):
        r, c = game["mole"]
        pygame.draw.rect(screen, MOLE_COLOR, square_rect(r, c))

    if game["state"] == "playing":
        mx, my = pygame.mouse.get_pos()
        pos = square_at_pos(mx, my)
        if pos:
            r, c = pos
            hover = square_rect(r, c)
            s = pygame.Surface((SQ_SIZE, SQ_SIZE), pygame.SRCALPHA)
            s.fill(HOVER_COLOR)
            screen.blit(s, hover.topleft)

def draw_header():
    screen.fill(BG_COLOR, Rect(0, 0, WIN_W, HEADER_H))

    if game["state"] == "playing":
        msg = f"Attempts left: {game['attempts']}"
    elif game["state"] == "won":
        msg = "You found the mole! Press R to play again."
    else:
        mr, mc = game["mole"]
        msg = f"You lost! Mole was at ({mr+1},{mc+1}). Press R to retry."

    txt: Surface = font_big.render(msg, True, TEXT_COLOR)
    screen.blit(txt, ((WIN_W - txt.get_width())//2, HEADER_H//2 - txt.get_height()//2))

def handle_click(pos):
    if game["state"] != "playing":
        return
    if pos in game["revealed"]:
        return
    game["revealed"].add(pos)
    if pos == game["mole"]:
        game["state"] = "won"
    else:
        game["attempts"] -= 1
        if game["attempts"] <= 0:
            game["state"] = "lost"

running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_r:
            game = new_game()
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            p = square_at_pos(*ev.pos)
            if p:
                handle_click(p)

    draw_header()
    draw_board()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
