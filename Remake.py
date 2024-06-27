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
    make_label(root, "Button Game")
    make_button(root, "Play", start)
    if "saves" in os.listdir():
        make_button(root, "Load", load_menu)
    else:
        os.mkdir("saves")
    make_button(root, "Quit", exit)

def load_menu():
    clear_screen()

    if os.listdir("saves"):
        for file in os.listdir("saves"):
            na = file.split(".")

            make_button(root, na[0], lambda: load("saves/" + na[0] + ".txt"))
    else:
        os.mkdir("saves")
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
def make_button(master, text, command):
    button = Button(master=master, text=text, command=command)


def make_label(master, text):
    label = Label(master=master, text=text)


def clear_screen():
    for i in range(len(buttons)):
        buttons[i].destroy()
    for i in range(len(labels)):
        labels[i].destroy()
    for i in range(len(images)):
        images[i].destroy()


# Game

def home():
    clear_screen()
    make_label(root, "Welcome to the Inn {}".format(name))
    make_button(root, "Rest", sleep)
    make_button(root, "Shop", shop)
    make_button(root, "Hunt", fight)
    make_button(root, "Stats", stats)
    make_button(root, "Spirit Refine", refine)
    make_button(root, "Cultivate", manaIncrease)
    make_button(root, "Inventory", stuff)


def refine():
    def refine_item(item, num):
        global mana
        mana = 0
        wl = randint(0, 1)
        if wl == 1:
            item.refinement += 1
            make_label(root, "{} upgraded to {}".format(item.name, inventory[num].refinement))
        else:
            make_label(root, "{} broke".format(inventory[num].name))
            inventory.remove(item)
        make_button(root, "Ok", home)

    clear_screen()
    make_label(root, "Select an item that will break or upgrade")
    for i in range(len(inventory)):
        make_button(root, inventory[i].name, lambda i=i: refine_item(inventory[i], i))


def manaIncrease():

    def sacrifice(sword, num):
        global maxMana
        maxMana += random.randint(1, 5) * sword
        del inventory[num]
        make_label(root, "Mana has been cultivated to {}".format(maxMana))
        make_button(root, "Ok", home)

    clear_screen()
    make_label(root, "Sacrifice an item")
    for i in range(len(inventory)):
        make_button(root, inventory[i].name, lambda: sacrifice(inventory[i].refinement, i))
    make_button(root, "Back", home)


def stats():
    global maxhp
    global hp
    global gold
    global level
    clear_screen()
    make_label(root, "You have {} max health and {} total".format(maxhp, hp))
    make_label(root, "You have {} gold".format(str(gold)))
    make_label(root, "You are level {}".format(str(level)))
    make_button(root, "That's Great", home)

def dungeon():
    dungeonFloors = [1,2,3,4,5]
    clear_screen()

def damage(monster, sword_damage, player_health, armor, use):
    monster.health -= sword_damage
    temp = armor
    temp -= monster.damage
    player_health += temp
    if use != "Hunt":
        return player_health, monster
    else:
        make_label(root, "The {} did {} reducing the player health to {}".format(monster.mtype, monster.damage, player_health))
        if monster.health <= 0:
            global gold
            make_label(root, "You vanquished the monster with an attack of {} damage".format(sword_damage))
            monster.damage = max(1, monster.damage)
            make_button(root, "Continue", lambda: add(g=random.randint(1, 5) * monster.damage))
            gold = gold//1
        else:
            make_label(root, "You hit the monster down to {} health with and attack of {} damage".format(monster.health, sword_damage))
            make_button(root, "Continue", lambda: fight_menu(monster))


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
    clear_screen()
    for i in range(len(inventory)):
        if inventory[i].type == "sword":
            make_button(root, inventory[i].name, lambda: damage(mon, inventory[i].damage, hp, armor, "Hunt"))
            print(inventory[i].damage)

def armor(monster):
    clear_screen()
    x = 0
    for i in range(len(inventory)):
       if inventory[i].type == "armor":
            make_button(root, inventory[i].name, lambda: sword(inventory[i].armor, monster))
            x += 1
    if x == 0:
        make_button(root, inventory[i].name, lambda: sword(0, monster))

def fight():
     global hp
     clear_screen()
     mon = create_monster()
     make_label(root, "A {} appeared it has {} health and {} damage".format(mon.mtype, mon.health, mon.damage))
     fight_menu(mon)


def fight_menu(monster):
    make_label(root, "The {} has {} health and {} attack damage".format(monster.mtype, monster.health, monster.damage))
    make_button(root, "Fight", lambda: armor(monster))

def sleep():
    global maxMana
    global mana
    global gold
    hp = maxhp
    mana = maxMana
    bgold = randint(1,5)
    gold += bgold
    clear_screen()
    make_label(root, ("Your health is {}".format(hp)))
    make_label(root, "You manu has recovered to {}".format(mana))
    make_label(root, "You gained {} gold".format(bgold))
    make_button(root, "Return", home)


def shop():
    global gold
    clear_screen()
    make_label(root, "You have {} gold".format(gold))
    make_button(root, "Sword", lambda: browse("Sword"))
    make_button(root, "Armors", lambda: browse("Armor"))

    def browse(type):
        clear_screen()
        global starter
        global gold
        print(type)
        if type == "Sword":
            make_label(root, "You have {} gold".format(gold))

            make_button(root, "Worn Sword", lambda: buy("Worn Sword", 10, 5, "sword", 0))
            make_button(root, "Steel Sword", lambda: buy("Steel Sword", 20, 10, "sword", 0))
            make_button(root, "Reinforced Blade", lambda: buy("Reinforced Blade", 30, 20, "sword", 0))
            make_button(root, "Battle Struck Blade", lambda: buy("Battle Struck Blade", 40, 25, "sword", 0))
            make_button(root, "Fluid like Moving Blade", lambda: buy("Fluid like Moving Blade", 50, 30, "sword", 0))
            make_button(root, "The Yellow Katana", lambda: buy("The Yellow Sword", 80, 50, "sword", 0))
        elif type == "Armor":
            make_label(root, "You have {} gold".format(gold))

            make_button(root, "Worn Armor", lambda: buy("Worn Armor", 10, 0, "armor", 2))
            make_button(root, "Steel Armor", lambda: buy("Steel Armor", 20, 0, "armor", 5))
            make_button(root, "Reinforced Armor", lambda: buy("Reinforced Armor", 30, 0, "armor", 8))
            make_button(root, "Battle Armor", lambda: buy("Battle Armor", 40, 0, "armor", 10))
            make_button(root, "Fluid like Moving Armor", lambda: buy("Fluid like Moving Armor", 50, 0, "armor", 12))
            make_button(root, "The Yellow Armor", lambda: buy("The Yellow Armor", 80, 0, "armor", 15))

        def buy(sword, price, damage, type, armor):
            global starter
            clear_screen()
            if type == "sword":
                make_label(root, "{} is {} Gold, with {} damage".format(sword, price, damage))
            if type == "armor":
                make_label(root, "{} is {} Gold, with {} protection".format(sword, price, armor))
            make_button(root, "Buy", lambda: comfirm(sword, price, damage, type, armor))
            make_button(root, "Exit", home)

        def comfirm(sword, price, damage, type, armor):
            global gold
            clear_screen()
            if gold > price or gold == price:
                gold -= price
                make_button(root, "Confirm",
                            lambda: add(item(name=sword, damage=damage, refinement=1, type=type, armor=armor)))
            else:
                make_button(root, "You can't afford this", home)


def add(item=None, g=0, use="home"):
    global gold
    clear_screen()
    if g > 0:
        gold += g
    if item != None:
        inventory.append(item)
    if use == "home":
        home()


def stuff():
    clear_screen()
    for i in range(len(inventory)):
        if inventory[i].type == "sword":
            make_label(root, (inventory[i].name + " with a damage of {}".format(inventory[i].damage)))
        else:
            make_label(root, inventory[i].name)
    make_button(root, "Exit", home)


def start():
    clear_screen()

    def enter():
        global name
        clear_screen()
        name = en.get()
        make_label(root, ("Hello " + en.get()))
        make_label(root, "You have {} Health".format(str(maxhp)))
        make_label(root, "You have {} Gold".format(str(gold)))
        make_label(root, "You have {} Mana".format(maxMana))
        make_button(root, "Ok", home)
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
        with open("saves/"+name+".txt", "w") as f:
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

def load(n):
    global gold
    global maxhp
    global maxMana
    global inventory
    global level
    global hp
    global starter
    global name
    clear_screen()
    with open(n, "r") as f:
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
    home()


root.protocol("WM_DELETE_WINDOW", on_closing)


if __name__ == "__main__":
    menu()

root.mainloop()
