from datetime import datetime, timedelta
from django_cron import CronJobBase, Schedule
import pytz

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from job_handler_app.utils import enqueue_job_decorator
from user_app.models import User, UserLoginOTP, UserToken, UserTokenUsage

class DeleteInactiveUsers(CronJobBase):
    """
    Deletes users who joined but never activated their account after 7 days.
    """
    RUN_AT_TIMES = ['00:00', '12:00'] # Run twice a day, at midnight and noon
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'delete_inactive_users'

    @enqueue_job_decorator
    def do(self):
        SEVEN_DAYS_AGO: datetime = datetime.now(pytz.timezone(settings.TIME_ZONE)) - timedelta(days=7)
        _ = User.objects.filter(
            Q(is_active=False) 
            & Q(date_joined__lte=SEVEN_DAYS_AGO)
        ).delete()


class DeleteAbandonedUsers(CronJobBase):
    """
    Delete users who have not logged into their account in over 1 year and 6 months.
    """
    RUN_AT_TIMES = ['00:00', '12:00'] # Run twice a day, at midnight and noon
    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'delete_abandoned_users'

    @enqueue_job_decorator
    def do(self):
        ONE_YEAR_SIX_MONTHS_AGO: datetime = datetime.now(pytz.timezone(settings.TIME_ZONE)) - timedelta(days=548) ## (prithoo): 364.25 days times 1.5 is equal to 547.875 days
        _ = User.objects.filter(
            Q(is_active=True) 
            & Q(last_login__lte=ONE_YEAR_SIX_MONTHS_AGO)
        ).delete()


class DeleteExpiredLoginOTPs(CronJobBase):
    """
    Deletes expired Login OTPs.
    """
    RUN_EVERY_MINUTES = 5 # Run every 5 minutes
    schedule = Schedule(run_every_mins=RUN_EVERY_MINUTES)

    code = 'delete_expired_login_otps'

    @enqueue_job_decorator
    def do(self):
        NOW: datetime = timezone.now()
        _ = UserLoginOTP.objects.filter(
            otp_expires_at__lte=NOW
        ).delete()


class DeleteExpiredUserLoginTokens(CronJobBase):
    """
    Deletes expired Permanent User Tokens.
    """

    RUN_EVERY_MINUTES = 20 # Run every 20 minutes
    schedule = Schedule(run_every_mins=RUN_EVERY_MINUTES)

    code = 'delete_expired_user_logins_tokens'

    @enqueue_job_decorator
    def do(self):
        NOW: datetime = timezone.now()
        objs = UserToken.objects.filter(
            expires_at__lte=NOW
        )

        # Iterating through a generator for better memory-management in background scheduled task.
        for _, item in enumerate(objs):
            item.delete()




class DeleteOldUserTokenUsage(CronJobBase):
    """
    Deletes records of users' permanent token usage from 1 year ago.
    """
    RUN_MONTHLY_ON_DAYS = [1, 15, 25]
    schedule = Schedule(run_monthly_on_days=RUN_MONTHLY_ON_DAYS)

    code = 'delete_old_permanent_token_usage_logs'

    @enqueue_job_decorator
    def do(self):
        ONE_YEAR_AGO: datetime = timezone.now() - timedelta(days=365)
        objs = UserTokenUsage.objects.filter(
            created__lte = ONE_YEAR_AGO
        )

        # Iterating through a generator for better memory-management in background scheduled task.
        for _, item in enumerate(objs):
            item.delete()