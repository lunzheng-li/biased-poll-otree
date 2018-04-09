from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

# # # In the poll part, a subject is probably answering to more one companies. I tried to think it as a "list of companies",
# # # therefore, tried to import a list field. Howeer, it not working.
# # # We have some other solutions:
# # # 1. set up a string field and convert the list to string, then put the string to the field
# # # 2. Or simply use a boolean condition. 
# # # if list = [company 1, company 2]
    # # # StringField = "company1 and company2"
#from django.db.models import CharField, Model
#from django_mysql.models import ListCharField 
# # # No module named 'django_mysql', The MySQL-python module does not support Python 3.x:
# # # http://django-mysql.readthedocs.io/en/latest/model_fields/list_fields.html

import random

author = 'Lunzheng Li'

doc = """

General information:
J is in ideological position 6 and candidate of Party K is in ideological position 10
id_value_J = 100 - 5 * abs(6 - id_position)
id_value_K = 100 - 5 * abs(10 - id_position)

simple version 
Let start with a very simple version. Everyone is informed, there is only one company, and everyone see the whole poll result.
It has 5 pages: 
page 1: present ideological position and candidate quality
page 2: polling (input)
page 3: present the poll result
page 4: voting (input)
page 5: results and payoffs

The above simple version is accomplished, let's focus on the poll part. We have 3 subjects now, let's say we have two companies, 
and each of randomly select two subjects.
Some questions: Do subjects know which company they are answering to? Do they know which company's poll is revealed to them?
Do they know how many companies are there?
the answers: yes, no, yes

second version (26/03) one group, one session 
page1. Your ideological position, everyone has different id_position
page2. Subjects are either informed or not informed according to id_position
page3. There is wait page.Companies randomly select participants. 
page4. The poll
page5. wait page
page6. Poll result
page7. election
page8. winner and payoffs.

further steps:
1. multiple groups, and multiple sessions (15 players per group, 30 rounds)
2. 5 companies, 4 random selections
3. Screen display, instruction
4. page3 is redundant 
5. page6 biased poll

"""


class Constants(BaseConstants):
    name_in_url = 'polls'
    players_per_group = None
    num_rounds = 2

    # # # # There are always 2 poll companies. It seems that we should define this in Group. But I think it will work here.
    # # # Companies = ['company 1', 'company 2' ] # I haven't used this lst yet, but I think when we have more companies, it might be helpful to loop the lst.

    instructions_template = 'polls/Instructions.html' # everytime when adding a var in model.py, reset the database.

    pass


class Subsession(BaseSubsession):
    def creating_session(self):
        # # # randomize to treatments
        for player in self.get_players():
            player.id_position = random.randint(1, 15)
            # # # player.company = random.randint(1,2) # players are allocated to a company at the beginning of the session.
        if self.round_number == 1:
                for p in self.get_players():
                    p.participant.vars['treatment'] = random.randint(0,1)
        for group in self.get_groups():
            group.quality_J = random.randint(1, 40)
            group.quality_K = random.randint(1, 40)
    pass


class Group(BaseGroup):
    quality_J = models.IntegerField() # every var need to displayed need a model field
    quality_K = models.IntegerField()

    k_inpolls = models.FloatField()# fraction of supporting K in whole poll
    winner = models.StringField()# the elected party
    k_inelection = models.FloatField()# fraction of supporting K in election.
    j_inelection = models.FloatField()# fraction of supporting J in election.


    # # # link subject's  preference back to companies.
    company1_k_inpolls = models.FloatField()
    company2_k_inpolls = models.FloatField()
    company1_j_inpolls = models.FloatField()
    company2_j_inpolls = models.FloatField()

    Allcompany = models.StringField()# it's actually not needed, I just want to print it out to check



    # # # Let's ignore this block of code.
    # company1 = ListCharField(
    #     base_field=CharField(max_length=10),
    #     size=2,
    #     max_length=(2*11)
    # ) # not working, we can't import this list Field. let's just try a string field
    # company1 = models.StringField()
    # list1 = [1, 2]
    # company1 = ','.join(map(str, list1)) # The general idea would be convert the list to string first then put store in s StringField
    # However, this is not working.
    # ERRORS:
    # polls: (otree.E111) NonModelFieldAttr: Group has attribute "company1", which is not a model field, and will therefore not be saved to the database.
    #         HINT: Consider changing to "company1 = models.CharField(initial='1,2')"
    # polls: (otree.E112) MutableModelClassAttr: Group.list1 is a list. Modifying it during a session (e.g. appending or setting values) will have unpredictable results; you should use session.vars or participant.vars instead. Or, if this list is read-only, then it's recommended to move it outside of this class (e.g. put it in Constants).



    def set_payoff(self):
        players = self.get_players() # is this return to a list of numbers? No, it seems not. I tried

        # The following counts everyone's poll
        polls = [p.poll for p in players]
        k_poll = polls.count("K")
        self.k_inpolls = k_poll / len(polls) # I am try put this in PollResult.html, however, nothing.
                                            # now solved, we need define a var outside the scopes of set_portion function
                                            # Then in the html file, use group.k_inpolls, rather than group
                                            
    # def set_payoff_2(self): # if put those things in different functions, it won't work. In most cases, we just define one function under this class

        # # #  the winner and payoffs
        votes = [p.vote for p in players]
        k_vote = votes.count("K")
        j_vote = votes.count("J")
        if k_vote > j_vote:
            self.winner = "K"
            for p in players:
                p.payoff = self.quality_K + 100 - 5 * abs(10 - p.id_position)
        else:
            self.winner = "J"
            for p in players:
                p.payoff = self.quality_J + 100 - 5 * abs(6 - p.id_position)
        self.k_inelection = round(k_vote/len(players)*100, 2) # show percentage
        self.j_inelection = round(j_vote/len(players)*100, 2)

        # # # the poll part
        company1 = random.sample(range(1, len(players)+1), 2)
        company2 = random.sample(range(1, len(players)+1), 2)
        Allcompany = company1 + company2
        
        self.Allcompany = ",".join(str(e) for e in Allcompany) # actually not needed, to print it out
        
        # # # The following codes of select subjects is dumb and is very likely to be wrong
        # for i in range(1, len(players)+1):
        #     if i in company1 and i in company2:
        #         self.get_player_by_id(i).company_each_player = "Company 1 and Company 2"
        #     elif i in company1 and i not in company2:
        #         self.get_player_by_id(i).company_each_player = "Company 1"
        #     elif i not in company1 and i in company2:
        #         self.get_player_by_id(i).company_each_player = "Company 2"
        #     else:
        #         self.get_player_by_id(i).company_each_player = "Please wait"

        
        # # # Let's try another way, it seems that this is working
        for i in range(1, len(players)+1):
            if i in Allcompany:
                index_player_i = [j for j, x in enumerate(Allcompany) if x == i]
                printout = ""
                for index in index_player_i:
                    if index in range(0,2):
                        printout = printout + " 1"
                    elif index in range(2,4):
                        printout = printout + " 2"
                    self.get_player_by_id(i).company_each_player = printout
            else:
                self.get_player_by_id(i).company_each_player = "None"


        # # #  fraction of supporting K in each company poll
        k_company1 = 0
        k_company2 = 0
        for i in company1:
            if self.get_player_by_id(i).poll == "K":
                k_company1 += 1
            else:
                pass

        for i in company2:
            if self.get_player_by_id(i).poll == "K":
                k_company2 += 1
            else:
                pass
        self.company1_k_inpolls = round(k_company1/2*100, 2) # each company sample 2
        self.company1_j_inpolls = 100-self.company1_k_inpolls
        self.company2_k_inpolls = round(k_company2/2 *100, 2)# need more tests on the numbers. If wrong, " Let's try another way, it seems that this is working" part might have problem.
        self.company2_j_inpolls = 100 - self.company2_k_inpolls
    pass


class Player(BasePlayer):
    # # # id_position = models.StringField(initial = random.randint(1, 15)) # I need different participant have different id_position, however, this is not working.
    # # # OK, using creating_session in Subsession solved this problem.
    # treatment = models.IntegerField() # this subject is in treatment group (two poll are reaveled ) or in control group
    id_position = models.IntegerField()
    poll = models.StringField(
        choices=['J', 'K'],
        widget=widgets.RadioSelect
    )
    vote = models.StringField(
        choices=['J', 'K'],
        widget=widgets.RadioSelect
    )

    # # # company = models.IntegerField()
    # # # each participant is randomly allocate to a company, companies are label using numbers. Seems that it won't work since some subjects might be assigned to
    # # # more than one company

    # # # the poll part.
    # every player has model of company_each_player  which contains the companies he is answering to
    # # # companies is string field, the general idea would we get a list first then convert it to strings
    company_each_player = models.StringField()
    pass
