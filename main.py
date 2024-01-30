# Imports
import tkinter as tk
from random import randint
from sys import exit

# Startup
root = tk.Tk()
root.title("Adventure Game")
root.geometry('500x300')

# Variables and Lists

global gold
maxhp = 0
hp = 0
inventory = []
buttons = []
labels = []

# Classes
def menu():
    makeLabel(root, "Button Game")
    makeButton(root, "Play", start)
    makeButton(root, "Quit", exit)

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

    def display(self):
        label = tk.Label(root, text=self.text)
        label.pack()
        labels.append(label)

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

# Menu


def sleep():
    global hp
    global maxhp
    clearScreen()
    makeLabel(root, "Health {} --> {}".format(hp, maxhp))
    hp = maxhp
    makeButton(root, "Ok", home)


def buy(sword, price):
    global gold
    if gold > price:
        clearScreen()
        makeLabel(root, "{} Added to Inventory, for {} Gold".format(sword, str(price)))
        gold -= price

        inventory.append(sword)
        print(inventory)
        makeButton(root, "Ok", home)

    elif gold == price:
        clearScreen()
        makeLabel(root, "{} Added to Inventory, for {} Gold".format(sword, str(price)))
        gold -= price

        inventory.append(sword)
        print(inventory)
        makeButton(root, "Ok", home)

    else:
        clearScreen()
        makeLabel(root, "You can't afford {}".format(sword))
        makeButton(root, "Ok", shop)


def shop():
    global gold
    clearScreen()

    def sword_armour(sword, cost):
        clearScreen()
        makeLabel(root, "Would you like to buy the {}".format(sword))
        makeButton(root, "Yes", lambda: buy(sword, cost))

    def weapons():
        clearScreen()
        makeLabel(root, "Weapons")
        makeButton(root, "Worn Sword 10", lambda: sword_armour("Worn Sword", 10))
        makeButton(root, "Steel Sword 20", lambda: sword_armour("Steel Sword", 20))
        makeButton(root, "Rune-Engraved Blade 40", lambda: sword_armour("Rune Engraved Blade", 40))
        makeButton(root, "Blood-Slayer Blade 60", lambda: sword_armour("Blood-Slayer Blade", 60))
        makeButton(root, "Back", shop)

    def armour():
        clearScreen()
        makeLabel(root, "Armours")
        makeButton(root, "Shattered Armour 10", lambda: sword_armour("Shattered Armour", 10))
        makeButton(root, "Battle Worn Armour 20", lambda: sword_armour("Battle-Worn Armour", 20))
        makeButton(root, "Steel-Plated Armour 40", lambda: sword_armour("Steel-Plated Armour", 40))
        makeButton(root, "Blood-Slayer Armour 60", lambda: sword_armour("Blood-Slayer Armour", 60))
        makeButton(root, "Back", shop)
    item = []
    price = []
    makeLabel(root, "Shop")
    makeLabel(root, "You have {} Gold".format(gold))
    makeButton(root, "Weapons", weapons)
    makeButton(root, "Armours", armour)
    makeButton(root, "Back", home)


def stuff():
    clearScreen()
    if len(inventory) == 0:
        home()
    for i in range(len(inventory)):
        makeLabel(root, inventory[i])
    makeButton(root, "Back", home)


# Battle System

def swordAttack(weapon):
    global chp
    weapons = ['Worn', 'Steel', 'Rune-Engraved', 'Blood-Slayer']
    damage = [5, 10, 15, 25]
    for i in range(weapons):
        print(str(i))
        if weapon == weapons[int(i)]:
            chp -= damage[i]

def attack():
    global chp
    clearScreen()
    for i in range(len(inventory)):
        x = inventory[i].split()
        for z in range(len(x)):
            if x[z] == 'Blade':
                makeButton(root, x[1], lambda : swordAttack(inventory[i]))
                print(x[1])
            elif x[z] == 'Sword':
                makeButton(root, x[1], lambda : swordAttack(inventory[i]))

def fight():
    global chp
    clearScreen()
    chp = randint(10, 20)
    creatures = ['Vampires', 'Golem', 'Dark Energy', 'Reaper', 'Knight']
    creature = creatures[randint(0,4)]
    level = 1
    makeLabel(root, "A level {}, {} appeared".format(str(level), creature))
    makeButton(root, "Fight", lambda : attack())


def home():
    clearScreen()
    makeButton(root, "To Bed", sleep)
    makeButton(root, "Shop", shop)
    makeButton(root, "Dungeon", fight)
    makeButton(root, "Inventory", stuff)

def start():

    clearScreen()

    def enter():

        clearScreen()
        makeLabel(root, ("Hello " + en.get()))
        makeLabel(root, "You have {} Health".format(str(maxhp)))
        makeLabel(root, "You have {} Gold".format(str(gold)))
        makeButton(root, "Ok", home)
        en.destroy()

    global gold
    global hp
    global maxhp
    maxhp = randint(20, 40)
    hp = maxhp
    gold = randint(35, 60)

    en = tk.Entry(root)
    en.pack()

    button = tk.Button(root, text="Enter", command=enter)
    button.pack()

    buttons.append(button)


print(buttons)

if __name__ == "__main__":
    menu()
    root.mainloop()
