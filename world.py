import random
import enemies
import npc


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro_text(self):
        return """
            You find yourself in a cave with a flickering torch on the wall. \n
            You can make out four paths, each equally as dark and foreboding.
        """


class BoringTile(MapTile):
    def intro_text(self):
        return """
                This is a very boring part of the cave.
            """


class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        self.gold_claimed = True
        player.gold = player.gold + self.gold
        print("+{} gold added".format(self.gold))

    def intro_text(self):
        if self.gold_claimed:
            return """
                Another unremarkable part of the cave. You must forge onwards.
            """
        else:
            return """
            Someone dropped some gold. You pick it up.
        """


class TraderTile(MapTile):
    def __init__(self, x, y):
        self.trader = npc.Trader()
        super.__init__(x,y)

    def intro_text(self):
        return """
                A frail not quite-human, not quite creature squats in the corner. \n
                Clinking his gold coins together, he looks willing to trade. 
            """

    def swap(self, seller, buyer, item):
        if item.value > buyer.gold:
            print("That's too expensive")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold = seller.gold + item.value
        buyer.gold = buyer.gold - item.value
        print("Trade complete!")

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {}".format(i, item.name, item.value))
        while True:
            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['q', 'Q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print("Invalid choice!")

    def check_if_trade(self, player):
        while True:
            print("Would you like to (B)uy, (S)ell, or (Q)uit?")
            user_input = input()
            if user_input in ['q''Q']:
                return
            elif user_input in ['b', 'B']:
                print("Here's what available to buy: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['s', 'S']:
                print("Here's what's available to sell: ")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid choice!")


class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True

    def intro_text(self):
        return """
                You see a bright light in the distance... \n
                ... it grows as you get closer! It's sunlight!\n
                \n
                Victory is yours!
            """


# TO DO: create loot when npc is dead
class EnemyTile(MapTile):
    def intro_text(self):
        if self.enemy.is_alive():
            return "A {} awaits!".format(self.enemy.name)
        else:
            return "You've defeated the {}".format(self.enemy.name)

    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "A giant spider jumps down from its web in front of you!"
            self.dead_text = "The corpse of a dead spider rots on the ground."
        elif r < 0.80:
            self.enemy = enemies.Ogre()
            self.alive_text = "An ogre is blocking your path!"
            self.dead_text = "A dead ogre reminds you of your triumph"
        elif r < 0.95:
            self.enemy = enemies.BatColony()
            self.alive_text = "You hear a squeaking noise growing louder ... \n" \
                              "suddenly you are lost in a swarm of bats!"
            self.dead_text = "Dozens of dead bats are scattered on the ground."
        else:
            self.enemy = enemies.RockMonster()
            self.alive_text = "You've disturbed a rock monster from his slumber"
            self.dead_text = "Defeated, the monster has reverted into an ordinary rock."

        super().__init__(x, y)

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, player.hp))


def at_tile(x,y):
    if x < 0 or y <0:
        return None

    try:
        return world_map[y][x]
    except IndexError:
        return None


world_dsl = """
|EN|EN|VT|EN|EN|
|EN|BT|BT|BT|EN|
|EN|FG|EN|BT|TT|
|TT|BT|ST|FG|EN|
|FG|BT|EN|BT|FG|
"""

world_map = []

title_type_dict = {
    "VT": VictoryTile,
    "EN": EnemyTile,
    "ST": StartTile,
    "BT": BoringTile,
    "FG": FindGoldTile,
    "TT": TraderTile,
    " ": None
}


def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|VT|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True


def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = title_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)

