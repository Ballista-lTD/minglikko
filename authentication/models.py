from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class Access_token(models.Model):
#


class Tokens(models.Model):
    user = models.OneToOneField(User, related_name='tokens', on_delete=models.CASCADE)
    intelligence = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    strength = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    individual_freedom = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    charisma = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    wealth = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    will_help_poor = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    religiousity = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])
    liberal = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])

    def total(self):
        return sum(
            [self.religiousity, self.liberal, self.will_help_poor, self.wealth,
             self.individual_freedom, self.charisma,
             self.strength, self.individual_freedom])

    def __str__(self):
        return f"{self.user} "
