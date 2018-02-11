from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    form_model = 'player'
    form_fields = ['name','age']
    pass



class Results(Page):
    pass


page_sequence = [
    MyPage,
    Results
]
