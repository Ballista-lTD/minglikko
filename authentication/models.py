from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class Tokens(models.Model):
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

    def total(self):
        return sum(
            [self.religiousity, self.liberal,
             self.will_help_poor, self.wealth,
             self.beauty, self.charisma,
             self.strength, self.intelligence])

    def __str__(self):
        return f"{self.user} "
