import os
from os import environ

import dj_database_url

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

# SENTRY_DSN = 'http://01b52db0653d4c80bbfea86a65add259:0cfd52b438064c0e89de041f8c37640c@sentry.otree.org/327'

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# don't share this with anybody.
SECRET_KEY = '#b91$%p5slstq=-(q^prtv--!b-ohq$(7rey)jjis6mq9ameli'

DATABASES = {
    'default': dj_database_url.config(
        # Rather than hardcoding the DB parameters here,
        # it's recommended to set the DATABASE_URL environment variable.
        # This will allow you to use SQLite locally, and postgres/mysql
        # on the server
        # Examples:
        # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
        # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME

        # fall back to SQLite if the DATABASE_URL env var is missing
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# If you are launching a study and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to STUDY.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2

# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_HTML = """
<b>Control</b>: 5 all. <br>
<b>Treatment</b>: 2 out of 5, biased. <br>
<b>Control_new</b>: 2 out of 5, random. <br>
<b>Treatment_new</b>: 2 out of 5, biased mechanism revealed. <br>
"""

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24,  # 7 days
    # 'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    # to use qualification requirements, you need to uncomment the 'qualification' import
    # at the top of this file.
    'qualification_requirements': [],
}

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.005,
    'participation_fee': 5.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}


SESSION_CONFIGS = [
    # {
    #     'name': 'Li_survey',
    #     'display_name': 'A simple survey',
    #     'num_demo_participants': 3,
    #     'app_sequence': ['Li_survey'],
    #
    # },
    # {
    #     'name': 'my_public_goods',
    #     'display_name': 'A simple public goods game',
    #     'num_demo_participants': 3,
    #     'app_sequence': ['my_public_goods'],
    #
    # },
    # {
    #     'name': 'my_trust',
    #     'display_name': "simple trust Game",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['my_trust'],
    # },
    # {
    #     'name': 'polls',
    #     'display_name': "simple poll",
    #     'num_demo_participants': 5,
    #     'app_sequence': ['polls'],
    #     'real_world_currency_per_point': 0.01
    # },
    {
        'name': 'polls_control',
        'display_name': "Control",
        'num_demo_participants': 15,
        'app_sequence': ['polls_control'],
        'real_world_currency_per_point': 0.005
    },
    {
        'name': 'polls_treatment',
        'display_name': "Treatment",
        'num_demo_participants': 15,
        'app_sequence': ['polls_treatment'],
        'real_world_currency_per_point': 0.005
    },
    {
        'name': 'poll_control_new',
        'display_name': "Control_new",
        'num_demo_participants': 15,
        'app_sequence': ['poll_control_new'],
        'real_world_currency_per_point': 0.005,

    },
    {
        'name': 'polls_treatment_new',
        'display_name': "Treatment_new",
        'num_demo_participants': 15,
        'app_sequence': ['poll_control_new'],
        'real_world_currency_per_point': 0.005,

    },
]


# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
SENTRY_DSN = 'http://01b52db0653d4c80bbfea86a65add259:0cfd52b438064c0e89de041f8c37640c@sentry.otree.org/327'