from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
from django.core.validators import MaxValueValidator, MinValueValidator

author = 'Lunzheng Li'

doc = """

This is the treatment group.

"""


class Constants(BaseConstants):
    name_in_url = 'polls_treatment'
    players_per_group = None
    num_rounds = 4
    practice_rounds = 2
    real_rounds = num_rounds - practice_rounds

    instructions_template = 'polls_treatment/Instructions.html'  # everytime when adding a var in model.py, reset the database.

    pass


class Subsession(BaseSubsession):
    def creating_session(self):
        # # # since this application is only for the treatment group, we don't need to creat the boolean treatment var here
        # voters can not have same id position, I firstly create a list with random order, then assign it one by one start from index 0
        id_list = list(range(1, 16))
        random.shuffle(id_list)
        for player in self.get_players():
            player.id_position = id_list[0]
            del id_list[0]  # what's cool is that the old index 1 become 0 now.

        # for player in self.get_players():
        #     player.id_position = random.randint(1, 15)

        for group in self.get_groups():
            group.quality_J = random.randint(1, 40)
            group.quality_K = random.randint(1, 40)

    pass


class Group(BaseGroup):
    practice_round_number = models.IntegerField()  # round numbers after adding round numbers.
    quality_J = models.IntegerField()
    quality_K = models.IntegerField()

    winner = models.StringField()  # the elected party, if there is draw, we randomly pick one.

    k_inelection = models.FloatField()  # fraction of supporting K in election.
    j_inelection = models.FloatField()  # fraction of supporting J in election.
    a_inelection = models.FloatField()  # fraction of abstain in election, actually we dont need it we do not want to print it out

    # # # fractions of supporting K, J in different company polls
    companyA_k_inpolls = models.FloatField()
    companyB_k_inpolls = models.FloatField()
    companyC_k_inpolls = models.FloatField()
    companyD_k_inpolls = models.FloatField()
    companyE_k_inpolls = models.FloatField()

    companyA_j_inpolls = models.FloatField()
    companyB_j_inpolls = models.FloatField()
    companyC_j_inpolls = models.FloatField()
    companyD_j_inpolls = models.FloatField()
    companyE_j_inpolls = models.FloatField()

    Allcompany = models.StringField()  # it's actually not needed, I just want to print it out to check

    # # # treatment group, select two baised poll, in this case, let's find the poll favours K.
    biased1_k_inpolls = models.FloatField()
    biased1_j_inpolls = models.FloatField()
    biased2_k_inpolls = models.FloatField()
    biased2_j_inpolls = models.FloatField()

    def set_payoff(self):
        players = self.get_players()  # is this return to a list of numbers? No, it seems not. I tried

        # The following counts everyone's poll
        polls = [p.poll for p in players]
        k_poll = polls.count("K")
        self.k_inpolls = k_poll / len(polls)

        # # #  the winner and payoffs
        votes = [p.vote for p in players]
        k_vote = votes.count("K")
        j_vote = votes.count("J")
        a_vote = votes.count("Abstain")
        if k_vote > j_vote:
            self.winner = "K"
        elif j_vote > k_vote:
            self.winner = "J"
        elif k_vote == j_vote:
            self.winner = random.choice(["K","J"])

        if self.winner == "K":
            for p in players:
                p.payoff = c(self.quality_K + 100 - 5 * abs(10 - p.id_position))
        else:
            for p in players:
                p.payoff = c(self.quality_J + 100 - 5 * abs(6 - p.id_position))

        self.k_inelection = round(k_vote / len(players) * 100, 2)  # show percentage
        self.j_inelection = round(j_vote / len(players) * 100, 2)
        self.a_inelection = round(a_vote / len(players) * 100, 2)

        # # # the poll part
        poll_num = 4  # each company select poll_num of participants
        companyA = random.sample(range(1, len(players) + 1), poll_num)
        companyB = random.sample(range(1, len(players) + 1), poll_num)
        companyC = random.sample(range(1, len(players) + 1), poll_num)
        companyD = random.sample(range(1, len(players) + 1), poll_num)
        companyE = random.sample(range(1, len(players) + 1), poll_num)

        Allcompany = companyA + companyB + companyC + companyD + companyE

        self.Allcompany = ",".join(str(e) for e in Allcompany)  # actually not needed, to print it out

        # # # find out subjects are allocated to which company
        for i in range(1, len(players) + 1):
            if i in Allcompany:
                index_player_i = [j for j, x in enumerate(Allcompany) if x == i]
                printout = ""
                for index in index_player_i:
                    if index in range(0, poll_num):
                        printout = printout + " A"
                    elif index in range(poll_num, 2 * poll_num):
                        printout = printout + " B"
                    elif index in range(2 * poll_num, 3 * poll_num):
                        printout = printout + " C"
                    elif index in range(3 * poll_num, 4 * poll_num):
                        printout = printout + " D"
                    elif index in range(4 * poll_num, 5 * poll_num):
                        printout = printout + " E"
                    self.get_player_by_id(i).company_each_player = printout
            else:
                self.get_player_by_id(i).company_each_player = "None"

        # # #  fraction of supporting K in each company poll
        k_companyA= k_companyB= k_companyC= k_companyD= k_companyE = 0
        j_companyA= j_companyB= j_companyC= j_companyD= j_companyE = 0

        for i in companyA:
            if self.get_player_by_id(i).poll == "K":
                k_companyA += 1
            elif self.get_player_by_id(i).poll == "J":
                j_companyA += 1
        for i in companyB:
            if self.get_player_by_id(i).poll == "K":
                k_companyB += 1
            elif self.get_player_by_id(i).poll == "J":
                j_companyB += 1
        for i in companyC:
            if self.get_player_by_id(i).poll == "K":
                k_companyC += 1
            elif self.get_player_by_id(i).poll == "J":
                j_companyC += 1
        for i in companyD:
            if self.get_player_by_id(i).poll == "K":
                k_companyD += 1
            elif self.get_player_by_id(i).poll == "J":
                j_companyD += 1
        for i in companyE:
            if self.get_player_by_id(i).poll == "K":
                k_companyE += 1
            elif self.get_player_by_id(i).poll == "J":
                j_companyE += 1

        self.companyA_k_inpolls = round(k_companyA / poll_num * 100, 2)
        self.companyA_j_inpolls = round(j_companyA / poll_num * 100, 2)
        self.companyB_k_inpolls = round(k_companyB / poll_num * 100, 2)
        self.companyB_k_inpolls = round(j_companyB / poll_num * 100, 2)
        self.companyC_k_inpolls = round(k_companyC / poll_num * 100, 2)
        self.companyC_j_inpolls = round(j_companyC / poll_num * 100, 2)
        self.companyD_k_inpolls = round(k_companyD / poll_num * 100, 2)
        self.companyD_j_inpolls = round(j_companyD / poll_num * 100, 2)
        self.companyE_k_inpolls = round(k_companyE / poll_num * 100, 2)
        self.companyE_j_inpolls = round(j_companyE / poll_num * 100, 2)

        # # # sort the fraction of support in polls, and pick the baised ones
        # since now we have abstain, we have to redefine which is the most baised one
        list_K = sorted(
            [self.companyA_k_inpolls, self.companyB_k_inpolls, self.companyC_k_inpolls, self.companyD_k_inpolls,
             self.companyE_k_inpolls, ]) # OR MAKE IT DIFFERENCE BETWEEN K AND J
        self.biased1_k_inpolls = list_K[-1]
        self.biased1_j_inpolls = 100 - self.biased1_k_inpolls
        self.biased2_k_inpolls = list_K[-2]
        self.biased2_j_inpolls = 100 - self.biased2_k_inpolls

    # # # define the display of round numbers
    def set_practice_round_numbers(self):
        if self.round_number < Constants.practice_rounds + 1:
            self.practice_round_number = self.round_number
        else:
            self.practice_round_number = self.round_number - Constants.practice_rounds
        return self.practice_round_number

    pass


class Player(BasePlayer):
    id_position = models.IntegerField()
    poll = models.StringField(
        choices=['J', 'K', 'Prefer not to answer'],
        widget=widgets.RadioSelect
    )
    vote = models.StringField(
        choices=['J', 'K', 'Abstain'],
        widget=widgets.RadioSelect
    )

    company_each_player = models.StringField()

    belief = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)]
     )

    # Survey
    gender = models.StringField(blank=True,
        choices=['M', 'F','Other','Prefer not to answer'],
        widget=widgets.RadioSelect
    )
    nationality = models.StringField(blank=True)
    major = models.StringField(blank=True)
    income = models.StringField(blank=True,
        choices=['Less than £40,000', '£40,000-70,000','£70,000 -£100,000','more than £100,000'],
        widget=widgets.RadioSelect
    )


    pass
