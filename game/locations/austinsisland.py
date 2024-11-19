from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
import random

class AustinsIsland (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "AustinsIsland"
        self.symbol = 'I'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach_with_ship(self)
        self.locations["jail"] = Jail(self)

        self.starting_location = self.locations["beach"]

    def enter (self, ship):
        display.announce ("arrived at an AustinsIsland", pause=False)

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        

    def enter (self):
        display.announce ("arrive at the beach. Your ship is at anchor in a small bay to the south.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship.")
            self.main_location.end_visit()
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["jail"]
        elif (verb == "east" or verb == "west"):
            display.announce ("You walk all the way around the island on the beach. It's not very interesting.")
class Key:
    def __init__ (self, m):
        self.name = "Cell key"
        description = "A small rusty key on a big key ring"
        display.announce(description)

       
class Jail (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "jail"
        self.verbs['exit'] = self
        self.verbs['leave'] = self
        self.key_found = False
        self.cell_locked = True
        self.key = Key()
        self.alchohlic_name = "alchohlic"
        self.alchohlic_decription = "A very massive guy that is very shaky and doesn't speak a word"
    def enter (self):
        description = "You walk upon the center of the island.\nA worn-down jail that has a sign that reads STAY AWAY, DON'T GIVE THE GIANT BOOZE! /nYou can enter it."
        display.announce(description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if verb == "search" and not self.key_found:
            self.key_found = True
            display.announce("You have searched the jail and found a important key")
            config.the_player.inventory.append(self.key)
        elif verb == 'unlocked' and self.cell_locked and "key" in nouns:
            if any(item.name == "cell_key" for item in config.the_player.inventory):
                self.cell_locked = False
                display.announce ("If you have a key why not trying to use it on the cell door")
            else:
                display.announce (" You don't have what is required to unlock the cell")
        elif verb == "enter" and not self.cell_locked:
            display.announce ("You entered the cell")
        elif verb == "enter" and self.cell_locked:
            display.announce ("The cell door is locked, you must unlock it")
class Debris_pile (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "debris"
        self.verbs['search'] = self
        self.booze = "Bottle of booze"
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "search" ):
           if self.booze not in config.the_player.inventory:
               config.the_player.inventory.append(self.booze)
           display.announce ("You have searched the debris pile, /nyou have found one bottle of booze and a bunch of trash")
        else: 
            display.announce ("You have searched the debris pile, and already have the booze.")


