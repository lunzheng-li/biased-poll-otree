from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    form_model = 'player'
    pass



class Results(Page):
    form_model = 'player'
    form_fields = ['poll']
    pass


page_sequence = [
    MyPage,
    Results
]
