import pyxel
import random
import time

W = 160
H = 120
state = "intro"

pad_x, pad_y = 70, 110
pad_w, pad_h = 20, 6

ingredients = ["egg", "tomato", "meat", "onion"]
ingredient_colors = {"egg": 10, "tomato": 8, "meat": 12, "onion": 7}

orders = [
    {"name": "オムレツ", "recipe": ["egg", "tomato"]},
    {"name": "ハンバーグ", "recipe": ["meat", "onion"]},
    {"name": "サラダ", "recipe": ["tomato", "onion"]},
]

current_order = random.choice(orders)
collected = []
falling_items = []

score = 0
time_limit = 60
start_time = time.time()
game_over = False

intro_text = [
    "こんにちは！私はシェフです。",
    "フライパンで食材をキャッチして、",
    "注文通りの料理を完成させてね！",
    "スペースキーでゲーム開始！"
]

complete_message = ""
complete_time = 0


def spawn_item():
    item = random.choice(ingredients)
    x = random.randint(0, W - 5)
    y = 0
    falling_items.append({"type": item, "x": x, "y": y})


def update():
    global pad_x, score, game_over, collected, current_order, state, start_time, complete_message, complete_time

    if state == "intro":
        if pyxel.btnp(pyxel.KEY_SPACE):
            state = "play"
            start_time = time.time()
        return

    if state == "gameover":
        if pyxel.btnp(pyxel.KEY_R):
            reset_game()
        return

    if game_over:
        state = "gameover"
        return

    if pyxel.btn(pyxel.KEY_LEFT):
        pad_x -= 2
    if pyxel.btn(pyxel.KEY_RIGHT):
        pad_x += 2

    if random.random() < 0.05:
        spawn_item()

    for item in falling_items:
        item["y"] += 2

    for item in falling_items[:]:
        if (pad_x <= item["x"] <= pad_x + pad_w and
            pad_y - 5 <= item["y"] <= pad_y):
            collected.append(item["type"])
            falling_items.remove(item)

            if set(collected) == set(current_order["recipe"]):
                score += 10
                complete_message = f"{current_order['name']} 完成！"
                complete_time = time.time()
                collected = []
                current_order = random.choice(orders)

        elif item["y"] > H:
            falling_items.remove(item)

    if time.time() - start_time > time_limit:
        game_over = True
        state = "gameover"


def draw():
    pyxel.cls(0)

    if state == "intro":
        # ここでキャラ画像を表示（例：64x72サイズ）
        pyxel.blt(40, 20, 0, 0, 0, 64, 72, 7)
        for i, line in enumerate(intro_text):
            pyxel.text(10, 100 + i*10, line, 7)
        return

    if state == "gameover":
        pyxel.text(W//2 - 30, H//2, "GAME OVER", 8)
        pyxel.text(W//2 - 40, H//2 + 10, f"SCORE: {score}", 7)
        pyxel.text(W//2 - 50, H//2 + 20, "Rキーでリスタート", 7)
        return

    pyxel.rect(pad_x, pad_y, pad_w, pad_h, 7)

    for item in falling_items:
        pyxel.rect(item["x"], item["y"], 5, 5, ingredient_colors[item["type"]])

    pyxel.text(5, 5, f"注文: {current_order['name']}", 11)
    pyxel.text(5, 15, f"レシピ: {','.join(current_order['recipe'])}", 7)

    pyxel.text(5, 30, f"SCORE: {score}", 7)
    remaining = int(time_limit - (time.time() - start_time))
    pyxel.text(5, 40, f"TIME: {remaining}", 8)

    pyxel.text(5, 55, f"集めた食材: {','.join(collected)}", 10)

    if complete_message and time.time() - complete_time < 2:
        pyxel.text(50, 80, complete_message, 10)


def reset_game():
    global pad_x, score, game_over, collected, current_order, falling_items, state, start_time
    pad_x = 70
    score = 0
    game_over = False
    collected = []
    current_order = random.choice(orders)
    falling_items = []
    state = "intro"
    start_time = time.time()


pyxel.init(W, H, title="Cooking Catch Game")
pyxel.load("assets.pyxres")  # ←ここを追加
pyxel.run(update, draw)
