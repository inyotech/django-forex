import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'forex'))

import csv
import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forex.settings")

import django
from django.db import transaction

django.setup()

from stories.models import Story

import story_downloader as downloader

downloader = downloader.Downloader()

downloader.retreive_stories()

with transaction.atomic():

    for story in downloader.iterate_stories():

        pprint.pprint(story)
