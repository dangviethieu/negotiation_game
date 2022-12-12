from otree.api import *


doc = """
This is a simple questionnaire before the game
"""


class C(BaseConstants):
    NAME_IN_URL = 'question_info'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    language = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, 'No Working Proficiency'],
            [2, 'Limited Working Proficiency'],
            [3, 'Professional Working Proficiency'],
            [4, 'Full Professional Proficiency']
        ]
    )
    address = models.StringField(
        widget=widgets.RadioSelect,
        choices=[
            ['North Vietnam', 'North Vietnam'],
            ['Middle Vietnam', 'Middle Vietnam'],
            ['South Vietnam', 'South Vietnam'],
            ['Other', 'Other']
        ]
    )

# PAGES
class QuestionBeforeOffer(Page):
    form_model = 'player'
    form_fields = ['language', 'address']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['language'] = player.language
        player.participant.vars['address'] = player.address

page_sequence = [
    QuestionBeforeOffer,
]
