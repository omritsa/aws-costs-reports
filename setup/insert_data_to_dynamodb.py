import boto3
import random

def insert_data(table):
    outer_id = random.randint(0, 9999)

    data = {
        'id': outer_id,
        'owner': 'Owner Name',                                                          # Optional: The name of the report owner
        'name': 'Cost notification name',                                               # Optional: The name of the notification
        'desc': 'Cost notification description',                                        # Optional: The description of the notification
        'slack_webhook_url': 'https://hooks.slack.com/services/XXXXX/XXXXX/XXXXXX',     # Required: Add your Slack webhook URL here
        'cost_aggregation_by': 'NetAmortizedCost',                                      # Required: This can be changed to any of the options: BlendedCost, UnblendedCost, NetAmortizedCost, NetUnblendedCost, UsageQuantity
        'group_by': 'SERVICE',                                                          # Required: This can be changed to any of the options: AZ, INSTANCE_TYPE, LINKED_ACCOUNT, OPERATION, PURCHASE_TYPE, REGION, SERVICE, USAGE_TYPE, USAGE_TYPE_GROUP, RECORD_TYPE, OPERATING_SYSTEM, TENANCY, SCOPE, PLATFORM, SUBSCRIPTION_ID, LEGAL_ENTITY_NAME, DEPLOYMENT_OPTION, DATABASE_ENGINE, CACHE_ENGINE, INSTANCE_TYPE_FAMILY
        'include_yesterday_report': True,                                               # This can be changed to False if you don't want to include yesterday's report
        'include_last_6_months_report': True,                                           # This can be changed to False if you don't want to include the last 6 months report
        'exclude_taxes': True,                                                          # This can be changed to False if you want to include taxes in the report
        'exclude_credits': True,                                                        # This can be changed to False if you want to include credits in the report
        'is_active': True                                                               # This can be changed to False if you want to disable the notification for this specific report
    }
    
    table.put_item(Item=data)
    
    print(f"Inserted data into {table.name}")

if __name__ == '__main__':
    table_name = input("Enter the DynamoDB table name: ")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    insert_data(table)
