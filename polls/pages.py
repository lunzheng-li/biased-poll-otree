from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Ideology(Page):
    form_model = 'player'
    pass

class Informed(Page):
    pass

class Poll(Page):
    form_model = 'player'
    form_fields = ['poll']
    pass

class PollWaitpage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoff()
    pass

class PollResult(Page):
    pass

class Vote(Page):
    form_model = 'player'
    form_fields = ['vote']
    pass

class VoteWaitpage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoff()
    pass

class FinalResult(Page):
    pass


page_sequence = [
    Ideology,
    Informed,
    Poll,
    PollWaitpage,
    PollResult,
    Vote,
    PollWaitpage,
    FinalResult
]
