from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Lunzheng Li'

doc = """
Let start with a very simple version. Everyone is informed, there is only one company, and everyone see the whole poll result.
It has 5 pages: 
page 1: present ideological position and candidate quality
page 2: polling (input)
page 3: present the poll result
page 4: voting (input)
page 5: results and payoffs
"""


class Constants(BaseConstants):
    name_in_url = 'polls'
    players_per_group = None
    num_rounds = 1
    quality_J = random.randint(1,40)
    quality_K = random.randint(1, 40)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    id_position = models.StringField(initial = random.randint(1, 15)) # I need different participant have different id_position, however, this is not working.
    poll = models.StringField(
        choices=['J', 'K'],
        widget=widgets.RadioSelect
    )
    vote = models.StringField(
        choices=['J', 'K'],
        widget=widgets.RadioSelect
    )
    pass
