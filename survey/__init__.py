from otree.api import *


doc = """
This is an attention check survey. It is used to check if the participant is paying attention to the game.
"""


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    StandardChoices = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    ]
    

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # survey 1
    item1A = models.IntegerField(
        label='How well did you negotiate in this game?',
        choices=C.StandardChoices,
    )

# PAGES
class SurveyPage1(Page):
    form_model = 'player'
    form_fields = ['item1A']


page_sequence = [
    SurveyPage1
]
