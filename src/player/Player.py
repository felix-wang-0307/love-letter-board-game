# player.py
class Player:
    def __init__(self, player_id, name, connection):
        self.player_id = player_id
        self.name = name
        self.hand = []
        self.discards = []
        self.is_protected = False  # 是否是保护的状态（即该轮打出侍女）
        self.is_alive = True  # 是否存活
        self.connection = connection  # WebSocket connection

    def draw_card(self, card):
        self.hand.append(card)

    def play_card(self, card_index):
        card = self.hand.pop(card_index)
        card.on_play(self)
        self.discards.append(card)
    
    def start_turn(self):
        self.is_protected = False
        self.draw_card()
        self.connection.send(f"Your hand: {self.hand}")

    def __repr__(self):
        return f"Player({self.name})"


