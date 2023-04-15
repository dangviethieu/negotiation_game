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
    SecondChoices = [
        [1, 'Completely False'],
        [2, 'Somewhat False'],
        [3, 'Somewhat True'],
        [4, 'Completely True']
    ]
    ThirdChoices = [
        0, 1, 2, 3, 4, 5, 6
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
    item2A = models.IntegerField(
        label='How satisfied were you with the settlement?',
        choices=C.StandardChoices,
    )
    item3A = models.IntegerField(
        label='How satisfied were you with your performance during the negotiation?',
        choices=C.StandardChoices,
    )
    item4A = models.IntegerField(
        label='How enjoyable did you feel in this negotiation?',
        choices=C.StandardChoices,
    )
    item5A = models.IntegerField(
        label='How unpleasant did you feel in this negotiation?',
        choices=C.StandardChoices,
    )
    item6A = models.IntegerField(
        label='How comfortable did you feel with your partner in this negotiation?',
        choices=C.StandardChoices,
    )
    item7A = models.IntegerField(
        label='How interested are you in your partner in this negotiation?',
        choices=C.StandardChoices,
    )
    item8A = models.IntegerField(
        label='How much do you trust your partner after interacting with them?',
        choices=C.StandardChoices,
    )
    item9A = models.IntegerField(
        label='How likely do you expect the future negotiations with your partner in this negotiation?',
        choices=C.StandardChoices,
    )
    item10A = models.IntegerField(
        label='To what extent did you rely on your expectation of your partner\'s integrity to make a side payment decision?',
        choices=C.StandardChoices,
    )
    item1B = models.IntegerField(
        label='The business code of conduct and ethics of my company is ambitious with non-tolerance of corruption.',
        choices=C.SecondChoices,
    )
    item2B = models.IntegerField(
        label='The business code of conduct and ethics of my company does not provide decision making criteria for dealing with corruption problems.',
        choices=C.SecondChoices,
    )
    item3B = models.IntegerField(
        label='In my company, it is very important to follow the company\'s code and rules.',
        choices=C.SecondChoices,
    )
    item4B = models.IntegerField(
        label='In my company, everyone is expected to stick by the company\'s code and rules.',
        choices=C.SecondChoices,
    )
    item5B = models.IntegerField(
        label='People in my company strictly obey the company\'s rules and policies.',
        choices=C.SecondChoices,
    )
    item6B = models.IntegerField(
        label='The rules on bribery at my company are easy to avoid.',
        choices=C.SecondChoices,
    )
    item7B = models.IntegerField(
        label='I find it difficult to comply with bribery rules at my company.',
        choices=C.SecondChoices,
    )
    item8B = models.IntegerField(
        label='I assume that my company allows to conduct a bribery transaction with customers/counterparts without any risk.',
        choices=C.SecondChoices,
    )
    item9B = models.IntegerField(
        label='The business code of my company clearly states negative consequences/penalties for the violation of bribery rules.',
        choices=C.SecondChoices,
    )
    itemC = models.LongStringField(
        label='Is there anything else you wish to share after the negotiation experiment (optional)?',
        blank=True,
    )
    itemD = models.IntegerField(
        label='How much do you trust your partner after interacting with them?',
        blank=True,
    )
    item1D = models.IntegerField(
        label='Guilty?',
        choices=C.ThirdChoices,
    )
    item2D = models.IntegerField(
        label='Anxious?',
        choices=C.ThirdChoices,
    )
    item3D = models.IntegerField(
        label='Pleasant?',
        choices=C.ThirdChoices,
    )
    itemE = models.IntegerField(
        label='How did you feel being offered or being requested the side payment?',
        blank=True,
    )
    item1E = models.IntegerField(
        label='Angry?',
        choices=C.ThirdChoices,
    )
    item2E = models.IntegerField(
        label='Pleasant?',
        choices=C.ThirdChoices,
    )
    item3E = models.IntegerField(
        label='Anxious?',
        choices=C.ThirdChoices,
    )
    item4E = models.IntegerField(
        label='Empathetic?',
        choices=C.ThirdChoices,
    )
    item5E = models.IntegerField(
        label='Disappointed?',
        choices=C.ThirdChoices,
    )
    itemF = models.IntegerField(
        label='How did you feel when your side payment offer/request was rejected?',
        blank=True,
    )
    item1F = models.IntegerField(
        label='Angry?',
        choices=C.ThirdChoices,
    )
    item2F = models.IntegerField(
        label='Pleasant?',
        choices=C.ThirdChoices,
    )
    item3F = models.IntegerField(
        label='Disappointed?',
        choices=C.ThirdChoices,
    )
    item4F = models.IntegerField(
        label='Empathetic?',
        choices=C.ThirdChoices,
    )
    item5F = models.IntegerField(
        label='Anxious?',
        choices=C.ThirdChoices,
    )

# PAGES
class SurveyPage1(Page):
    form_model = 'player'
    form_fields = ['item1A', 'item2A', 'item3A', 'item4A', 'item5A', 'item6A', 'item7A', 'item8A', 'item9A', 'item10A']
    
    def vars_for_template(self):
        return {
            'progress': 0
        }

class SurveyPage2(Page):
    form_model = 'player'
    form_fields = ['item1D', 'item2D', 'item3D']
    
    def vars_for_template(self):
        return {
            'progress': 40
        }

class SurveyPage3(Page):
    form_model = 'player'
    form_fields = ['item1E', 'item2E', 'item3E', 'item4E', 'item5E']
    
    def vars_for_template(self):
        return {
            'progress': 43
        }

class SurveyPage4(Page):
    form_model = 'player'
    form_fields = ['item1F', 'item2F', 'item3F', 'item4F', 'item5F']
    
    def vars_for_template(self):
        return {
            'progress': 48
        }

class SurveyPage5(Page):
    form_model = 'player'
    form_fields = ['item1B', 'item2B', 'item3B', 'item4B', 'item5B', 'item6B', 'item7B', 'item8B', 'item9B', 'itemC']
    
    def vars_for_template(self):
        return {
            'progress': 55
        }
    
class ResultsSurveyGame(Page):
    form_model = 'player'

page_sequence = [
    SurveyPage1,
    SurveyPage2,
    SurveyPage3,
    SurveyPage4,
    SurveyPage5,
    ResultsSurveyGame
]
