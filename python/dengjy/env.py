# -*- coding: utf-8 -*-

USER_ACCOUNTS = [
    {
        'key': 'jiyuan12354',
        'user_name': 'jiyuan12354',
        'password': '',
        'type': ''
    }
]

QUERY_INTERVAL = 1

USER_HEARTBEAT_INTERVAL = 120

QUERY_JOB_THREAD_ENABLED = 0

AUTO_CODE_PLATFORM = 'free'
API_USER_CODE_QCR_API = ''
AUTO_CODE_ACCOUNT = {
    'user': 'your user name',
    'pwd': 'your password'
}

NOTIFICATION_BY_VOICE_CODE = 1
NOTIFICATION_VOICE_CODE_TYPE = 'dingxin'
NOTIFICATION_API_APP_CODE = 'your app code'
NOTIFICATION_VOICE_CODE_PHONE = 'your phone'

DINGTALK_ENABLED = 0
DINGTALK_WEBHOOK = 'https://oapi.dingtalk.com/robot/send?access_token=your token'

TELEGRAM_ENABLED = 0
TELEGRAM_BOT_API_URL = 'https://tgbot.lbyczf.com/sendMessage/:your_token'

SERVERCHAN_ENABLED = 0
SERVERCHAN_KEY = ''
PUSHBEAR_ENABLED = 0
PUSHBEAR_KEY = ''

BARK_ENABLED = 0
BARK_PUSH_URL = 'https://api.day.app/:your_token'

OUT_PUT_LOG_TO_FILE_ENABLED = 0
OUT_PUT_LOG_TO_FILE_PATH = 'runtime/12306.log'

CLUSTER_ENABLED = 0
NODE_IS_MASTER = 1
NODE_SLAVE_CAN_BE_MASTER = 1
NODE_NAME = 'master'
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_PASSWORD = ''

EMAIL_ENABLED = 0
EMAIL_SENDER = 'sender@example.com'
EMAIL_RECEIVER = '1941334799@qq.com'
EMAIL_SERVER_HOST = 'localhost'
EMAIL_SERVER_USER = ''
EMAIL_SERVER_PASSWORD = ''

WEB_ENABLE = 1
WEB_USER = {
    'username': 'admin',
    'password': 'password'
}
WEB_PORT = 8008

CDN_ENABLED = 0
CDN_CHECK_TIME_OUT = 1

CACHE_RAIL_ID_ENABLED = 0
RAIL_EXPIRATION = ''
RAIL_DEVICEID = ''

QUERY_JOBS = [
    {
        'account_key': 0,
        'left_dates': [
            "2022-01-22",
            "2022-01-23",
            "2022-01-24",
        ],
        'stations': {
            'left': '深圳',
            'arrive': '隆回',
        },
        'members': [
            "邓建源",
            "陈阿梅",
            "戴青凤",
            "邓星叶",
        ],
        'allow_less_member': 0,
        'seats': [
            '二等座'
        ],
        'train_numbers': [
        ],
        'except_train_numbers': [
        ],
        'period': {
            'from': '00:00',
            'to': '24:00'
        }

    }
]
