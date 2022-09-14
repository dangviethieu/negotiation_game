from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'negotiation_game'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    SELLER_ROLE = 'Seller'
    BUYER_ROLE = 'Buyer'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    buyer_offer_bribe = models.BooleanField(initial=False)
    seller_offer_bribe = models.BooleanField(initial=False)
    deal_fixed_sum = models.IntegerField()
    deal_percentage = models.IntegerField()
    is_finished = models.BooleanField(initial=False)


class Player(BasePlayer):
    buyer_offer_bribe = models.BooleanField(initial=False)
    seller_offer_bribe = models.BooleanField(initial=False)
    fixed_sum_proposed = models.IntegerField(initial=0, min=0, max=C.ENDOWMENT)
    fixed_sum_accepted = models.IntegerField(initial=0, min=0, max=C.ENDOWMENT)
    percentage_proposed = models.IntegerField(initial=0, min=0, max=100)
    percentage_accepted = models.IntegerField(initial=0, min=0, max=100)
    is_reject = models.BooleanField(initial=False)

# PAGES
def set_payoffs_after_offer_bribe(group: Group):
    p1, p2 = group.get_players()
    group.buyer_offer_bribe = p1.buyer_offer_bribe
    group.seller_offer_bribe = p2.seller_offer_bribe
    if group.buyer_offer_bribe and group.seller_offer_bribe:
        group.is_finished = False
    else:
        group.is_finished = True

class BuyerOfferBribe(Page):
    form_model = 'player'
    form_fields = ['buyer_offer_bribe']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class ResultsWaitSellerAcceptBribePage(WaitPage):
    pass

class SellerAcceptBribe(Page):
    form_model = 'player'
    form_fields = ['seller_offer_bribe']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'buyer_offer_bribe': player.group.buyer_offer_bribe,
        }

class ResultsWaitBuyerAcceptBribePage(WaitPage):
    after_all_players_arrive = 'set_payoffs_after_offer_bribe'

class OfferFixedSum(Page):

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        deal_fixed_sum = group.field_maybe_none('deal_fixed_sum')
        return (not player.group.is_finished) and deal_fixed_sum is None

    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_role=player.get_others_in_subsession()[0].role)

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        [other] = player.get_others_in_group()
        if 'amount' in data:
            try:
                amount = int(data['amount'])
            except ValueError:
                return dict(error='Please enter a number.')
            if data['type'] == 'accept':
                if amount == other.fixed_sum_proposed:
                    player.fixed_sum_accepted = amount
                    other.fixed_sum_accepted = amount
                    group.deal_fixed_sum = amount
                    return {0: dict(finished=True)}
            if data['type'] == 'reject':
                group.is_finished = True
                player.is_reject = True
                return {0: dict(finished=True)}
            if data['type'] == 'propose':
                player.fixed_sum_proposed = amount
        proposals = []
        for p in group.get_players():
            fixed_sum_proposed = p.field_maybe_none('fixed_sum_proposed')
            if fixed_sum_proposed is not None:
                proposals.append([p.id_in_group, fixed_sum_proposed])
        return {0: dict(proposals=proposals)}

    @staticmethod
    def error_message(player: Player, values):
        group = player.group
        deal_fixed_sum = group.field_maybe_none('deal_fixed_sum')
        is_finished = group.field_maybe_none('is_finished')
        if deal_fixed_sum is None and is_finished is None:
            return "Game not finished yet"

class OfferPercentage(Page):

    @staticmethod
    def is_displayed(player: Player):
        group = player.group
        deal_percentage = group.field_maybe_none('deal_percentage')
        return (not player.group.is_finished) and deal_percentage is None

    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_role=player.get_others_in_subsession()[0].role)

    @staticmethod
    def js_vars(player: Player):
        return dict(my_id=player.id_in_group)

    @staticmethod
    def live_method(player: Player, data):
        group = player.group
        [other] = player.get_others_in_group()
        if 'amount' in data:
            try:
                amount = int(data['amount'])
            except ValueError:
                return dict(error='Please enter a number.')
            if data['type'] == 'accept':
                if amount == other.percentage_proposed:
                    player.percentage_accepted = amount
                    other.percentage_accepted = amount
                    group.is_finished = True
                    group.deal_percentage = amount
                    return {0: dict(finished=True)}
            if data['type'] == 'reject':
                group.is_finished = True
                player.is_reject = True
                return {0: dict(finished=True)}
            if data['type'] == 'propose':
                player.percentage_proposed = amount
        proposals = []
        for p in group.get_players():
            percentage_proposed = p.field_maybe_none('percentage_proposed')
            if percentage_proposed is not None:
                proposals.append([p.id_in_group, percentage_proposed])
        return {0: dict(proposals=proposals)}

    @staticmethod
    def error_message(player: Player, values):
        group = player.group
        deal_percentage = group.field_maybe_none('deal_percentage')
        is_finished = group.field_maybe_none('is_finished')
        if deal_percentage is None and is_finished is None:
            return "Game not finished yet"

class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        deal_fixed_sum = group.field_maybe_none('deal_fixed_sum')
        deal_percentage = group.field_maybe_none('deal_percentage')
        is_negation_game_successful = False
        if deal_fixed_sum is not None and deal_percentage is not None:
            is_negation_game_successful = True
        return dict(
            other_role=player.get_others_in_subsession()[0].role,
            deal_fixed_sum=deal_fixed_sum,
            deal_percentage=deal_percentage,
            is_negation_game_successful=is_negation_game_successful,
            is_reject=player.is_reject,
        )


page_sequence = [BuyerOfferBribe, ResultsWaitSellerAcceptBribePage, SellerAcceptBribe, ResultsWaitBuyerAcceptBribePage, OfferFixedSum, OfferPercentage, Results]
