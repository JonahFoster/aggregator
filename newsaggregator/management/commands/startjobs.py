from django.core.management.base import BaseCommand

import feedparser
from dateutil import parser

from newsaggregator.models import Post

class Command(BaseCommand):
    def handle(self, *args, **options):
        feed = feedparser.parse("https://realpython.com/podcasts/rpp/feed")
        post_title = feed.channel.title
        post_image = feed.channel.image["href"]

        for item in feed.entries:
            if not Post.objects.filter(guid=item.guid).exists():
                post = Post(
                    title=item.title,
                    description=item.description,
                    pub_date=parser.parse(item.published),
                    link=item.link,
                    image=post_image,
                    website_name=post_title,
                    guid=item.guid,
                )
                post.save()
        print("Done")