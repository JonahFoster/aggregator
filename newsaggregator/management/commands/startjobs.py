# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# Third Party
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# Models
from newsaggregator.models import Post

# Logging
import logging

logger = logging.getLogger(__name__)

def save_new_posts(feed):
    """Saves new episodes to the database.

    Checks the episode GUID against the episodes currently stored in the
    database. If not found, then a new `Episode` is added to the database.

    Args:
        feed: requires a feedparser object
    """
    post_title = feed.channel.title
    #post_image = feed.channel.image["href"]

    for entry in feed.entries:
        #if not Post.objects.filter().exists():
            post = Post(
                title=entry.title,
                description=entry.description,
                pub_date=parser.parse(entry.published),
                link=entry.link,
                #image=post_image,
                website_name=post_title,
            )
            post.save()

def fetch_athletic_posts():
    """Fetches new posts from RSS for The Athletic"""
    _feed = feedparser.parse("https://theathletic.com/team/florida-gators-college-football/?rss=1")
    save_new_posts(_feed)

def fetch_gatorreddit_posts():
    """Fetches new posts from RSS for The Gators Subreddit"""
    _feed = feedparser.parse("https://www.reddit.com/r/floridagators/.rss")
    save_new_posts(_feed)

def delete_old_job_executions(max_age=604_800): # 1 week
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_athletic_posts,
            trigger="interval",
            seconds=10,
            # Change interval when live
            id="The Athletic",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: The Athletic")

        scheduler.add_job(
            fetch_gatorreddit_posts,
            trigger="interval",
            seconds=10,
            # Change interval when live
            id="Gators Subreddit",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job: The Athletic")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")