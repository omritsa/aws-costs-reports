from aws_operations import get_dynamodb_configs, get_cost_and_usage_for_days, get_cost_and_usage_for_months
from datetime import datetime, timedelta


def calculate_dates():
    now = datetime.utcnow()
    today = now.date()
    yesterday = (now - timedelta(days=1)).date()
    week_ago = yesterday - timedelta(days=7)
    six_months_ago = (now - timedelta(days=6*30)).date()
    last_month_end = today.replace(day=1)
    last_month_start = (last_month_end - timedelta(days=1)).replace(day=1)

    return today, yesterday, week_ago, six_months_ago, last_month_start, last_month_end

def fetch_costs(cost_explorer, config_item, yesterday, today, week_ago, six_months_ago, last_month_start, last_month_end):
    return {
        'daily': get_cost_and_usage_for_days(cost_explorer, yesterday, today, config_item),
        'weekly': get_cost_and_usage_for_days(cost_explorer, week_ago, today, config_item),
        'six_monthly': get_cost_and_usage_for_days(cost_explorer, six_months_ago, today, config_item, granularity='MONTHLY'),
        'monthly': get_cost_and_usage_for_days(cost_explorer, last_month_start, last_month_end, config_item),
        'six_monthly_sparks': get_cost_and_usage_for_days(cost_explorer, six_months_ago, last_month_end, config_item, granularity='MONTHLY')
    }

def aggregate_daily_costs(costs_week, costs):
    cost_history = {}
    for day_data in costs_week:
        for group in day_data['groups']:
            service, cost = group['service'], group['cost']
            cost_history.setdefault(service, []).append(cost)

    costs_yesterday = {}
    for item in costs:
        for group in item['groups']:
            service, cost = group['service'], group['cost']
            costs_yesterday[service] = costs_yesterday.get(service, 0) + cost

    return cost_history, costs_yesterday

def aggregate_monthly_costs(costs_six_months_sparks, costs_last_month):
    cost_history_six_months = {}
    for month_data in costs_six_months_sparks:
        for group in month_data['groups']:
            service, cost = group['service'], group['cost']
            cost_history_six_months.setdefault(service, []).append(cost)

    costs_last_month_aggregated = {}
    for item in costs_last_month:
        for group in item['groups']:
            service, cost = group['service'], group['cost']
            costs_last_month_aggregated[service] = costs_last_month_aggregated.get(service, 0) + cost

    return cost_history_six_months, costs_last_month_aggregated

