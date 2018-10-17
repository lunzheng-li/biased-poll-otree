from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random
from django.core.validators import MaxValueValidator, MinValueValidator

author = 'Lunzheng Li'

doc = """

This is the control_new, we randomly choose 2 from the 5

08/10 22:45 pm
We should modify the treatment app

10/10 0:03 am

    Company E: 0.0% for Candidate J; 100.0% for Candidate K.
    Company C: 0.0% for Candidate J; 100.0% for Candidate K.
    
    E might appear before C, guess it's not a problem-


"""

class Constants(BaseConstants):
    name_in_url = 'poll_control_new'
    players_per_group = 5

    num_rounds = 2 # the total number of round, including the practice round.
    practice_rounds = 1
    no_paying_rounds = list(range(1, practice_rounds+1))
    real_rounds = num_rounds - practice_rounds

    poll_num = 4  # each company select poll_num of participants

    instructions_template = 'poll_control_new/Instructions.html' # everytime when adding a var in model.py, reset the database.

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
            player.poll_display_order = random.randint(0,1)

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

    # # # Select two random companies to reveal the poll.
    random1_company = models.StringField()
    random2_company = models.StringField()
    random1_k_inpolls = models.FloatField()
    random1_j_inpolls = models.FloatField()
    random2_k_inpolls = models.FloatField()
    random2_j_inpolls = models.FloatField()


    # # # The function should excecute before the poll page: companies randomly select 4 participants.
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
        companyC = [self.get_player_by_id(i).poll for i in Allcompany_lst[(2 * Constants.poll_num):(3 * Constants.poll_num)]]
        companyD = [self.get_player_by_id(i).poll for i in Allcompany_lst[(3 * Constants.poll_num):(4 * Constants.poll_num)]]
        companyE = [self.get_player_by_id(i).poll for i in Allcompany_lst[(4 * Constants.poll_num):(5 * Constants.poll_num)]]

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
            self.companyA_k_inpolls = round(k_companyA/(k_companyA + j_companyA)*100, 2)
            self.companyA_j_inpolls = round(j_companyA/(k_companyA + j_companyA)*100, 2)
        except ZeroDivisionError:
            self.companyA_k_inpolls = self.companyA_j_inpolls = 0
        try:
            self.companyB_k_inpolls = round(k_companyB/(k_companyB + j_companyB)*100, 2)
            self.companyB_j_inpolls = round(j_companyB/(k_companyB + j_companyB)*100, 2)
        except ZeroDivisionError:
            self.companyB_k_inpolls = self.companyB_j_inpolls = 0
        try:
            self.companyC_k_inpolls = round(k_companyC/(k_companyC + j_companyC)*100, 2)
            self.companyC_j_inpolls = round(j_companyC/(k_companyC + j_companyC)*100, 2)
        except ZeroDivisionError:
            self.companyC_k_inpolls = self.companyC_j_inpolls = 0
        try:
            self.companyD_k_inpolls = round(k_companyD/(k_companyD + j_companyD)*100, 2)
            self.companyD_j_inpolls = round(j_companyD/(k_companyD + j_companyD)*100, 2)
        except ZeroDivisionError:
            self.companyD_k_inpolls = self.companyD_j_inpolls = 0
        try:
            self.companyE_k_inpolls = round(k_companyE/(k_companyE + j_companyE)*100, 2)
            self.companyE_j_inpolls = round(j_companyE/(k_companyE + j_companyE)*100, 2)
        except ZeroDivisionError:
            self.companyE_k_inpolls = self.companyE_j_inpolls = 0


        self.companyA = ",".join(str(e) for e in companyA)  # actually not needed, to print it out
        self.companyB = ",".join(str(e) for e in companyB)  # actually not needed, to print it out
        self.companyC = ",".join(str(e) for e in companyC)  # actually not needed, to print it out
        self.companyD = ",".join(str(e) for e in companyD)  # actually not needed, to print it out
        self.companyE = ",".join(str(e) for e in companyE)  # actually not needed, to print it out


        # no bias here, let's pick random two polls from the five companies'
        random_companies = sorted(random.sample(['A', 'B', 'C', 'D', 'E'], 2))
        self.random1_company = random_companies[0]
        self.random2_company = random_companies[1]

        # ok, now I have got the names of the selected companies. use the names to retrive the percentages.
        if random_companies[0] == 'A':
            self.random1_j_inpolls = self.companyA_j_inpolls
            self.random1_k_inpolls = self.companyA_k_inpolls
        elif random_companies[0] == 'B':
            self.random1_j_inpolls = self.companyB_j_inpolls
            self.random1_k_inpolls = self.companyB_k_inpolls
        elif random_companies[0] == 'C':
            self.random1_j_inpolls = self.companyC_j_inpolls
            self.random1_k_inpolls = self.companyC_k_inpolls
        elif random_companies[0] == 'D':
            self.random1_j_inpolls = self.companyD_j_inpolls
            self.random1_k_inpolls = self.companyD_k_inpolls
        elif random_companies[0] == 'E':
            self.random1_j_inpolls = self.companyE_j_inpolls
            self.random1_k_inpolls = self.companyE_k_inpolls

        if random_companies[1] == 'A':
            self.random2_j_inpolls = self.companyA_j_inpolls
            self.random2_k_inpolls = self.companyA_k_inpolls
        elif random_companies[1] == 'B':
            self.random2_j_inpolls = self.companyB_j_inpolls
            self.random2_k_inpolls = self.companyB_k_inpolls
        elif random_companies[1] == 'C':
            self.random2_j_inpolls = self.companyC_j_inpolls
            self.random2_k_inpolls = self.companyC_k_inpolls
        elif random_companies[1] == 'D':
            self.random2_j_inpolls = self.companyD_j_inpolls
            self.random2_k_inpolls = self.companyD_k_inpolls
        elif random_companies[1] == 'E':
            self.random2_j_inpolls = self.companyE_j_inpolls
            self.random2_k_inpolls = self.companyE_k_inpolls

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

        if k_vote+j_vote != 0:
            self.k_inelection = round(k_vote / (k_vote+j_vote) * 100, 2)  # show percentage
            self.j_inelection = round(j_vote / (k_vote+j_vote) * 100, 2)
        else:
            self.k_inelection = self.j_inelection = 0

        # # # to cope with the payoff issue.
        if self.round_number == Constants.num_rounds:
            for player in players:
                player.total_payoffs = float(sum([p.payoff for p in player.in_rounds(Constants.practice_rounds + 1,Constants.num_rounds)]))/200 + 5

        # if self.subsession.round_number in Constants.no_paying_rounds:
        #     p.payoff = 0



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
        choices=['K', 'J','Prefer not to participate in the Poll'],
        widget=widgets.RadioSelect,
    )
    vote = models.StringField(
        choices=['K', 'J', 'Abstain'],
        widget=widgets.RadioSelect,
    )

    company_each_player = models.StringField()# for instance, player 1 is selected by company A B C, player 2 is selected by company A D....

    belief_k = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)]
     )

    belief_j = models.IntegerField(
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

    # # # try to resolve the total payoff issue
    total_payoffs = models.FloatField()# note that it's a little bit different from the var in page.py

    # 17/10/2018 20:13, TypeError: FloatField should be set to float, not RealWorldCurrency.
    # how about we simply change the total_payoffs to a currency field
    # not sure how this Currency Field behavior, let's go back to FloatField
    # ok we should change it back again, since payoff is currencyfield
    # https: // groups.google.com / forum /  # !msg/otree/1MRfRGtwJR4/6x3LLLA4GAAJ

    # # # in the poll result page, random order of K, J display across subjects
    poll_display_order = models.IntegerField() # if this var = 0, K before J; if this var = 1, J before K.

    pass
