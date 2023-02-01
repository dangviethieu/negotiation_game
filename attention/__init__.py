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
        label='I read and agree with the consent and attention pledge above.'
    )
    attention_1 = models.BooleanField(
        widget=widgets.CheckboxInput,
        label='Devote my full attention to the game and not engage in other activities, such as browsing the internet.'
    )
    attention_2 = models.BooleanField(
        widget=widgets.CheckboxInput,
        label='Put my mobile device in silent mode and not use them during the game.'
    )

# PAGES
class ConsentPage(Page):
    form_model = 'player'
    form_fields = ['consent_1']

class AttentionPage(Page):
    form_model = 'player'
    form_fields = ['attention_1', 'attention_2']


page_sequence = [
    ConsentPage, AttentionPage
]
