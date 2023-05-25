from otree.api import *


doc = """
This is an attention check survey. It is used to check if the participant is paying attention to the game.
"""


class C(BaseConstants):
    NAME_IN_URL = 'survey_vn'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    StandardChoices = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    ]
    SecondChoices = [
        [1, 'Hoàn toàn sai'],
        [2, 'Hơi sai'],
        [3, 'Hơi đúng'],
        [4, 'Hoàn toàn đúng']
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
        label='Bạn đánh giá mình đã thương lượng tốt như thế nào trong trò chơi này?',
        choices=C.StandardChoices,
    )
    item2A = models.IntegerField(
        label='Bạn hài lòng như thế nào với kết quả giá được thỏa thuận?',
        choices=C.StandardChoices,
    )
    item3A = models.IntegerField(
        label='Bạn hài lòng như thế nào với hiệu quả đàm phán của bạn trong quá trình thương lượng?',
        choices=C.StandardChoices,
    )
    item4A = models.IntegerField(
        label='Bạn cảm thấy thú vị như thế nào trong cuộc thương lượng này?',
        choices=C.StandardChoices,
    )
    item5A = models.IntegerField(
        label='Bạn cảm thấy khó chịu như thế nào trong cuộc thương lượng này?',
        choices=C.StandardChoices,
    )
    item6A = models.IntegerField(
        label='Bạn cảm thấy thoải mái như thế nào với đối tác của mình trong cuộc thương lượng này?',
        choices=C.StandardChoices,
    )
    item7A = models.IntegerField(
        label='Bạn ưa thích đối tác của mình ở mức độ nào trong cuộc thương lượng này?',
        choices=C.StandardChoices,
    )
    item8A = models.IntegerField(
        label='Bạn tin tưởng đối tác này của mình ở mức độ nào sau khi tương tác với họ?',
        choices=C.StandardChoices,
    )
    item9A = models.IntegerField(
        label='Bạn có mong đợi thương lượng với đối tác này trong các cuộc đàm phán trong tương lai?',
        choices=C.StandardChoices,
    )
    item10A = models.IntegerField(
        label='Bạn đã dựa vào kỳ vọng của mình về tính chính trực của đối tác ở mức độ nào để đưa ra quyết định liên quan đến khoản thanh toán phụ?',
        choices=C.StandardChoices,
    )
    item1B = models.IntegerField(
        label='Quy tắc ứng xử và đạo đức trong kinh doanh của công ty tôi là mơ hồ về sự không dung thứ cho hành vi tham nhũng.',
        choices=C.SecondChoices,
    )
    item2B = models.IntegerField(
        label='Quy tắc ứng xử và đạo đức trong kinh doanh của công ty tôi không đưa ra các tiêu chí ra quyết định khi gặp phải các tình huống tham nhũng.',
        choices=C.SecondChoices,
    )
    item3B = models.IntegerField(
        label='Trong công ty của tôi, việc tuân theo quy tắc và quy định của công ty là rất quan trọng.',
        choices=C.SecondChoices,
    )
    item4B = models.IntegerField(
        label='Trong công ty của tôi, mọi người được mong đợi phải tuân theo quy tắc và quy định của công ty.',
        choices=C.SecondChoices,
    )
    item5B = models.IntegerField(
        label='Mọi người trong công ty của tôi tuân thủ nghiêm ngặt các quy tắc, chính sách của công ty.',
        choices=C.SecondChoices,
    )
    item6B = models.IntegerField(
        label='Các quy định ngăn chặn hối lộ tại công ty của tôi rất dễ tránh.',
        choices=C.SecondChoices,
    )
    item7B = models.IntegerField(
        label='Tôi cảm thấy khó tuân thủ các quy định về hối lộ tại công ty của mình.',
        choices=C.SecondChoices,
    )
    item8B = models.IntegerField(
        label='Tôi nghĩ là công ty của tôi cho phép thực hiện giao dịch hối lộ với khách hàng/đối tác mà không gặp bất kỳ rủi ro nào.',
        choices=C.SecondChoices,
    )
    item9B = models.IntegerField(
        label='Quy tắc ứng xử kinh doanh của công ty tôi nêu rõ các hậu quả/hình phạt đối với hành vi vi phạm hối lộ.',
        choices=C.SecondChoices,
    )
    itemC = models.LongStringField(
        label='Có bất cứ điều gì khác mà bạn muốn chia sẻ sau khi tham gia nghiên cứu thử nghiệm này không (không bắt buộc)?',
        blank=True,
    )
    itemD = models.IntegerField(
        label='Bạn có cảm xúc nào sau đây khi thực hiện/yêu cầu một khoản thanh toán phụ hoặc chấp nhận khoản thanh toán phụ?',
        blank=True,
    )
    item1D = models.IntegerField(
        label='Tội lỗi?',
        choices=C.ThirdChoices,
    )
    item2D = models.IntegerField(
        label='Lo lắng?',
        choices=C.ThirdChoices,
    )
    item3D = models.IntegerField(
        label='Dễ chịu ?',
        choices=C.ThirdChoices,
    )
    itemE = models.IntegerField(
        label='Bạn có cảm xúc nào sau đây khi được đề nghị (hoặc bị đòi hỏi) một khoản thanh toán phụ?',
        blank=True,
    )
    item1E = models.IntegerField(
        label='Tức giận?',
        choices=C.ThirdChoices,
    )
    item2E = models.IntegerField(
        label='Dễ chịu?',
        choices=C.ThirdChoices,
    )
    item3E = models.IntegerField(
        label='Lo lắng?',
        choices=C.ThirdChoices,
    )
    item4E = models.IntegerField(
        label='Đồng cảm?',
        choices=C.ThirdChoices,
    )
    item5E = models.IntegerField(
        label='Thất vọng?',
        choices=C.ThirdChoices,
    )
    itemF = models.IntegerField(
        label='Bạn có cảm xúc nào sau đây khi lời đề nghị về khoản thanh toán phụ (hoặc lời yêu cầu về khoản thanh toán phụ) bị từ chối?',
        blank=True,
    )
    item1F = models.IntegerField(
        label='Tức giận?',
        choices=C.ThirdChoices,
    )
    item2F = models.IntegerField(
        label='Dễ chịu?',
        choices=C.ThirdChoices,
    )
    item3F = models.IntegerField(
        label='Thất vọng?',
        choices=C.ThirdChoices,
    )
    item4F = models.IntegerField(
        label='Đồng cảm?',
        choices=C.ThirdChoices,
    )
    item5F = models.IntegerField(
        label='Lo lắng?',
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
