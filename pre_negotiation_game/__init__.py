from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'negotiation_game'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    BUYER_ROLE = 'Buyer'
    SELLER_ROLE = 'Seller'
    OFFER_NO_BRIBE = 0
    OFFER_FIXED_SUM = 1
    OFFER_PERCENTAGE = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    buyer_offer_bribe = models.IntegerField(initial=0)
    seller_offer_no_bribe = models.BooleanField(initial=False)
    deal_fixed_sum = models.IntegerField()
    buyer_accepted_fixed_sum = models.BooleanField()
    seller_accepted_fixed_sum = models.BooleanField()
    deal_percentage = models.IntegerField()
    buyer_accepted_percentage = models.BooleanField()
    seller_accepted_percentage = models.BooleanField()

class Player(BasePlayer):
    offer_bribe = models.IntegerField(initial=0)
    fixed_sum_proposed = models.IntegerField(initial=0, min=0, max=C.ENDOWMENT)
    accepted_neogtiation_from_fixed_sum = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, 'Accept'],
            [2, 'Reject'],
            [3, 'Reject with new proposal']
        ]
    )
    percentage_proposed = models.IntegerField(initial=2, choices=[2, 5, 10])
    accepted_neogtiation_from_percentage = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, 'Accept'],
            [2, 'Reject'],
            [3, 'Reject with new proposal']
        ]
    )

# PAGES
def set_payoffs_after_offer_bribe(group: Group):
    p1, p2 = group.get_players()
    group.buyer_offer_bribe = p1.offer_bribe
    group.seller_offer_no_bribe = p2.offer_bribe
    if p1.offer_bribe == C.OFFER_FIXED_SUM:
        if p2.accepted_neogtiation_from_fixed_sum == 1:
            group.deal_fixed_sum = p1.fixed_sum_proposed
            group.seller_accepted_fixed_sum = True
        elif p2.accepted_neogtiation_from_fixed_sum == 2:
            group.seller_accepted_fixed_sum = False
        elif p2.accepted_neogtiation_from_fixed_sum == 3:
            if p1.accepted_neogtiation_from_fixed_sum == 1:
                group.deal_fixed_sum = p2.fixed_sum_proposed
                group.buyer_accepted_fixed_sum = True
            else:
                group.buyer_accepted_fixed_sum = False
    if p1.offer_bribe == C.OFFER_PERCENTAGE:
        if p2.accepted_neogtiation_from_percentage == 1:
            group.deal_percentage = p1.percentage_proposed
            group.seller_accepted_percentage = True
        elif p2.accepted_neogtiation_from_percentage == 2:
            group.seller_accepted_percentage = False
        elif p2.accepted_neogtiation_from_percentage == 3:
            if p1.accepted_neogtiation_from_percentage == 1:
                group.deal_percentage = p2.percentage_proposed
                group.buyer_accepted_percentage = True
            else:
                group.buyer_accepted_percentage = False

class BuyerPreOffer(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.BUYER_ROLE

class SellerPreOffer(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.SELLER_ROLE

class WaitForBuyerSendOfferPage(WaitPage):
    pass

class BuyerOfferBribe(Page):
    form_model = 'player'
    form_fields = ['offer_bribe']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.BUYER_ROLE

class BuyerOfferFixedSum(Page):
    form_model = 'player'
    form_fields = ['fixed_sum_proposed']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.BUYER_ROLE and player.offer_bribe == 1

class BuyerOfferPercentage(Page):
    form_model = 'player'
    form_fields = ['percentage_proposed']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.BUYER_ROLE and player.offer_bribe == C.OFFER_PERCENTAGE

class WaitForSellerAcceptBribePage(WaitPage):
    pass

class SellerAcceptNoBribe(Page):
    form_model = 'player'
    form_fields = ['offer_bribe']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.SELLER_ROLE and player.group.get_player_by_role(C.BUYER_ROLE).offer_bribe == C.OFFER_NO_BRIBE

class SellerAcceptFixedSum(Page):
    form_model = 'player'
    form_fields = ['fixed_sum_proposed', 'accepted_neogtiation_from_fixed_sum']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.SELLER_ROLE and player.group.get_player_by_role(C.BUYER_ROLE).offer_bribe == C.OFFER_FIXED_SUM

    @staticmethod
    def vars_for_template(player: Player):
        return dict(fixed_sum_proposed=player.group.get_player_by_role(C.BUYER_ROLE).fixed_sum_proposed)

class SellerAcceptPercentage(Page):
    form_model = 'player'
    form_fields = ['percentage_proposed', 'accepted_neogtiation_from_percentage']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.SELLER_ROLE and player.group.get_player_by_role(C.BUYER_ROLE).offer_bribe == C.OFFER_PERCENTAGE

    @staticmethod
    def vars_for_template(player: Player):
        return dict(percentage_proposed=player.group.get_player_by_role(C.BUYER_ROLE).percentage_proposed)

class WaitForBuyerAcceptBribePage(WaitPage):
    pass

class BuyerAcceptFixedSum(Page):
    form_model = 'player'
    form_fields = ['accepted_neogtiation_from_fixed_sum']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.BUYER_ROLE \
            and player.offer_bribe == C.OFFER_FIXED_SUM \
            and player.group.get_player_by_role(C.SELLER_ROLE).accepted_neogtiation_from_fixed_sum == 3

    @staticmethod
    def vars_for_template(player: Player):
        return dict(fixed_sum_proposed=player.group.get_player_by_role(C.SELLER_ROLE).fixed_sum_proposed)

class BuyerAcceptPercentage(Page):
    form_model = 'player'
    form_fields = ['accepted_neogtiation_from_percentage']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.BUYER_ROLE \
            and player.offer_bribe == C.OFFER_PERCENTAGE \
            and player.group.get_player_by_role(C.SELLER_ROLE).accepted_neogtiation_from_percentage == 3

    @staticmethod
    def vars_for_template(player: Player):
        return dict(percentage_proposed=player.group.get_player_by_role(C.SELLER_ROLE).percentage_proposed)

class ResultsWaitBuyerAcceptBribePage(WaitPage):
    after_all_players_arrive = 'set_payoffs_after_offer_bribe'

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        deal_fixed_sum = group.field_maybe_none('deal_fixed_sum')
        buyer_accepted_fixed_sum = group.field_maybe_none('buyer_accepted_fixed_sum')
        seller_accepted_fixed_sum = group.field_maybe_none('seller_accepted_fixed_sum')
        deal_percentage = group.field_maybe_none('deal_percentage')
        buyer_accepted_percentage = group.field_maybe_none('buyer_accepted_percentage')
        seller_accepted_percentage = group.field_maybe_none('seller_accepted_percentage')
        return dict(
            other_role=player.get_others_in_subsession()[0].role,
            buyer_offer_bribe=group.buyer_offer_bribe,
            seller_offer_no_bribe=group.seller_offer_no_bribe,
            deal_fixed_sum=deal_fixed_sum,
            buyer_accepted_fixed_sum=buyer_accepted_fixed_sum,
            seller_accepted_fixed_sum=seller_accepted_fixed_sum,
            deal_percentage=deal_percentage,
            buyer_accepted_percentage=buyer_accepted_percentage,
            seller_accepted_percentage=seller_accepted_percentage,
        )


page_sequence = [
    BuyerPreOffer,
    SellerPreOffer,
    WaitForBuyerSendOfferPage,
    BuyerOfferBribe,
    BuyerOfferFixedSum,
    BuyerOfferPercentage,
    WaitForSellerAcceptBribePage,
    SellerAcceptNoBribe,
    SellerAcceptFixedSum,
    SellerAcceptPercentage,
    WaitForBuyerAcceptBribePage,
    BuyerAcceptFixedSum,
    BuyerAcceptPercentage,
    ResultsWaitBuyerAcceptBribePage,
    Results
]
