

import pygame
import sys
import random
import requests
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tombola - Pygame Version')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 215)
GREEN = (144, 238, 144)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 24)
tiny_font = pygame.font.SysFont('Arial', 18)


# Input boxes for server URL and username
input_box_url = pygame.Rect(250, 150, 300, 40)
input_box_user = pygame.Rect(300, 210, 200, 40)
server_url = ''
username = ''
active_url = False
active_user = False

# Button
button_rect = pygame.Rect(350, 280, 100, 40)

# Tombola card settings
CELL_SIZE = 50
GAP = 5
BOARD_TOPLEFT = (WIDTH // 2 - (9 * CELL_SIZE + 8 * GAP) // 2, 160)

# Win buttons
win_types = ['Ambo', 'Terno', 'Quaterna', 'Cinquina', 'Tombola']
win_buttons = []
for i, label in enumerate(win_types):
    rect = pygame.Rect(120 + i * 130, 400, 120, 40)
    win_buttons.append((rect, label))

# Message
message = ''
message_color = BLACK

def generate_tombola_card():
    decine = [list(range(1, 10)),
              list(range(10, 20)),
              list(range(20, 30)),
              list(range(30, 40)),
              list(range(40, 50)),
              list(range(50, 60)),
              list(range(60, 70)),
              list(range(70, 80)),
              list(range(80, 91))]
    used_numbers = set()
    card = [[None for _ in range(9)] for _ in range(3)]
    for r in range(3):
        chosen_cols = []
        while len(chosen_cols) < 5:
            col = random.randint(0, 8)
            if col not in chosen_cols:
                chosen_cols.append(col)
        for col in chosen_cols:
            while True:
                num = random.choice(decine[col])
                if num not in used_numbers:
                    used_numbers.add(num)
                    card[r][col] = num
                    break
    return card

def draw_home():
    screen.fill(WHITE)
    title = font.render('Client Tombola', True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))
    # Server URL input
    pygame.draw.rect(screen, BLUE if active_url else BLACK, input_box_url, 2)
    url_text = small_font.render(server_url or 'URL server (es. http://localhost:3001)', True, BLACK)
    screen.blit(url_text, (input_box_url.x + 10, input_box_url.y + 5))
    # Username input
    pygame.draw.rect(screen, BLUE if active_user else BLACK, input_box_user, 2)
    user_text = small_font.render(username or 'Username', True, BLACK)
    screen.blit(user_text, (input_box_user.x + 10, input_box_user.y + 5))
    # Button
    pygame.draw.rect(screen, BLUE, button_rect)
    btn_text = small_font.render('Gioca', True, WHITE)
    screen.blit(btn_text, (button_rect.x + 20, button_rect.y + 5))
    pygame.display.flip()

def draw_card(card, selected):
    # Draw the 3x9 card
    for r in range(3):
        for c in range(9):
            x = BOARD_TOPLEFT[0] + c * (CELL_SIZE + GAP)
            y = BOARD_TOPLEFT[1] + r * (CELL_SIZE + GAP)
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            if card[r][c] is not None:
                color = GREEN if card[r][c] in selected else WHITE
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
                num_text = small_font.render(str(card[r][c]), True, BLACK)
                screen.blit(num_text, (x + CELL_SIZE // 2 - num_text.get_width() // 2, y + CELL_SIZE // 2 - num_text.get_height() // 2))
            else:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)

def draw_game(username, card, selected, message, message_color):
    screen.fill(WHITE)
    title = font.render(f'Scheda di {username}', True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
    draw_card(card, selected)
    # Draw win buttons
    for rect, label in win_buttons:
        pygame.draw.rect(screen, BLUE, rect)
        btn_text = tiny_font.render(label, True, WHITE)
        screen.blit(btn_text, (rect.x + rect.width // 2 - btn_text.get_width() // 2, rect.y + rect.height // 2 - btn_text.get_height() // 2))
    # Draw message
    if message:
        msg = small_font.render(message, True, message_color)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 500))
    pygame.display.flip()

def get_card_cell_at_pos(pos):
    """Return (row, col) of the card cell at screen position pos, or (None, None) if outside cells."""
    x0, y0 = BOARD_TOPLEFT
    x, y = pos
    # Quick bounds check
    total_width = 9 * CELL_SIZE + 8 * GAP
    total_height = 3 * CELL_SIZE + 2 * GAP
    if x < x0 or x > x0 + total_width or y < y0 or y > y0 + total_height:
        return None, None
    relx = x - x0
    rely = y - y0
    cell_w = CELL_SIZE + GAP
    col = int(relx // cell_w)
    row = int(rely // cell_w)
    # Make sure click wasn't in the gap area
    cx = relx % cell_w
    cy = rely % cell_w
    if cx > CELL_SIZE or cy > CELL_SIZE:
        return None, None
    if 0 <= row < 3 and 0 <= col < 9:
        return row, col
    return None, None


def try_join(server_url, username, card):
    global message, message_color
    try:
        url = server_url.rstrip('/') + '/join'
        payload = {"username": username, "card": [[n for n in row if n is not None] for row in card]}
        res = requests.post(url, json=payload, timeout=5)
        data = res.json()
        if 'error' in data:
            message = 'Errore registrazione: ' + str(data['error'])
            message_color = (200, 0, 0)
        else:
            message = 'Registrazione avvenuta con successo!'
            message_color = GREEN
    except Exception:
        message = 'Errore di connessione al server'
        message_color = (200, 0, 0)


def try_check_win(server_url, username, selected, win_type):
    global message, message_color
    try:
        url = server_url.rstrip('/') + '/checkWin'
        payload = {"username": username, "numbers": selected}
        res = requests.post(url, json=payload, timeout=5)
        data = res.json()
        if 'error' in data:
            message = 'Errore: ' + str(data['error'])
            message_color = (200, 0, 0)
        else:
            message = f'Vincita registrata: {data.get("type", win_type)}'
            message_color = GREEN
    except Exception:
        message = 'Errore di connessione al server'
        message_color = (200, 0, 0)


def main():
    global active_url, active_user, server_url, username, message
    running = True
    on_home = True
    card = None
    selected = []
    print('main: starting game loop')
    start_time = time.time()

    while running:
        for event in pygame.event.get():
            # Debug: print events for first 3 seconds to inspect unexpected QUIT
            if time.time() - start_time < 3:
                print('event:', event)
            if event.type == pygame.QUIT:
                print('main: received QUIT event')
                running = False
            if on_home:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box_url.collidepoint(event.pos):
                        active_url = True
                        active_user = False
                    elif input_box_user.collidepoint(event.pos):
                        active_user = True
                        active_url = False
                    else:
                        active_url = False
                        active_user = False
                    if button_rect.collidepoint(event.pos) and server_url.strip() and username.strip():
                        on_home = False
                        card = generate_tombola_card()
                        selected = []
                        message = ''
                        try_join(server_url, username, card)
                if event.type == pygame.KEYDOWN:
                    if active_url:
                        if event.key == pygame.K_RETURN:
                            active_url = False
                        elif event.key == pygame.K_BACKSPACE:
                            server_url = server_url[:-1]
                        else:
                            if len(server_url) < 64 and event.unicode.isprintable():
                                server_url += event.unicode
                    elif active_user:
                        if event.key == pygame.K_RETURN:
                            active_user = False
                        elif event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        else:
                            if len(username) < 16 and event.unicode.isprintable():
                                username += event.unicode
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check for cell click
                    r, c = get_card_cell_at_pos(event.pos)
                    if r is not None and c is not None and card[r][c] is not None:
                        num = card[r][c]
                        if num in selected:
                            selected.remove(num)
                        else:
                            selected.append(num)
                    # Check win buttons
                    for rect, label in win_buttons:
                        if rect.collidepoint(event.pos):
                            try_check_win(server_url, username, selected, label)
        if on_home:
            draw_home()
        else:
            draw_game(username, card, selected, message, message_color)
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
