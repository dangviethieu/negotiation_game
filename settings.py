from os import environ

SESSION_CONFIGS = [
    dict(
        name='negotiation_game_en',
        display_name="Negotiation Game EN version",
        num_demo_participants=2,
        app_sequence=['attention', 'negotiation_en_game', 'survey'],
    ),
    dict(
        name='negotiation_game_en_with_info',
        display_name="Negotiation Game EN version With Info",
        num_demo_participants=2,
        app_sequence=['attention', 'negotiation_en_game_info', 'survey'],
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['language', 'address']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '9340409623470'

ROOMS = [
    dict(
        name='negotiation',
        display_name='Negotiation Game',
        participant_label_file='_rooms/negotiation.txt',
    )
]

VERSION = '0.3'
