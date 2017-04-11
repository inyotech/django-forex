from django.db import models

class Story(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.CharField(max_length=255)
    feed_url = models.CharField(max_length=255)
    published_date = models.DateTimeField()
    created_date = models.DateTimeField()

    class Meta:

        db_table = 'stories'

    def __str__(self):

        return "{0.id}, {0.title}".format(self)

