class JobQ:
    WEB_Q = "web"
    EMAIL_Q = "email"
    SMS_Q = "sms"
    NOTIFICATION_Q = "notification"
    DEFAULT_Q = "default"
    STATS_Q = "stats"

    DEFAULT_QS = [WEB_Q, EMAIL_Q, SMS_Q, NOTIFICATION_Q, DEFAULT_Q, STATS_Q]
    NOTIFICATION_QS = [EMAIL_Q, SMS_Q, NOTIFICATION_Q]
    ALL_QS = [WEB_Q, EMAIL_Q, SMS_Q, NOTIFICATION_Q, DEFAULT_Q, STATS_Q]