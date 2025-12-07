import pyxel

class Game:
    def __init__(self):
        self.state = "title"  # title, select, stage, result
        self.stage = None
        pyxel.init(160, 120)
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.state == "title":
            if pyxel.btnp(pyxel.KEY_RETURN):  # スタートボタン
                self.state = "select"
        elif self.state == "select":
            if pyxel.btnp(pyxel.KEY_1):
                self.stage = "runner"
                self.state = "stage"
            elif pyxel.btnp(pyxel.KEY_2):
                self.stage = "forest"
                self.state = "stage"
            elif pyxel.btnp(pyxel.KEY_3):
                self.stage = "ocean"
                self.state = "stage"
            elif pyxel.btnp(pyxel.KEY_4):
                self.stage = "co2"
                self.state = "stage"
        elif self.state == "stage":
            # 各ステージの処理を呼び出す
            pass
        elif self.state == "result":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.state = "select"

    def draw(self):
        pyxel.cls(0)
        if self.state == "title":
            pyxel.text(50, 60, "環境アクションゲーム", 7)
            pyxel.text(40, 80, "Press ENTER to Start", 10)
        elif self.state == "select":
            pyxel.text(20, 20, "ステージを選んでください", 11)
            pyxel.text(20, 40, "1: ゴミ拾いランナー", 7)
            pyxel.text(20, 50, "2: 森を守るヒーロー", 3)
            pyxel.text(20, 60, "3: 海洋クリーンアップ", 6)
            pyxel.text(20, 70, "4: CO2バスター", 8)
        elif self.state == "stage":
            pyxel.text(40, 60, f"Stage: {self.stage}", 7)
        elif self.state == "result":
            pyxel.text(40, 60, "結果画面", 7)
Game()