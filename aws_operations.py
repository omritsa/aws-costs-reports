from datetime import datetime, timedelta
from decimal import Decimal
import boto3

AWS_REGION = 'us-east-1' # Adjust as necessary
DYNAMO_TABLE_NAME = 'CostReports-TEST' # Adjust as necessary

def get_dynamodb_configs(table_name):
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table(table_name)
    response = table.scan()
    items = response.get('Items', [])
    return items

def get_cost_and_usage_for_days(cost_explorer, start_date, end_date, config_item, granularity='DAILY'):
    metrics = [config_item['cost_aggregation_by']]
    
    filter_values = []
    if config_item.get('exclude_credits', False):
        filter_values.append("Credit")
    if config_item.get('exclude_taxes', False):
        filter_values.append("Tax")

    response = cost_explorer.get_cost_and_usage(
        TimePeriod={
            'Start': str(start_date),
            'End': str(end_date)
        },
        Granularity=granularity,
        Metrics=metrics,
        Filter={
            "Not": {
                "Dimensions": {
                    "Key": "RECORD_TYPE",
                    "Values": filter_values
                }
            }
        } if filter_values else {},
        GroupBy=[{'Type': 'DIMENSION', 'Key': config_item['group_by']}]
    )

    results = response['ResultsByTime']
    costs = [
        {'date': day_data['TimePeriod']['Start'], 'groups': [
        {'service': group['Keys'][0], 'cost': Decimal(group['Metrics'][config_item['cost_aggregation_by']]['Amount'])}
            for group in day_data['Groups']
        ]}
        for day_data in results
    ]

    return costs

def get_cost_and_usage_for_months(cost_explorer, start_date, end_date, config_item, granularity='MONTHLY'):
    """Retrieve cost and usage details from AWS Cost Explorer for a specified date range."""
    response = cost_explorer.get_cost_and_usage(
        TimePeriod={
            'Start': str(start_date),
            'End': str(end_date)
        },
        Granularity=granularity,
        Metrics=[config_item['cost_aggregation_by']],
        Filter={
            "Not": {
                "Dimensions": {
                    "Key": "RECORD_TYPE",
                    "Values": ["Credit", "Tax"]
                }
            }
        },
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    months_data = []

    for month in response['ResultsByTime']:
        month_costs = []
        for group in month['Groups']:
            service = group['Keys'][0]
            cost = float(group['Metrics'][config_item['cost_aggregation_by']]['Amount'])
            month_costs.append({'service': service, 'cost': cost})
        months_data.append({'date': month['TimePeriod']['Start'], 'groups': month_costs})

    return months_data
