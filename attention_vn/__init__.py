from otree.api import *


doc = """
This is an attention check
"""


class C(BaseConstants):
    NAME_IN_URL = 'attention_vn'
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
        label='Tôi đã đọc và đồng ý với cam kết chấp thuận nghiên cứu và tập trung chú ý ở trên.'
    )

# PAGES
class ConsentPage(Page):
    form_model = 'player'
    form_fields = ['consent_1']


page_sequence = [
    ConsentPage
]
