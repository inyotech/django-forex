import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'forex'))

import time
import datetime
import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forex.settings")

import django
from django.db import transaction, connection

django.setup()

from stories.models import Story

import story_downloader as downloader

downloader = downloader.Downloader()

now = datetime.datetime.now(tz=datetime.timezone.utc)

keep_threshold = now - datetime.timedelta(days=3)

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


pprint.pprint(connection.queries)
