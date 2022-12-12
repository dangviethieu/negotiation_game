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
        label='I confirm that I have read and understand the information sheet for the above study. I have had the opportunity to consider the information, ask questions and have had these answered satisfactorily'
    )
    consent_2 = models.BooleanField(
        widget=widgets.CheckboxInput,
        label='I understand that my participation is voluntary and that I am free to withdraw up to 4 weeks after taking part in the study without giving any reason, without my legal rights being affected.'
    )
    consent_3 = models.BooleanField(
        widget=widgets.CheckboxInput,
        label='I understand that data collected will be used, in anonymised form, for academic and policy outputs. I give permission for the research team to have access to my responses in the online game.'
    )
    consent_4 = models.BooleanField(
        widget=widgets.CheckboxInput,
        label='I agree to take part in the above study.'
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
    form_fields = ['consent_1', 'consent_2', 'consent_3', 'consent_4']

class AttentionPage(Page):
    form_model = 'player'
    form_fields = ['attention_1', 'attention_2']


page_sequence = [
    ConsentPage, AttentionPage
]
