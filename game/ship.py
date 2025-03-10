
import random
from game.context import Context
import game.display as display
import game.config as config

class Ship (Context):
    '''The pirate ship. Mostly handles food and sailing around the ocean map.'''
    def __init__(self):
        super().__init__()
        self.hx = 0
        self.hy = 0
        self.medicine = 5
        self.food = 100
        self.loc = None

        self.verbs['anchor'] = self
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['give'] = self


    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "north"):
            self.hx = 0
            self.hy = -1
        elif (verb == "south"):
            self.hx = 0
            self.hy = 1
        elif (verb == "east"):
            self.hx = 1
            self.hy = 0
        elif (verb == "west"):
            self.hx = -1
            self.hy = 0
        elif (verb == "anchor"):
            self.hx = 0
            self.hy = 0
        elif (verb == "give"):
            # give medicine to crewmember
            if (len(cmd_list) > 3):
                if ((cmd_list[1] == "medicine") and (cmd_list[3] in nouns.keys())):
                    if (self.medicine > 0):
                        nouns[cmd_list[3]].receive_medicine(1)
                        self.medicine =  self.medicine - 1
                    else:
                        display.announce ("no more medicine to give")
            else:
                display.announce ("Give medicine to who?")
        else:
            display.announce ("Error: Ship object doe not understand verb " + verb)


    def print (self):
        display.announce(f"ship is at: {self.loc.get_x()}, {self.loc.get_y()}", pause=False)
        if ((self.hx==0) and (self.hy==0)):
            display.announce ("ship anchored", pause=False)
        elif ((self.hx == 1) and (self.hy == 0)):
            display.announce ("ship heading is east", pause=False)
        elif ((self.hx == -1) and (self.hy == 0)):
            display.announce ("ship heading is west", pause=False)
        elif ((self.hx == 0) and (self.hy == -1)):
            display.announce ("ship heading is north", pause=False)
        elif ((self.hx == 0) and (self.hy == 1)):
            display.announce ("ship heading is south", pause=False)

        display.announce(f"ship has {self.medicine} medicine", pause=False)

    def get_loc (self):
        return self.loc

    def set_loc (self, loc):
        self.loc = loc

    def start_day (self, world):
        # crew members eat, and possibly die of illnesses
        i = 0
        for crew in config.the_player.get_pirates():
            crew.start_day (self)

    def get_food (self):
        return self.food

    def take_food (self, amt):
        self.food = self.food - amt

    def enter (self):
        pass

    def end_day (self, world):

        if ((self.hx != 0) or (self.hy != 0)):
            # find the destination
            new_loc = world.get_loc (self.loc.get_x()+self.hx, self.loc.get_y()+self.hy)

            # change our location
            self.set_loc (new_loc)

            # tell the new location that we entered
            new_loc.enter(self)

        for crew in config.the_player.get_pirates():
            crew.end_day ()
