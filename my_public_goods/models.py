from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Lunzheng Li'

doc = """
It is simple public goods game. 
"""


class Constants(BaseConstants):
    name_in_url = 'my_public_goods'
    players_per_group = 3
    num_rounds = 1
    endowment = c(100)
    multiplier = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # I DON'T CARE ABOUT THE total_contribution, and individual_share, so I don't define the Field
    # here, let's see what is gonna happen.
    # it worked and we get rid off all the redunant var in the result file
    def set_payoffs(self):
        players = self.get_players()
        contributions = [p.contribution for p in players]
        self.total_contribution = sum(contributions)
        self.individual_share = self.total_contribution * Constants.multiplier / Constants.players_per_group
        for p in self.get_players():
            p.payoff = Constants.endowment - p.contribution + self.individual_share
    pass


class Player(BasePlayer):
    contribution = models.CurrencyField(min = 0, max = Constants.endowment)
    pass
