import random

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.money = 1000  # Starting money
        self.areas = []  # List of owned areas
        self.points = {
            'Impact': 0,
            'Valuation': 0,
            'Expansion': 0,
            'Bonus': 0
        }

    def total_points(self):
        return sum(self.points.values())

    def add_points(self, category, amount):
        if category in self.points:
            self.points[category] += amount

class Area:
    def __init__(self, id, cost, center_bonus=False):
        self.id = id
        self.cost = cost
        self.owner = None
        self.business_level = 1
        self.center_bonus = center_bonus

    def upgrade_cost(self):
        return self.business_level * 200

    def upgrade_business(self):
        if self.business_level < 5:  # Max level is 5
            self.business_level += 1
            return True
        return False

class Game:
    def __init__(self, players, hex_map_size=7):
        self.players = players
        self.hex_map = self.generate_hex_map(hex_map_size)
        self.turn_order = players
        self.current_turn = 0
        self.opportunity_deck = self.generate_opportunity_deck()

    def generate_hex_map(self, size):
        hex_map = []
        for i in range(size):
            cost = 100 + (i * 50)  # Increase cost for areas closer to the center
            center_bonus = (i == size // 2)  # Center tile bonus
            hex_map.append(Area(i, cost, center_bonus))
        return hex_map

    def generate_opportunity_deck(self):
        return [f"Complete task {i} for bonus points" for i in range(1, 31)]

    def draw_opportunity_cards(self):
        return random.sample(self.opportunity_deck, 3)

    def trade_area(self, from_player, to_player, area_id):
        area = self.hex_map[area_id]
        if area.owner == from_player:
            from_player.areas.remove(area)
            to_player.areas.append(area)
            area.owner = to_player

    def play_turn(self):
        player = self.turn_order[self.current_turn]
        print(f"{player.name}'s turn! Money: ${player.money}, Total Points: {player.total_points()}")
        
        # Display available actions
        print("1. Buy Area\n2. Upgrade Business\n3. Draw Opportunity Card\n4. End Turn")
        choice = int(input("Choose an action: "))
        
        if choice == 1:
            self.buy_area(player)
        elif choice == 2:
            self.upgrade_business(player)
        elif choice == 3:
            self.draw_opportunity(player)
        elif choice == 4:
            print("Turn ended.")
        else:
            print("Invalid choice.")

        # Move to the next player
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def buy_area(self, player):
        available_areas = [area for area in self.hex_map if area.owner is None]
        if not available_areas:
            print("No areas available to buy.")
            return

        print("Available Areas:")
        for area in available_areas:
            print(f"Area {area.id}: Cost ${area.cost}")

        choice = int(input("Enter the ID of the area you want to buy: "))
        area = self.hex_map[choice]
        
        if player.money >= area.cost:
            player.money -= area.cost
            player.areas.append(area)
            area.owner = player
            player.add_points('Expansion', 1)
            print(f"You bought Area {area.id}!")
        else:
            print("Not enough money to buy this area.")

    def upgrade_business(self, player):
        if not player.areas:
            print("You don't own any areas to upgrade.")
            return

        print("Your Areas:")
        for area in player.areas:
            print(f"Area {area.id}: Business Level {area.business_level}, Upgrade Cost ${area.upgrade_cost()}")

        choice = int(input("Enter the ID of the area you want to upgrade: "))
        area = self.hex_map[choice]

        if area in player.areas and player.money >= area.upgrade_cost():
            player.money -= area.upgrade_cost()
            area.upgrade_business()
            player.add_points('Valuation', 1)
            print(f"Upgraded business in Area {area.id} to Level {area.business_level}!")
        else:
            print("Cannot upgrade this business.")

    def draw_opportunity(self, player):
        cards = self.draw_opportunity_cards()
        print("Opportunity Cards:")
        for i, card in enumerate(cards):
            print(f"{i + 1}. {card}")

        choice = int(input("Choose a card (1-3): "))
        print(f"You chose: {cards[choice - 1]}!")
        player.add_points('Bonus', 5)

# Initialize players and game
players = [Player("Alice", "Red"), Player("Bob", "Blue"), Player("Charlie", "Green")]
game = Game(players)

# Game loop
while all(player.total_points() < 50 for player in players):
    game.play_turn()

# Determine winner
winner = max(players, key=lambda p: p.total_points())
print(f"{winner.name} wins with {winner.total_points()} points!")
