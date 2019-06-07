from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_trust'
    players_per_group = 2
    num_rounds = 1

    endowment = c(10)
    multiplication_factor = 3


class Subsession(BaseSubsession):


    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField()
    sent_back_amount = models.CurrencyField()# forget to define the range of those vars
    #  defining those fields at the Group level.
    #  This makes each group has exactly 1 sent_amount and exactly 1 sent_back_amount
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * Constants.multiplication_factor - self.sent_back_amount
        # the sent_amount can be 0, and when it is, it makes the sent_back_amount 0
        pass


class Player(BasePlayer):
    pass
