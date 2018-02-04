#!/bin/python3

import bs4
from bs4 import BeautifulSoup as bs

def istag(item):
    return isinstance(item, bs4.element.Tag)

class GurpsCharacter(object):
    ''' Class to handle loading/saving character to/from gcs xmls '''

    def __init__(self, fname):
        self._fname = fname

        with open(self._fname, 'r') as f:
            # read in file, convert to string and replace name with name_ since
            # bs does not support having a tag called <name>
            self.data = f.read().replace('name', 'name_')
        self.soup = bs(self.data, 'lxml')

        self.__load()

        for k, v in self.__dict__.items():
            print('{:12} : {}'.format(k, v))

    def __load(self):
        ''' tedius loading of elements '''
        stats = [
                 'dx',
                 'fp',
                 'hp',
                 'ht',
                 'iq',
                 'move',
                 'perception',
                 'speed',
                 'st',
                 'will',
                 ]
        self._id = self.soup.character.get('id')
        self._created = self.soup.character.created_date
        self._modified = self.soup.character.modified_date

        # contains general info about the character such as name, age, weight
        self._profile = {attr.name: attr.text
                         for attr in self.soup.character.profile
                         if istag(attr)
                         }

        self._stats = {attr.name: attr.text
                       for attr in self.soup.character
                       if istag(attr)
                       if attr.name in stats
                       }
        self._advantages = {advantage.name_.text: {attr.name: attr.text.strip()
                                                   for attr in advantage
                                                   if istag(attr)
                                                   if attr.name != 'name_'
                                                   }
                            for advantage in self.soup.find_all('advantage')
                            }

        self._skills = {skill.name_.text: {attr.name: attr.text.strip()
                                           for attr in skill
                                           if istag(attr)
                                           if attr.name != 'name_'
                                           }
                        for skill in self.soup.find_all('skill')
                        }

    def __contains__(self, attr):
        return self.__dict__.has_key(attr)




def main():
    gc = GurpsCharacter('royce.gcs')


if __name__ == '__main__':
    main()
