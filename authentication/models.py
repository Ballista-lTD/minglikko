from random import choice

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

set_1 = ["shikkari", 'anonymous', 'Minnal ⚡', 'thee', 'kokkrachi', "pavam", 'Kayamkulam', 'veeran',
         'killadi', 'porali', 'gunda', "dashamoolam", "girirajan"]
set_2 = ["Crow", "Peacock", "Dove", "Pigeon", "Turkey", "kakka", "kakkachi", "kuyil", "giraffe", "babu", "sabu", "ramu",
         "dhamu", "shambu", "Parrot", "Seagull", "Ostrich", "Penguin", "Owl",
         "Crab", "Fish", "Octopus", "Shark", "Penguin", "Woodpecker",
         "Camel", "Owl", "Tiger", "Bear", "Chimpanzee", "Lion",
         "Crocodile", "Dolphin", "Elephant", "Snake", "Kangaroo", "Hippopotamus",
         "Fox", "Gorilla", "Bat", "Frog", "Deer", "Rat", "Lizard", 'shibu', "poth", "eruma",
         "pashu", "kili", "vekili", "kuruvi", "thavala", 'poocha', "moonga", "moori", "suni", "mayil", "kozhi", "eli",
         "ottakappakshi", "puli", 'kaduva']


def id_generator():
    return f"{choice(set_1)} {choice(set_2)}"


def create_new_id():
    not_unique = True
    unique_id = id_generator()
    while not_unique:
        unique_id = id_generator()
        if not Tokens.objects.filter(name=unique_id):
            not_unique = False
    return str(unique_id)


class Tokens(models.Model):
    name = models.CharField(default='create_new_id', max_length=45)
    user = models.OneToOneField(User, related_name='tokens', on_delete=models.CASCADE)
    intelligence = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)],
                                               help_text='0-> Brain potteto. 5 -> Omniscient')
    strength = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)],
                                           help_text='0:pappadavanam , 5:Hercules'
                                           )
    beauty = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)],
                                         help_text='0-> mirrors scare me . 5-> Maya Mohini ')
    charisma = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)],
                                           help_text='0->bed is my valentine   5->I sell sand in sahara')
    wealth = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)],
                                         help_text='0 -> starving to death, 5-> I pave golden roads')
    will_help_poor = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    religiousity = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    liberal = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    priority_list = ArrayField(models.CharField(max_length=45), default=list)

    @property
    def total(self):
        return sum(
            [self.religiousity, self.liberal,
             self.will_help_poor, self.wealth,
             self.beauty, self.charisma,
             self.strength, self.intelligence])

    def __str__(self):
        return f"{self.user}"
