drop view if exists exchange_rate_ratios;

create view if not exists exchange_rate_ratios as

with rate_ratios as (
select
    target_rate.currency_id target_currency_id,
    base_rate.currency_id base_currency_id,
    target_rate.rate_date rate_ratio_date,
    target_rate.per_dollar/base_rate.per_dollar rate_ratio
from exchange_rates base_rate
join exchange_rates target_rate on target_rate.rate_date = base_rate.rate_date
)

select * from rate_ratios;
