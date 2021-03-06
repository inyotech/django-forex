from django.db import models

class Currency(models.Model):

    currency_id = models.AutoField(primary_key=True)
    h10_id = models.CharField(max_length=25, unique=True)
    country_name = models.CharField(max_length=25)
    short_name = models.CharField(max_length=10)
    flag_image_file_name = models.CharField(max_length=64)
    currency_name = models.CharField(max_length=20)
    currency_code = models.CharField(max_length=3)

    class Meta:

        db_table = 'currencies'

    def __str__(self):

        return "{0.h10_id} {0.short_name} {0.currency_name} ({0.currency_code})".format(self)

class Rate(models.Model):

    rate_id = models.AutoField(primary_key=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate_date = models.DateField()
    per_dollar = models.FloatField()

    class Meta:

        db_table = 'exchange_rates'
        unique_together = (('currency', 'rate_date'))

    def __str__(self):

        return "{0.currency_id} {0.rate_date} {0.per_dollar}".format(self)


class RateRatio(models.Model):

    target_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, related_name='+')
    base_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, related_name='+')
    rate_ratio_date = models.DateField(primary_key=True)
    rate_ratio = models.FloatField()

    class Meta:
        db_table = 'exchange_rate_ratios'
        unique_together = (('target_currency', 'base_currency', 'rate_ratio_date'))
        managed = False

    def __str__(self):
        return "{0.base_currency.currency_code} {0.target_currency.currency_code} {0.rate_ratio_date} {0.rate_ratio}".format(self)
