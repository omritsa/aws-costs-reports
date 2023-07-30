from aws_operations import get_dynamodb_configs, get_cost_and_usage_for_days, get_cost_and_usage_for_months
from slack_utils import format_slack_message, format_monthly_slack_message, post_to_slack
from utils import calculate_dates, fetch_costs, aggregate_daily_costs, aggregate_monthly_costs
from decimal import Decimal
import boto3
import os

print('''                                                 
 .---.-.--.--.--.-----.                       
 |  _  |  |  |  |__ --|                       
 |___._|________|_____|                       
                   __                         
 .----.-----.-----|  |_.-----.                
 |  __|  _  |__ --|   _|__ --|                
 |____|_____|_____|____|_____|
                              __              
 .----.-----.-----.-----.----|  |_.-----.----.
 |   _|  -__|  _  |  _  |   _|   _|  -__|   _|
 |__| |_____|   __|_____|__| |____|_____|__|  
            |__|                              
                                              
''')

AWS_REGION = 'us-east-1' # Update this to your Primary AWS region
DYNAMO_TABLE_NAME = 'CostReports-TEST' # Update this to your DynamoDB table name created in "create_dynamodb_table.py

def lambda_handler(event, context):
    configs = get_dynamodb_configs(DYNAMO_TABLE_NAME)
    report_count = 0

    for config_item in configs:
        if not config_item.get('is_active', True):
            continue

        report_count += 1 
        print(f"Report #{report_count}")
        print(f"Report Owner: {config_item['owner']}")
        print(f"Report Name: {config_item['name']}")
        print(f"Report Description: {config_item['desc']}")
        print(f"Slack Webhook URL: {config_item['slack_webhook_url']}")
        print("-------------------------------------------------")

        SLACK_WEBHOOK = config_item['slack_webhook_url']
        cost_explorer = boto3.client('ce', region_name=AWS_REGION)

        today, yesterday, week_ago, six_months_ago, last_month_start, last_month_end = calculate_dates()

        costs_data = fetch_costs(cost_explorer, config_item, yesterday, today, week_ago, six_months_ago, last_month_start, last_month_end)

        cost_history, costs_yesterday = aggregate_daily_costs(costs_data['weekly'], costs_data['daily'])

        cost_history_six_months, costs_last_month_aggregated = aggregate_monthly_costs(costs_data['six_monthly_sparks'], costs_data['monthly'])

        slack_message = format_slack_message(costs_yesterday, cost_history)
        post_to_slack([slack_message], SLACK_WEBHOOK)

        slack_messages_monthly = format_monthly_slack_message(costs_last_month_aggregated, cost_history_six_months, last_month_end)
        post_to_slack(slack_messages_monthly, SLACK_WEBHOOK)

    print(f"Summary: {report_count} reports were sent.")
    print("-------------------------------------------------")

if __name__ == "__main__":
    lambda_handler(None, None)
