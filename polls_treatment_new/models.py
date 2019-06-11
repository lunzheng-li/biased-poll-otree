from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
import numpy as np
from django.core.validators import MaxValueValidator, MinValueValidator

author = 'Lunzheng Li'

doc = """

This is the new treatment group.

"""


class Constants(BaseConstants):
    name_in_url = 'polls_treatment_new'
    players_per_group = 15

    num_rounds = 18 # the total number of round, including the practice round.
    practice_rounds = 3
    real_rounds = num_rounds - practice_rounds

    poll_num = 4  # each company select poll_num of participants

    instructions_template = 'polls_treatment_new/Instructions.html'  # everytime when adding a var in model.py, reset the database.

    V_K = [68, 101, 19, 94, 73, 1, 65, 109, 23, 41, 78, 71, 104, 112, 82, 113, 119, 113,]
    V_J = [104, 100, 96, 37, 94, 37, 94, 45, 43, 76, 108, 19, 44, 84, 75, 1, 15, 96, 74, 4,]

    pass


class Subsession(BaseSubsession):
    def creating_session(self):
        # voters can not have same id position, I firstly create a list with random order, then assign it one by one start from index 0
        id_list = list(range(1,16))
        random.shuffle(id_list)
        companyA_ID = random.sample(range(1, Constants.players_per_group + 1), Constants.poll_num)
        companyB_ID = random.sample(range(1, Constants.players_per_group + 1), Constants.poll_num)
        companyC_ID = random.sample(range(1, Constants.players_per_group + 1), Constants.poll_num)
        companyD_ID = random.sample(range(1, Constants.players_per_group + 1), Constants.poll_num)
        companyE_ID = random.sample(range(1, Constants.players_per_group + 1), Constants.poll_num)
        Allcompany = companyA_ID + companyB_ID + companyC_ID + companyD_ID + companyE_ID
        for player in self.get_players():
            player.id_position = id_list[0]
            del id_list[0] # what's cool is that the old index 1 become 0 now.
            player.poll_display_order = random.randint(0, 1)

        for group in self.get_groups(): # it works if we have multiple groups.
            group.quality_J = Constants.V_J[self.round_number - 1]
            group.quality_K = Constants.V_K[self.round_number - 1]
            group.Allcompany = ",".join(str(e) for e in Allcompany)

    pass


class Group(BaseGroup):
    practice_round_number = models.IntegerField() # round numbers after adding round numbers.
    quality_J = models.IntegerField()
    quality_K = models.IntegerField()

    winner = models.StringField()# the elected party, if there is draw, we randomly pick one.

    k_inelection = models.FloatField()# fraction of supporting K in election.
    j_inelection = models.FloatField()# fraction of supporting J in election.

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

    # # # The string(lst) of poll results in each company
    companyA = models.StringField()
    companyB = models.StringField()
    companyC = models.StringField()
    companyD = models.StringField()
    companyE = models.StringField()

    Allcompany = models.StringField()# it's actually not needed, I just want to print it out to check

    # # # treatment group, select two baised poll, in this case, let's find the poll favours K.
    biased1_company = models.StringField() # the company name of the most biased (toward K) company
    biased2_company = models.StringField()
    biased1_k_inpolls = models.FloatField()
    biased1_j_inpolls = models.FloatField()
    biased2_k_inpolls = models.FloatField()
    biased2_j_inpolls = models.FloatField()


    def set_pollwaitpage(self):
        Allcompany_lst = [int(e) for e in self.Allcompany.split(",")]

        # # # find out subjects are allocated to which company
        for i in range(1, Constants.players_per_group + 1):
            if i in Allcompany_lst:
                index_player_i = [j for j, x in enumerate(Allcompany_lst) if x == i]
                printout = ""
                for index in index_player_i:
                    if index in range(0, Constants.poll_num):
                        printout = printout + " Company A,"
                    elif index in range(Constants.poll_num, 2 * Constants.poll_num):
                        printout = printout + " Company B,"
                    elif index in range(2 * Constants.poll_num, 3 * Constants.poll_num):
                        printout = printout + " Company C,"
                    elif index in range(3 * Constants.poll_num, 4 * Constants.poll_num):
                        printout = printout + " Company D,"
                    elif index in range(4 * Constants.poll_num, 5 * Constants.poll_num):
                        printout = printout + " Company E,"
                self.get_player_by_id(i).company_each_player = printout
            else:
                self.get_player_by_id(i).company_each_player = "None"
                # # # the function excecute before poll result page: to calcaulate every company's results.

    def set_pollresultwaitpage(self):
        Allcompany_lst = [int(e) for e in self.Allcompany.split(",")]
        companyA = [self.get_player_by_id(i).poll for i in Allcompany_lst[0:Constants.poll_num]]
        companyB = [self.get_player_by_id(i).poll for i in Allcompany_lst[Constants.poll_num:(2 * Constants.poll_num)]]
        companyC = [self.get_player_by_id(i).poll for i in
                    Allcompany_lst[(2 * Constants.poll_num):(3 * Constants.poll_num)]]
        companyD = [self.get_player_by_id(i).poll for i in
                    Allcompany_lst[(3 * Constants.poll_num):(4 * Constants.poll_num)]]
        companyE = [self.get_player_by_id(i).poll for i in
                    Allcompany_lst[(4 * Constants.poll_num):(5 * Constants.poll_num)]]

        k_companyA = companyA.count("K")
        k_companyB = companyB.count("K")
        k_companyC = companyC.count("K")
        k_companyD = companyD.count("K")
        k_companyE = companyE.count("K")
        j_companyA = companyA.count("J")
        j_companyB = companyB.count("J")
        j_companyC = companyC.count("J")
        j_companyD = companyD.count("J")
        j_companyE = companyE.count("J")

        # # # if everyone abstain, we have a zero division error.
        try:
            self.companyA_k_inpolls = round(k_companyA / (k_companyA + j_companyA) * 100, 2)
            self.companyA_j_inpolls = round(j_companyA / (k_companyA + j_companyA) * 100, 2)
        except ZeroDivisionError:
            self.companyA_k_inpolls = self.companyA_j_inpolls = 0
        try:
            self.companyB_k_inpolls = round(k_companyB / (k_companyB + j_companyB) * 100, 2)
            self.companyB_j_inpolls = round(j_companyB / (k_companyB + j_companyB) * 100, 2)
        except ZeroDivisionError:
            self.companyB_k_inpolls = self.companyB_j_inpolls = 0
        try:
            self.companyC_k_inpolls = round(k_companyC / (k_companyC + j_companyC) * 100, 2)
            self.companyC_j_inpolls = round(j_companyC / (k_companyC + j_companyC) * 100, 2)
        except ZeroDivisionError:
            self.companyC_k_inpolls = self.companyC_j_inpolls = 0
        try:
            self.companyD_k_inpolls = round(k_companyD / (k_companyD + j_companyD) * 100, 2)
            self.companyD_j_inpolls = round(j_companyD / (k_companyD + j_companyD) * 100, 2)
        except ZeroDivisionError:
            self.companyD_k_inpolls = self.companyD_j_inpolls = 0
        try:
            self.companyE_k_inpolls = round(k_companyE / (k_companyE + j_companyE) * 100, 2)
            self.companyE_j_inpolls = round(j_companyE / (k_companyE + j_companyE) * 100, 2)
        except ZeroDivisionError:
            self.companyE_k_inpolls = self.companyE_j_inpolls = 0

        self.companyA = ",".join(str(e) for e in companyA)  # actually not needed, to print it out
        self.companyB = ",".join(str(e) for e in companyB)  # actually not needed, to print it out
        self.companyC = ",".join(str(e) for e in companyC)  # actually not needed, to print it out
        self.companyD = ",".join(str(e) for e in companyD)  # actually not needed, to print it out
        self.companyE = ",".join(str(e) for e in companyE)  # actually not needed, to print it out

        list_K= [self.companyA_k_inpolls, self.companyB_k_inpolls, self.companyC_k_inpolls, self.companyD_k_inpolls, self.companyE_k_inpolls,]
        list_K_sorted = sorted(list_K)
        list_K_index = np.argsort(list_K)
        self.biased1_k_inpolls = list_K_sorted[-1]
        self.biased1_j_inpolls = 100 - self.biased1_k_inpolls
        self.biased2_k_inpolls = list_K_sorted[-2]
        self.biased2_j_inpolls = 100 - self.biased2_k_inpolls

        if list_K_index[-1] == 0:
            self.biased1_company = "A"
        elif list_K_index[-1] == 1:
            self.biased1_company = "B"
        elif list_K_index[-1] == 2:
            self.biased1_company = "C"
        elif list_K_index[-1] == 3:
            self.biased1_company = "D"
        elif list_K_index[-1] == 4:
            self.biased1_company = "E"

        if list_K_index[-2] == 0:
            self.biased2_company = "A"
        elif list_K_index[-2] == 1:
            self.biased2_company = "B"
        elif list_K_index[-2] == 2:
            self.biased2_company = "C"
        elif list_K_index[-2] == 3:
            self.biased2_company = "D"
        elif list_K_index[-2] == 4:
            self.biased2_company = "E"

    def set_voteresultwaitpage(self):
        players = self.get_players()  # is this return to a list of numbers? No, it seems not. I tried
        votes = [p.vote for p in players]
        k_vote = votes.count("K")
        j_vote = votes.count("J")
        # a_vote = votes.count("Abstain")
        if k_vote > j_vote:
            self.winner = "K"
        elif j_vote > k_vote:
            self.winner = "J"
        elif k_vote == j_vote:
            self.winner = random.choice(["K", "J"])

        if self.winner == "K":
            for p in players:
                p.payoff = c(self.quality_K + 100 - 5 * abs(10 - p.id_position))
        else:
            for p in players:
                p.payoff = c(self.quality_J + 100 - 5 * abs(6 - p.id_position))

        if k_vote + j_vote != 0:
            self.k_inelection = round(k_vote / (k_vote + j_vote) * 100, 2)  # show percentage
            self.j_inelection = round(j_vote / (k_vote + j_vote) * 100, 2)
        else:
            self.k_inelection = self.j_inelection = 0

        # # # to cope with the payoff issue.
        if self.round_number == Constants.num_rounds:
            for player in players:
                player.total_payoffs = round(float(sum([p.payoff for p in player.in_rounds(Constants.practice_rounds + 1, Constants.num_rounds)]))/200 + 5, 2)


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
        choices=['K', 'J', 'Prefer not to participate in the Poll'],
        widget=widgets.RadioSelect,
    )
    vote = models.StringField(
        choices=['K', 'J', 'Abstain'],
        widget=widgets.RadioSelect,
    )

    company_each_player = models.StringField()  # for instance, player 1 is selected by company A B C, player 2 is selected by company A D....

    belief_k = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )

    belief_j = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )

    # Survey
    gender = models.StringField(blank=True,
                                choices=['M', 'F', 'Other', 'Prefer not to answer'],
                                widget=widgets.RadioSelect
                                )
    nationality = models.StringField(blank=True)
    major = models.StringField(blank=True)
    income = models.StringField(blank=True,
                                choices=['Less than £40,000', '£40,000-70,000', '£70,000 -£100,000',
                                         'more than £100,000'],
                                widget=widgets.RadioSelect
                                )

    # # # try to resolve the total payoff issue
    total_payoffs = models.FloatField() # note that it's a little bit different from the var in page.py

    # # # in the poll result page, random order of K, J display across subjects
    poll_display_order = models.IntegerField()  # if this var = 0, K before J; if this var = 1, J before K.

    pass