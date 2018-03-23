from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Information(Page):
    form_model = 'player'
    pass

class Poll(Page):
    form_model = 'player'
    form_fields = ['poll']
    pass

class PollWaitpage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_portion()
    pass

class PollResult(Page):
    pass

class Vote(Page):
    form_model = 'player'
    form_fields = ['vote']
    pass

class VoteWaitpage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_portion()
    pass

class FinalResult(Page):
    pass


page_sequence = [
    Information,
    Poll,
    PollWaitpage,
    PollResult,
    Vote,
    PollWaitpage,
    FinalResult
]
