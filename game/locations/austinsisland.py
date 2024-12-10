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

        

       

  
    
   # def process_verb (self, verb, cmd_list, nouns):
       # if verb == "search" and not self.key_found:
         #   self.key_found = True
           # display.announce("You have searched the jail and found a important key")
            #config.the_player.inventory.append(self.key)
       # elif verb == 'unlocked' and self.cell_locked and "key" in nouns:
#            if any(item.name == "cell_key" for item in config.the_player.inventory):
 #               self.cell_locked = False
  #              display.announce ("If you have a key why not trying to use it on the cell door")
   #         else:
    #            display.announce (" You don't have what is required to unlock the cell")
     #   elif verb == "enter" and not self.cell_locked:
      #    display.announce ("You entered the cell")
       # elif verb == "enter" and self.cell_locked:
        #    display.announce ("The cell door is locked, you must unlock it")
class OutsideJail (location.SubLocation):
    def __init__ (self, m):
        self.name = "jail"
        self.verbs['exit'] = self
        self.verbs['leave'] = self
    
    def enter (self):
        description = "You walk upon the center of the island.\nA worn-down jail that has a sign that reads STAY AWAY, DON'T GIVE THE GIANT BOOZE! /nYou can enter it."
        display.announce(description)
class JainEntryAndCells (location.SubLocation):
    def __init__ (self, m):
        self.cell_locked = True
        self.alchohlic_name = "alchohlic"
        self.alchohlic_decription = "A very massive guy that is very shaky and doesn't speak a word"
        self.alcoholic_helping = False
        self.booze = "Bottle of Booze"
    def process_verb (self, verb, cmd_list, nouns):
        if verb == 'unlock' and self.cell_locked and "key" in nouns:
            if any(item.name == "cell_key" for item in config.the_player.inventory):
                self.cell_locked = False
                display.announce ("If you have a key why not trying to use it on the cell door")
            else:
                display.announce (" You don't have what is required to unlock the cell")
        elif verb == "enter":
            if self.cell_locked:
               display.announce ("The cell door is locked, you must unlock it")
            else:
                display.announce ("You entered the cell")
    
    def process_verb(self, verb, cmd_list, nouns):
        if verb == "give" and "booze" in nouns:
            if self.booze in config.the_player.inventory:
                config.the_player.inventory.remove(self.booze)
                self.alcoholic_helping = True 
                display.announce("The alcoholic takes the booze and is ready to help you!")
                config.the_player.add_crewmate("Alcoholic")
            else: 
                display.announce("You don't have any booze to give.")

    def trigger_combat_help(self):
        if self.alcoholic_helping:
            display.announce("the alcaholic comes to help you fight.")
            combat.increase_player_damage(10)
        else:
            display.announce(" Alcaholic is not helping because he is not part of your crew. ")


class JailOffice (location.SubLocation):
    def __init__ (self, m):
        self.key = Key()
        self.key_found = False
    def process_verb (self, verb, cmd_list, nouns):
        if verb == "search" and not self.key_found:
            self.key_found = True
            display.announce("You have searched the jail and found a important key")
            config.the_player.inventory.append(self.key)
        elif verb == "search":
            display.announce("You have already found the key.")
        
    

class Debris_pile (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "debris"
        self.verbs['search'] = self
        self.booze = "Bottle of booze"
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "search" ):
           if self.booze not in config.the_player.inventory:
               c
               config.the_player.inventory.append(self.booze)
               display.announce ("You have searched the debris pile, /nyou have found one bottle of booze and a bunch of trash")
        else: 
            display.announce ("You have searched the debris pile, and already have the booze.")

class store (location.Sublocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "store"
        self.loot = "Pot of Gold"
        self.battle_triggered = False
    
    def enter(self):
        display.announce("You are entering the store, it is very quiet.")

    def process_verb (self, verb, cmd_list, nouns):
        if not self.battle_triggered and verb == "search":
            display.announce("As you search the store, you find a group of enemies! ")
            self.battle_triggered = True
            combat.start.combat_with_enemies["pirate", "theif"]
        if combat.player_wins():
            display.announce(" You have won the fight! You found a Pot of Gold behind the counter")
            config.the_player.inventory.append(self.loot)
        else:
            display.announce("You died")
# I want to make the user and the alcaholic fight something in the store if they win they get a pot of gold

