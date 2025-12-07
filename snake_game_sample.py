import pyxel
import time
import random

# 画面サイズ
W = 160
H = 120
CELL = 8

GRID_W = W // CELL
GRID_H = H // CELL

snake = [(10, 7), (9, 7), (8, 7)]
dx, dy = 1, 0

food = (5, 5)
food_type = "glucose"
food_tips = {
    "glucose": "グルコースは体のエネルギー源！",
    "vitamin": "ビタミンCは免疫力を高める！",
    "antibiotic": "抗生物質は細菌を倒すけどウイルスには効かない！"
}
tip_message = ""
tip_time = 0

game_over = False
last_move_time = time.time()


def place_food():
    global food, food_type
    while True:
        x = random.randrange(GRID_W)
        y = random.randrange(GRID_H)
        if (x, y) not in snake:
            food = (x, y)
            break
    r = random.random()
    if r < 0.7:
        food_type = "glucose"
    elif r < 0.9:
        food_type = "vitamin"
    else:
        food_type = "antibiotic"


def update():
    global dx, dy, last_move_time, game_over, tip_message, tip_time

    if game_over:
        return

    if pyxel.btnp(pyxel.KEY_LEFT) and dx != 1:
        dx, dy = -1, 0
    if pyxel.btnp(pyxel.KEY_RIGHT) and dx != -1:
        dx, dy = 1, 0
    if pyxel.btnp(pyxel.KEY_UP) and dy != 1:
        dx, dy = 0, -1
    if pyxel.btnp(pyxel.KEY_DOWN) and dy != -1:
        dx, dy = 0, 1

    now = time.time()
    if now - last_move_time < 0.2:
        return
    last_move_time = now

    head_x, head_y = snake[0]
    new_x = head_x + dx
    new_y = head_y + dy

    if new_x < 0 or new_x >= GRID_W or new_y < 0 or new_y >= GRID_H:
        game_over = True
        return
    if (new_x, new_y) in snake:
        game_over = True
        return

    # 頭を追加
    snake.insert(0, (new_x, new_y))

    # 食べた判定
    if (new_x, new_y) == food:
        tip_message = food_tips[food_type]
        tip_time = time.time()
        place_food()
    else:
        snake.pop()


def draw():
    pyxel.cls(0)

    if game_over:
        pyxel.text(W//2 - 20, H//2, "GAME OVER", 8)
        return

    fx, fy = food
    color_map = {"glucose": 8, "vitamin": 11, "antibiotic": 12}
    pyxel.rect(fx * CELL, fy * CELL, CELL, CELL, color_map[food_type])

    for i, (x, y) in enumerate(snake):
        color = 11 if i == 0 else 7
        pyxel.rect(x * CELL, y * CELL, CELL, CELL, color)

    if tip_message and time.time() - tip_time < 3:
        pyxel.text(5, H-10, tip_message, 10)


pyxel.init(W, H, title="Snake Medical")
pyxel.run(update, draw)
