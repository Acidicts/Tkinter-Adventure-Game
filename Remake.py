# Imports
import ast
import os
import random
import tkinter as tk
from random import randint
from sys import exit

# Startup
root = tk.Tk()
root.title("Adventure Game")
root.geometry('500x300')
root.resizable(True, True)

# Variables and Lists

global gold
global name
level = 0.1
maxhp = 0
hp = 0
inventory = []
buttons = []
labels = []
images = []
name = ""


def menu():
    makeLabel(root, "Button Game")
    makeButton(root, "Play", start)
    if os.path.exists("data.txt"):
        makeButton(root, "Load", load)
    makeButton(root, "Quit", exit)


# Classes

class Button(tk.Button):
    def __init__(self, master, text, command):
        super().__init__(command=command, text=text)
        self.text = text
        self.command = command
        self.root = master
        self.button = tk.Button(self.root, text=self.text, command=self.command)
        self.make()

    def make(self):
        self.button.pack()
        buttons.append(self.button)
        print(self.button)


class Canvas(tk.Canvas):
    def __init__(self, master, width, height, bg):
        super().__init__(master, bg=bg, height=height, width=width)
        self.canvas = None
        self.width = width
        self.height = height
        self.root = master
        self.bg = bg
        self.display()

    def display(self):
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg=self.bg)
        self.canvas.pack()


class Label(tk.Label):
    def __init__(self, master, text):
        super().__init__(text=text)
        self.text = text
        self.display()
        self.root = master

    def display(self):
        label = tk.Label(root, text=self.text)
        label.pack()
        labels.append(label)


class item:
    def __init__(self, name, damage, type, refinement, armor):
        self.name = name
        self.refinement = refinement
        self.damage = damage * self.refinement
        self.type = type
        self.armor = armor * refinement
        if self.type == "spell":
            if 'frost' in name:
                self.spell = 'frost'
                self.manaConsumption = 10
            if 'fire' in name:
                self.spell = 'fire'
                self.manaConsumption = 15
            if 'life' in name:
                self.spell = 'life'
                self.manaConsumption = 20
            if 'death' in name:
                self.spell = 'death'
                self.manaConsumption = 50
                self.damage = 1000
            if 'disintegration' in name:
                self.spell = 'death'
                self.manaConsumption = 100
                self.damage = 10000

    def to_dict(self):
        return {'name': self.name,
                'refinement': self.refinement,
                'type': self.type,
                'damage': self.damage,
                'armor': self.armor}


class Monster:
    def __init__(self, type, hp, dp):
        self.mtype = type
        self.health = hp
        self.damage = dp


# Basic Functions
def makeButton(master, text, command):
    button = Button(master=master, text=text, command=command)


def makeLabel(master, text):
    label = Label(master=master, text=text)


def clearScreen():
    for i in range(len(buttons)):
        buttons[i].destroy()
    for i in range(len(labels)):
        labels[i].destroy()
    for i in range(len(images)):
        images[i].destroy()


# Game

def home():
    clearScreen()
    makeLabel(root, "Welcome to the Inn {}".format(name))
    makeButton(root, "Rest", sleep)
    makeButton(root, "Shop", shop)
    makeButton(root, "Hunt", fight)
    makeButton(root, "Stats", stats)
    makeButton(root, "Spirit Refine", refine)
    makeButton(root, "Cultivate", manaIncrease)
    makeButton(root, "Inventory", stuff)


def refine():
    def refine(item, num):
        global mana
        mana = 0
        wl = randint(0, 1)
        if wl == 1:
            item.refinement += 1
            makeLabel(root, "{} upgraded to {}".format(inventory[num].name, inventory[num].refinement))
            pass
        else:
            makeLabel(root, "{} broke".format(inventory[num].name))
            del inventory[num]
        makeButton(root, "Ok", home)

    clearScreen()
    makeLabel(root, "Select an item that will break or upgrade")
    for i in range(len(inventory)):
        makeButton(root, inventory[i].name, lambda: refine(inventory[i], i))


def manaIncrease():

    def sacrifice(sword, num):
        global maxMana
        maxMana += random.randint(1, 5) * sword
        del inventory[num]
        makeLabel(root, "Mana has been cultivated to {}".format(maxMana))
        makeButton(root, "Ok", home)

    clearScreen()
    makeLabel(root, "Sacrifice an item")
    for i in range(len(inventory)):
        makeButton(root, inventory[i].name, lambda: sacrifice(inventory[i].refinement, i))
    makeButton(root, "Back", home)


def stats():
    global maxhp
    global hp
    global gold
    global level
    clearScreen()
    makeLabel(root, "You have {} max health and {} total".format(maxhp, hp))
    makeLabel(root, "You have {} gold".format(str(gold)))
    makeLabel(root, "You are level {}".format(str(level)))
    makeButton(root, "That's Great", home)

def dungeon():
    dungeonFloors = [1,2,3,4,5]
    clearScreen()

def damage(monster, sword_damage, player_health, armor, use):
    monster.health -= sword_damage
    temp = armor
    temp -= monster.damage
    player_health += temp
    if use != "Hunt":
        return player_health, monster
    else:
        makeLabel(root, "The {} did {} reducing the player health to {}".format(monster.mtype, monster.damage, player_health))
        if monster.health <= 0:
            makeLabel(root, "You vanquished the monster with an attack of {} damage".format(sword_damage))
            makeButton(root, "Continue", lambda: add(g=random.randint(1,5) * monster.damage/monster.health))
        else:
            makeLabel(root, "You hit the monster down to {} health with and attack of {} damage".format(monster.health, sword_damage))
            makeButton(root, "Continue", lambda: fight_menu(monster))


def create_monster():
    global level
    monsters = ["Vampire", "Zombie", "Golem", "Ogre"]
    hp = randint(1,10) * level * 5 // 1
    if level < 1:
        dp = randint(1,5) * level * 10 // 1
    else:
        dp = randint(1, 5) * level // 1
    print("{} {}".format(dp, hp))

    return Monster(random.choice(monsters), hp, dp)

def sword(armor, mon):
    clearScreen()
    for i in range(len(inventory)):
        if inventory[i].type == "sword":
            makeButton(root, inventory[i].name, lambda: damage(mon, inventory[i].damage, hp, armor, "Hunt"))
            print(inventory[i].damage)

def armor(monster):
    clearScreen()
    x = 0
    for i in range(len(inventory)):
       if inventory[i].type == "armor":
            makeButton(root, inventory[i].name, lambda: sword(inventory[i].armor, monster))
            x += 1
    if x == 0:
        makeButton(root, inventory[i].name, lambda: sword(0, monster))

def fight():
     global hp
     clearScreen()
     mon = create_monster()
     makeLabel(root, "A {} appeared it has {} health and {} damage".format(mon.mtype, mon.health, mon.damage))
     fight_menu(mon)


def fight_menu(monster):
    makeLabel(root, "The {} has {} health and {} attack damage".format(monster.mtype, monster.health, monster.damage))
    makeButton(root, "Fight", lambda: armor(monster))

def sleep():
    global maxMana
    global mana
    global gold
    hp = maxhp
    mana = maxMana
    bgold = randint(1,5)
    gold += bgold
    clearScreen()
    makeLabel(root, ("Your health is {}".format(hp)))
    makeLabel(root, "You manu has recovered to {}".format(mana))
    makeLabel(root, "You gained {} gold".format(bgold))
    makeButton(root, "Return", home)


def shop():
    global gold
    clearScreen()
    makeLabel(root, "You have {} gold".format(gold))
    makeButton(root, "Sword", lambda: browse("Sword"))
    makeButton(root, "Armors", lambda: browse("Armor"))

    def browse(type):
        clearScreen()
        global starter
        global gold
        print(type)
        if type == "Sword":
            makeLabel(root, "You have {} gold".format(gold))

            makeButton(root, "Worn Sword", lambda: buy("Worn Sword", 10, 5, "sword", 0))
            makeButton(root, "Steel Sword", lambda: buy("Steel Sword", 20, 10, "sword", 0))
            makeButton(root, "Reinforced Blade", lambda: buy("Reinforced Blade", 30, 20, "sword", 0))
            makeButton(root, "Battle Struck Blade", lambda: buy("Battle Struck Blade", 40, 25, "sword", 0))
            makeButton(root, "Fluid like Moving Blade", lambda: buy("Fluid like Moving Blade", 50, 30, "sword", 0))
            makeButton(root, "The Yellow Katana", lambda: buy("The Yellow Sword", 80, 50, "sword", 0))
        elif type == "Armor":
            makeLabel(root, "You have {} gold".format(gold))

            makeButton(root, "Worn Armor", lambda: buy("Worn Armor", 10, 0, "armor", 2))
            makeButton(root, "Steel Armor", lambda: buy("Steel Armor", 20, 0, "armor", 5))
            makeButton(root, "Reinforced Armor", lambda: buy("Reinforced Armor", 30, 0, "armor", 8))
            makeButton(root, "Battle Armor", lambda: buy("Battle Armor", 40, 0, "armor", 10))
            makeButton(root, "Fluid like Moving Armor", lambda: buy("Fluid like Moving Armor", 50, 0, "armor", 12))
            makeButton(root, "The Yellow Armor", lambda: buy("The Yellow Armor", 80, 0, "armor", 15))

        def buy(sword, price, damage, type, armor):
            global starter
            clearScreen()
            if type == "sword":
                makeLabel(root, "{} is {} Gold, with {} damage".format(sword, price, damage))
            if type == "armor":
                makeLabel(root, "{} is {} Gold, with {} protection".format(sword, price, armor))
            makeButton(root, "Buy", lambda: comfirm(sword, price, damage, type, armor))
            makeButton(root, "Exit", home)

        def comfirm(sword, price, damage, type, armor):
            global gold
            clearScreen()
            if gold > price or gold == price:
                gold -= price
                makeButton(root, "Confirm",
                           lambda: add(item(name=sword, damage=damage, refinement=1, type=type, armor=armor)))
            else:
                makeButton(root, "You can't afford this", home)


def add(item=None,g=0, use="home"):
    global gold
    clearScreen()
    gold += g
    if item != None:
        inventory.append(item)
    if use == "home":
        home()


def stuff():
    clearScreen()
    for i in range(len(inventory)):
        if inventory[i].type == "sword":
            makeLabel(root, (inventory[i].name + " with a damage of {}".format(inventory[i].damage)))
        else:
            makeLabel(root, inventory[i].name)
    makeButton(root, "Exit", home)


def start():
    clearScreen()

    def enter():
        global name
        clearScreen()
        name = en.get()
        makeLabel(root, ("Hello " + en.get()))
        makeLabel(root, "You have {} Health".format(str(maxhp)))
        makeLabel(root, "You have {} Gold".format(str(gold)))
        makeLabel(root, "You have {} Mana".format(maxMana))
        makeButton(root, "Ok", home)
        en.destroy()

    global maxMana
    global mana
    global gold
    global hp
    global maxhp
    global starter
    starter = True
    maxhp = randint(20, 40)
    maxMana = randint(-5, 10)
    mana = maxMana
    hp = maxhp
    gold = randint(35, 60)

    en = tk.Entry(root)
    en.pack()

    button = tk.Button(root, text="Enter", command=enter)
    button.pack()

    add(item("Starter Sword", 1, "sword", 1, 0),0,"_")
    add(item("Starter Armor", 0, "armor", 1, 1), 0, "_")

    buttons.append(button)

def dict_to_item(item_dict):
    return item(name=item_dict['name'],
                damage=item_dict['damage'],
                type=item_dict['type'],
                refinement=item_dict['refinement'],
                armor=item_dict['armor'])

# Save and Load
def on_closing():
    global name
    items = [item.to_dict() for item in inventory]
    try:
        with open("data.txt", "w") as f:
            f.write("Gold: {}\n".format(gold))
            f.write("Max Health: {}\n".format(maxhp))
            f.write("Max Mana: {}\n".format(maxMana))
            f.write("Inventory: {}\n".format(items))
            f.write("Level: {}\n".format(level))
            f.write("HP: {}\n".format(hp))
            f.write("Starter: {}\n".format(starter))
            f.write("Name: {}\n".format(name))

        print("Saving data...")
        root.destroy()
    except Exception as e:
        print(e)
        root.destroy()

def load():
    global gold
    global maxhp
    global maxMana
    global inventory
    global level
    global hp
    global starter
    global name
    clearScreen()
    with open("data.txt", "r") as f:
        for line in f:
            if "Gold" in line:
                gold = int(line[6:])
            elif "Max Health" in line:
                maxhp = int(line[12:])
            elif "Max Mana" in line:
                maxMana = int(line[10:])
            elif "Inventory" in line:
                inventory = [dict_to_item(item) for item in ast.literal_eval(line[11:].strip())]
            elif "Level" in line:
                level = float(line[7:])
            elif "HP" in line:
                hp = int(line[4:])
            elif "Starter" in line:
                starter = bool(line[9:])
            elif "Name" in line:
                name = line[6:-1]
    os.remove("data.txt")
    home()


root.protocol("WM_DELETE_WINDOW", on_closing)


if __name__ == "__main__":
    menu()

root.mainloop()
