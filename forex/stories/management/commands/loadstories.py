import datetime
import time
import pprint

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from stories.models import Story

import stories.story_downloader as story_downloader

class Command(BaseCommand):
    help = 'Downloads financial stories from rss feeds'

    def add_arguments(self, parser):
        parser.add_argument('-e', '--expire-days', default=3, type=int)


    def handle(self, *args, **options):

        downloader = story_downloader.Downloader()

        now = datetime.datetime.now(tz=datetime.timezone.utc)

        keep_threshold = now - datetime.timedelta(days=options['expire_days'])

        with transaction.atomic():

            for story in downloader.iterate_stories():

                published_at = datetime.datetime.fromtimestamp(time.mktime(story.published_parsed), datetime.timezone.utc)
                s, created = Story.objects.get_or_create(
                    title=story.title,
                    link=story.link,
                    feed_url=story.feed_url,
                    defaults={
                        'description': story.summary,
                        'published_date': published_at,
                        'created_date': now,
                    });

                if created:
                    print('saved story %s' % (story.title,))
                else:
                    print('story %s exists' % (story.title,))

            Story.objects.filter(created_date__lt=keep_threshold).delete()
