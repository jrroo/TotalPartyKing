#!/bin/python

import random
import time
import sys
import collections

class TPKli():
    ''' CLI interface for the Total Party King '''
    def __init__(self, prompt=None):
        ''' init '''
        self._prompt = prompt or 'Your command? '
        pass

    def print_menu(self, menu):
        ''' takes in a dict, vals are options, keys are ret 
            options: dict, key - vals are printed and returns selected element's key
            prompt: None is default, or you can pass a string to use
        '''
        longest_key = max([len(x.key) for x in menu.items])
        choice = None
        while not menu.has_key(choice):
            for item in menu.items:
                print('{:{width}} - {}'.format(item.key,
                                               item.desc,
                                               width=longest_key
                                              ))
            choice = self.get_string(menu.prompt or self._prompt)
        menu.choose(choice)

    def get_string(self, prompt):
        ''' get a string from the user '''
        choice = input(prompt)
        return str(choice)

    def get_int(self, prompt):
        ''' get an int from the user '''
        choice = 'bad'
        while not isinstance(choice, int):
            try:
                choice = int(input(prompt))
            except ValueError:
                print('Must enter an integer')
        return choice

    def roll_dice(self, d=6, n=3):
        ''' roll n of d sided dice, return list of rolls
            call sum(ret) to get the total of the rolls
        '''
        results = []
        for i in range(0, n):
            results.append(random.randint(1, d))
        return results

    class Menu():
        ''' Holds the definition of a menu for later use '''
        MenuItem = collections.namedtuple('MenuItem',
                                          'desc, key, action, args, kwargs'
                                         )
        def __init__(self, prompt=None):
            ''' init for the menu class '''
            self.items = [] 
            self._next_key = 0
            self.prompt = prompt
        def add_item(self, desc, action, key=None, *args, **kwargs):
            ''' Appends and item to the menu list
                desc: the displayed description
                action: either a method to call or a submenu
                [key]: string user must enter to select this option
                [args]: args to pass to function
                [kwargs]: kwargs to pass to function
            '''
            if not callable(action) and not isinstance(action, Menu):
                return False
            if not key is None and self.has_key(key):
                return False
            item = self.MenuItem(desc=desc,
                                 key=key or self._get_next_key(),
                                 action=action,
                                 args=args,
                                 kwargs=kwargs,
                                )
            self.items.append(item)
            return True

        def has_key(self, key):
            ''' tests if the key exists in our menu '''
            if key is None:
                return False
            return any(key == x.key for x in self.items)

        def get_item(self, key):
            if key is None:
                return None
            ret = [item for item in self.items if item.key == key]
            assert len(ret) == 1, 'Too many/no matching keys'
            return ret[0]

        def choose(self, choice):
            if self.has_key(choice):
                item = self.get_item(choice)
                #item.action(*item.args, **item.kwargs)

        def _get_next_key(self):
            ''' gets next unique key '''
            while any(self._next_key == x.get('key', None)
                      for x in self.items):
                self._next_key += 1
            return str(self._next_key)



def main():
    ''' test function '''
    cli = TPKli()
    menu = cli.Menu()
    menu.add_item('Some item', print, args='some item selected')
    menu.add_item('Exit', sys.exit, key='q')
    choice = cli.print_menu(menu)
    print('Your int is {}'.format(cli.get_int('Integer? ')))
    

if __name__ == '__main__':
    main()