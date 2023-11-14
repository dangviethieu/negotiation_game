from otree.api import *
from .helper import User, EN_LANGUAGE, get_user_from_excel
import random


doc = """
This is a negotiation game
"""


class C(BaseConstants):
    NAME_IN_URL = 'negotiation_en_game_info'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    BUYER_ROLE = 'Buyer'
    SELLER_ROLE = 'Seller'
    OFFER_NO_BRIBE = 0
    OFFER_FIXED_SUM = 1
    OFFER_PERCENTAGE = 2
    ACCEPT_NO_BRIBE = 0
    OFFER_NEW_BRIBE = 1
    REJECT_NO_BRIBE = 2
    NEGOTIATION_GAME = True
    TIMEOUT_NEGOTIATION = 20 * 60


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    buyer_offer_bribe = models.IntegerField(initial=0)
    seller_offer_no_bribe = models.IntegerField(initial=0)
    seller_offer_new_bribe = models.IntegerField(initial=0)
    deal_fixed_sum = models.IntegerField()
    buyer_accepted_fixed_sum = models.BooleanField()
    seller_accepted_fixed_sum = models.BooleanField()
    deal_percentage = models.IntegerField()
    buyer_accepted_percentage = models.BooleanField()
    seller_accepted_percentage = models.BooleanField()
    next_negotiation_game = models.BooleanField()

class Player(BasePlayer):
    offer_bribe = models.IntegerField(initial=0)
    seller_offer_new_bribe = models.IntegerField(initial=0)
    fixed_sum_proposed = models.IntegerField(initial=0, min=0, max=C.ENDOWMENT)
    accepted_negotiation_from_fixed_sum = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, 'Accept'],
            [2, 'Reject'],
            [3, 'Reject with new proposal']
        ]
    )
    percentage_proposed = models.IntegerField(initial=2, choices=[2, 5, 10])
    accepted_negotiation_from_percentage = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[
            [1, 'Accept'],
            [2, 'Reject'],
            [3, 'Reject with new proposal']
        ]
    )
    address = models.StringField()

# PAGES
def set_payoffs_after_offer_bribe(group: Group):
    p1, p2 = group.get_players()
    group.buyer_offer_bribe = p1.offer_bribe
    group.seller_offer_no_bribe = p2.offer_bribe
    if p1.offer_bribe == C.OFFER_NO_BRIBE:
        if p2.offer_bribe == C.ACCEPT_NO_BRIBE:
            group.seller_offer_no_bribe = C.ACCEPT_NO_BRIBE
        elif p2.offer_bribe == C.OFFER_NEW_BRIBE:
            group.seller_offer_no_bribe = C.OFFER_NEW_BRIBE
            if p2.seller_offer_new_bribe == C.OFFER_FIXED_SUM:
                group.seller_offer_new_bribe = C.OFFER_FIXED_SUM
                if p1.accepted_negotiation_from_fixed_sum == 1:
                    group.buyer_accepted_fixed_sum = True
                    group.deal_fixed_sum = p1.fixed_sum_proposed
                    group.next_negotiation_game = True
                elif p1.accepted_negotiation_from_fixed_sum == 2:
                    group.buyer_accepted_fixed_sum = False
            elif p2.seller_offer_new_bribe == C.OFFER_PERCENTAGE:
                group.seller_offer_new_bribe = C.OFFER_PERCENTAGE
                if p1.accepted_negotiation_from_percentage == 1:
                    group.buyer_accepted_percentage = True
                    group.deal_percentage = p1.percentage_proposed
                    group.next_negotiation_game = True
                elif p1.accepted_negotiation_from_percentage == 2:
                    group.buyer_accepted_percentage = False
        elif p2.offer_bribe == C.REJECT_NO_BRIBE:
            group.seller_offer_no_bribe = C.REJECT_NO_BRIBE
    elif p1.offer_bribe == C.OFFER_FIXED_SUM:
        if p2.accepted_negotiation_from_fixed_sum == 1:
            group.deal_fixed_sum = p1.fixed_sum_proposed
            group.seller_accepted_fixed_sum = True
            group.next_negotiation_game = True
        elif p2.accepted_negotiation_from_fixed_sum == 2:
            group.seller_accepted_fixed_sum = False
        elif p2.accepted_negotiation_from_fixed_sum == 3:
            if p1.accepted_negotiation_from_fixed_sum == 1:
                group.deal_fixed_sum = p2.fixed_sum_proposed
                group.buyer_accepted_fixed_sum = True
                group.next_negotiation_game = True
            else:
                group.buyer_accepted_fixed_sum = False
    elif p1.offer_bribe == C.OFFER_PERCENTAGE:
        if p2.accepted_negotiation_from_percentage == 1:
            group.deal_percentage = p1.percentage_proposed
            group.seller_accepted_percentage = True
            group.next_negotiation_game = True
        elif p2.accepted_negotiation_from_percentage == 2:
            group.seller_accepted_percentage = False
        elif p2.accepted_negotiation_from_percentage == 3:
            if p1.accepted_negotiation_from_percentage == 1:
                group.deal_percentage = p2.percentage_proposed
                group.buyer_accepted_percentage = True
                group.next_negotiation_game = True
            else:
                group.buyer_accepted_percentage = False

class WaitGroupPlayersPage(WaitPage):
    group_by_arrival_time = True

def group_by_arrival_time_method(subsession, waiting_players):
    # # matching players with ID csv file
    # players_vn_language_vn = []
    # players_vn_language_en = []
    players_en = []
    players_vn = []
    for player in waiting_players:
        id = player.participant.label
        # check if address, language from previous game
        if player.participant.vars.get('address'):
            user = User(id=id, address=player.participant.vars.get('address'), language=player.participant.vars.get('language'), email="")
        else:
            user = get_user_from_excel(id)
        if user is not None:
            player.address = user.address
            if 'Vietnam' not in user.address:
                player._role = C.BUYER_ROLE
                players_en.append(player)
            # elif int(user.language) <= EN_LANGUAGE:
            #     players_vn_language_vn.append(player)
            # else:
            #     players_vn_language_en.append(player)
            else:
                player._role = C.SELLER_ROLE
                players_vn.append(player)
    # if len(players_en) >= 1 and len(players_vn_language_en) >= 1:
    #     return [players_en[0], players_vn_language_en[0]]
    # elif len(players_vn_language_vn) > 1:
    #     return [players_vn_language_vn[0], players_vn_language_vn[1]]
    # if len(waiting_players) > 1:
    #     return [waiting_players[0], waiting_players[1]]
    if len(players_en) >= 1 and len(players_vn) >= 1:
        # ret = [players_en[0], players_vn[0]]
        # random.shuffle(ret)
        # return ret
        return [players_en[0], players_vn[0]]

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
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            other_player=player.get_others_in_group()[0]
        )

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
    form_fields = ['offer_bribe', 'seller_offer_new_bribe']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.SELLER_ROLE and player.group.get_player_by_role(C.BUYER_ROLE).offer_bribe == C.OFFER_NO_BRIBE
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            other_player=player.get_others_in_group()[0]
        )
    
class SellerOfferFixedSum(Page):
    form_model = 'player'
    form_fields = ['fixed_sum_proposed']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.SELLER_ROLE and \
            player.group.get_player_by_role(C.SELLER_ROLE).offer_bribe == C.OFFER_NEW_BRIBE and \
                player.group.get_player_by_role(C.SELLER_ROLE).seller_offer_new_bribe == C.OFFER_FIXED_SUM
                
class SellerOfferPercentage(Page):
    form_model = 'player'
    form_fields = ['percentage_proposed']
    
    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.SELLER_ROLE and \
            player.group.get_player_by_role(C.SELLER_ROLE).offer_bribe == C.OFFER_NEW_BRIBE and \
                player.group.get_player_by_role(C.SELLER_ROLE).seller_offer_new_bribe == C.OFFER_PERCENTAGE

class SellerAcceptFixedSum(Page):
    form_model = 'player'
    form_fields = ['fixed_sum_proposed', 'accepted_negotiation_from_fixed_sum']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.SELLER_ROLE and player.group.get_player_by_role(C.BUYER_ROLE).offer_bribe == C.OFFER_FIXED_SUM

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            other_player=player.get_others_in_group()[0],
            fixed_sum_proposed=player.group.get_player_by_role(C.BUYER_ROLE).fixed_sum_proposed
        )

class SellerAcceptPercentage(Page):
    form_model = 'player'
    form_fields = ['percentage_proposed', 'accepted_negotiation_from_percentage']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.SELLER_ROLE and player.group.get_player_by_role(C.BUYER_ROLE).offer_bribe == C.OFFER_PERCENTAGE

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            other_player=player.get_others_in_group()[0],
            percentage_proposed=player.group.get_player_by_role(C.BUYER_ROLE).percentage_proposed
        )

class WaitForBuyerAcceptBribePage(WaitPage):
    pass

class BuyerAcceptNewBribeWithFixedSum(Page):
    form_model = 'player'
    form_fields = ['accepted_negotiation_from_fixed_sum']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.BUYER_ROLE and \
            player.group.get_player_by_role(C.SELLER_ROLE).offer_bribe == C.OFFER_NEW_BRIBE and \
                player.group.get_player_by_role(C.SELLER_ROLE).seller_offer_new_bribe == C.OFFER_FIXED_SUM

    @staticmethod
    def vars_for_template(player: Player):
        return dict(fixed_sum_proposed=player.group.get_player_by_role(C.SELLER_ROLE).fixed_sum_proposed)

class BuyerAcceptNewBribeWithPercentage(Page):
    form_model = 'player'
    form_fields = ['accepted_negotiation_from_percentage']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.BUYER_ROLE and \
            player.group.get_player_by_role(C.SELLER_ROLE).offer_bribe == C.OFFER_NEW_BRIBE and \
                player.group.get_player_by_role(C.SELLER_ROLE).seller_offer_new_bribe == C.OFFER_PERCENTAGE

    @staticmethod
    def vars_for_template(player: Player):
        return dict(percentage_proposed=player.group.get_player_by_role(C.SELLER_ROLE).percentage_proposed)

class BuyerAcceptFixedSum(Page):
    form_model = 'player'
    form_fields = ['accepted_negotiation_from_fixed_sum']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.BUYER_ROLE \
            and player.offer_bribe == C.OFFER_FIXED_SUM \
            and player.group.get_player_by_role(C.SELLER_ROLE).accepted_negotiation_from_fixed_sum == 3

    @staticmethod
    def vars_for_template(player: Player):
        return dict(fixed_sum_proposed=player.group.get_player_by_role(C.SELLER_ROLE).fixed_sum_proposed)

class BuyerAcceptPercentage(Page):
    form_model = 'player'
    form_fields = ['accepted_negotiation_from_percentage']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == C.BUYER_ROLE \
            and player.offer_bribe == C.OFFER_PERCENTAGE \
            and player.group.get_player_by_role(C.SELLER_ROLE).accepted_negotiation_from_percentage == 3

    @staticmethod
    def vars_for_template(player: Player):
        return dict(percentage_proposed=player.group.get_player_by_role(C.SELLER_ROLE).percentage_proposed)

class ResultsWaitBuyerAcceptBribePage(WaitPage):
    after_all_players_arrive = 'set_payoffs_after_offer_bribe'

class ResultsPreNegotiationGame(Page):
    form_model = 'player'

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
            seller_offer_new_bribe=group.seller_offer_new_bribe,
            deal_fixed_sum=deal_fixed_sum,
            buyer_accepted_fixed_sum=buyer_accepted_fixed_sum,
            seller_accepted_fixed_sum=seller_accepted_fixed_sum,
            deal_percentage=deal_percentage,
            buyer_accepted_percentage=buyer_accepted_percentage,
            seller_accepted_percentage=seller_accepted_percentage,
        )

class WaitForAllUserGoToNegotiationGamePage(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return \
            (group.buyer_offer_bribe == C.OFFER_NO_BRIBE and (group.seller_offer_no_bribe == C.ACCEPT_NO_BRIBE or 
                group.field_maybe_none('seller_accepted_fixed_sum') == True or group.field_maybe_none('buyer_accepted_fixed_sum') == True or
                group.field_maybe_none('seller_accepted_percentage') == True or group.field_maybe_none('buyer_accepted_percentage') == True)
            ) or \
            (group.buyer_offer_bribe == C.OFFER_FIXED_SUM and (
                group.field_maybe_none('seller_accepted_fixed_sum') == True or group.field_maybe_none('buyer_accepted_fixed_sum') == True)
            ) or \
            (group.buyer_offer_bribe == C.OFFER_PERCENTAGE and (
                group.field_maybe_none('seller_accepted_percentage') == True or group.field_maybe_none('buyer_accepted_percentage') == True)
            )

class NegotiationGame(Page):
    form_model = 'player'
    timeout_seconds = C.TIMEOUT_NEGOTIATION

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return \
            (group.buyer_offer_bribe == C.OFFER_NO_BRIBE and (group.seller_offer_no_bribe == C.ACCEPT_NO_BRIBE or 
                group.field_maybe_none('seller_accepted_fixed_sum') == True or group.field_maybe_none('buyer_accepted_fixed_sum') == True or
                group.field_maybe_none('seller_accepted_percentage') == True or group.field_maybe_none('buyer_accepted_percentage') == True)
            ) or \
            (group.buyer_offer_bribe == C.OFFER_FIXED_SUM and (
                group.field_maybe_none('seller_accepted_fixed_sum') == True or group.field_maybe_none('buyer_accepted_fixed_sum') == True)
            ) or \
            (group.buyer_offer_bribe == C.OFFER_PERCENTAGE and (
                group.field_maybe_none('seller_accepted_percentage') == True or group.field_maybe_none('buyer_accepted_percentage') == True)
            )

class ResultsNegotiationGame(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        return \
            (group.buyer_offer_bribe == C.OFFER_NO_BRIBE and (group.seller_offer_no_bribe == C.ACCEPT_NO_BRIBE or 
                group.field_maybe_none('seller_accepted_fixed_sum') == True or group.field_maybe_none('buyer_accepted_fixed_sum') == True or
                group.field_maybe_none('seller_accepted_percentage') == True or group.field_maybe_none('buyer_accepted_percentage') == True)
            ) or \
            (group.buyer_offer_bribe == C.OFFER_FIXED_SUM and (
                group.field_maybe_none('seller_accepted_fixed_sum') == True or group.field_maybe_none('buyer_accepted_fixed_sum') == True)
            ) or \
            (group.buyer_offer_bribe == C.OFFER_PERCENTAGE and (
                group.field_maybe_none('seller_accepted_percentage') == True or group.field_maybe_none('buyer_accepted_percentage') == True)
            )

page_sequence = [
    WaitGroupPlayersPage,
    BuyerPreOffer,
    SellerPreOffer,
    WaitForBuyerSendOfferPage,
    BuyerOfferBribe,
    BuyerOfferFixedSum,
    BuyerOfferPercentage,
    WaitForSellerAcceptBribePage,
    SellerAcceptNoBribe,
    SellerOfferFixedSum,
    SellerOfferPercentage,
    SellerAcceptFixedSum,
    SellerAcceptPercentage,
    WaitForBuyerAcceptBribePage,
    BuyerAcceptNewBribeWithFixedSum,
    BuyerAcceptNewBribeWithPercentage,
    BuyerAcceptFixedSum,
    BuyerAcceptPercentage,
    ResultsWaitBuyerAcceptBribePage,
    ResultsPreNegotiationGame,
    WaitForAllUserGoToNegotiationGamePage,
    NegotiationGame,
    ResultsNegotiationGame
]
