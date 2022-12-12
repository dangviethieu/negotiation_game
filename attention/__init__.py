from otree.api import *


doc = """
This is an attention check
"""


class C(BaseConstants):
    NAME_IN_URL = 'attention'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    consent_1 = models.BooleanField(
        widget=widgets.CheckboxInput,
        choices=[
            [True, '1.	I confirm that I have read and understand the information sheet for the above study. I have had the opportunity to consider the information, ask questions and have had these answered satisfactorily']
        ]
    )

# PAGES
class ConsentPage(Page):
    form_model = 'player'
    form_fields = ['consent_1']


page_sequence = [
    ConsentPage,
]
