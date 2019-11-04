# TO DO: create loot


class Weapon:
    def __init__(self):
        self.name = None
        raise NotImplementedError("Do not create raw Weapon objects.")

    def __str__(self):
        return self.name


class Consumable:
    def __init__(self):
        self.healing_value = None
        self.name = None
        raise NotImplementedError("Do not create raw Consumable objects.")

    def __str__(self):
        return "{} (+{} HP)".format(self.name, self.healing_value)


class Armor:
    def __init__(self):
        self.name = None
        self.protective_value = 1
        raise NotImplementedError("Do not create raw Armor objects")

    def __str__(self):
        return "{} (-{} Reduces Damage)".format(self.name, self.protective_value)


class CrustyBread(Consumable):
    def __init__(self):
        self.name = "Crusty Bread"
        self.healing_value = 10


class Rock(Weapon):
    def __init__(self):
        self.name = "Rock"
        self.description = "A fist-sized rock, suitable for bludgeoning."
        self.damage = 5
        self.value = 1


class Dagger(Weapon):
    def __init__(self):
        self.name = "Dagger"
        self.description = "A small dagger with some rust. Somewhat more dangerous than a rock."
        self.damage = 10
        self.value = 20


class RustySword(Weapon):
    def __init__(self):
        self.name = "Rusty Sword"
        self.description = "This sword is showing its age. But it still has some fight in it."
        self.damage = 20
        self.value = 100


class HealingPotion(Consumable):
    def __init__(self):
        self.name = "Healing Potion"
        self.healing_value = 50
        self.value = 60


class Helm(Armor):
    def __init__(self):
        self.name = "Helm"
        self.protective_value = 2
        self.value = 50


class ChestArmor(Armor):
    def __init__(self):
        self.name = "Chest Armor"
        self.protective_value = 5
        self.value = 200


class Boots(Armor):
    def __init__(self):
        self.name = "Boots"
        self.protective_value = 3
        self.value = 50
