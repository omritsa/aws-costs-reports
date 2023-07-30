from datetime import datetime, timedelta
from typing import List
import requests
import json

sparks = ['▁', '▂', '▃', '▄', '▅', '▆', '▇']

def sparkline(datapoints):
    if not datapoints:
        return ""

    lower = min(datapoints)
    upper = max(datapoints)
    n_sparks = len(sparks) - 1
    line = ""

    for dp in datapoints:
        scaled = (dp - lower) / (upper - lower) if (upper - lower) != 0 else 0
        scaled = max(0, min(scaled, 1))  # Clamp the scaled value between 0 and 1
        which_spark = round(scaled * n_sparks)
        line += (sparks[which_spark])

    return line


def format_slack_message(costs, cost_history):
    sorted_costs = sorted(costs.items(), key=lambda x: x[1], reverse=True)
    message_text = "```AWS cost report for yesterday:\n\n"
    message_text += "Data                                               Last 7d      $Yesterday\n"
    total_cost = 0

    for service, cost in sorted_costs:
        history = cost_history.get(service, [])
        sparkline_str = sparkline(history)
        message_text += f"{service:50} {sparkline_str:12} ${cost:,.2f}\n"
        total_cost += cost

    message_text += f"\nTotal: ${total_cost:,.2f}\n"
    message_text += "```"

    slack_message = {
        'text': message_text
    }

    return slack_message

def format_monthly_slack_message(last_month_costs: dict, costs_six_months_sparks: dict, last_month_end: datetime.date) -> List[dict]:
    last_month_start_date = last_month_end.replace(day=1) - timedelta(days=1)
    header = f"AWS cost report for {last_month_start_date.strftime('%B %Y')} (Previous month):\n\n"
    subheader = "Data                                               Last 6mo     $Last Month"
    total_cost = 0
    
    sorted_month_costs = sorted(last_month_costs.items(), key=lambda x: x[1], reverse=True)

    message_text = ""
    for service, cost in sorted_month_costs:
        sparkline_str = sparkline(costs_six_months_sparks.get(service, []))
        message_text += f"{service:50} {sparkline_str:12} ${cost:,.2f}\n"
        total_cost += cost

    message_text += f"\nTotal: ${total_cost:,.2f}\n"

    slack_messages = [{'text': f"```{header}{subheader}\n{message_text}```"}]
    return slack_messages

def post_to_slack(slack_messages, webhook_url):
    for slack_message in slack_messages:
        response = requests.post(
            webhook_url,
            data=json.dumps(slack_message),
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            raise ValueError(
                f'Request to Slack returned an error {response.status_code}, the response is:\n{response.text}'
            )

