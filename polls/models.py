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
    pass


class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize to treatments
        for player in self.get_players():
            player.id_position = random.randint(1, 15)
    pass


class Group(BaseGroup):
    k_inpolls = models.FloatField()
    winner = models.StringField()
    def set_portion(self):
        players = self.get_players()
        polls = [p.poll for p in players]
        num_k = 0
        for i in polls:
            if i == 'K':
                num_k += 1
        self.k_inpolls = num_k / len(polls) # I am try put this in PollResult.html, however, nothing.
                                            # now solved, we need define a var outside the scopes of set_portion function
                                            # Then in the html file, use group.k_inpolls, rather than group
    # def set_payoff(self): # if put those things in different functions, it won't work. In most cases, we just define one function under this class
        players = self.get_players()
        votes = [p.vote for p in players]
        k_vote = votes.count("K")
        j_vote = votes.count("J")
        if k_vote > j_vote:
            self.winner = "K"
        else:
            self.winner = "J"

    pass


class Player(BasePlayer):
    #id_position = models.StringField(initial = random.randint(1, 15)) # I need different participant have different id_position, however, this is not working.
    # OK, using creating_session in Subsession solved this problem.
    id_position = models.IntegerField()
    poll = models.StringField(
        choices=['J', 'K'],
        widget=widgets.RadioSelect
    )
    vote = models.StringField(
        choices=['J', 'K'],
        widget=widgets.RadioSelect
    )
    pass
