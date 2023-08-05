# AWS Costs Reports

``` 
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
                                              
``` 

AWS Costs Reports is a comprehensive solution that provides engineers and other stakeholders a customized visibility into the AWS costs that interest them.
Easily build a FinOps culture within your organization by delivering customized reports over Slack or Email to individuals, groups, or channels.

## Edge:
Unlimited customized cost reports for individuals, teams, departments, and interests (reports by tags).

## Features:

1. **Configurable Reports**: Personalize cost reports per user or Slack channel. 
2. **Detailed Insights**: Aggregate daily and monthly costs, providing both recent and historical perspectives.
3. **Slack Integration**: Seamlessly send cost insights directly to users or specific Slack channels.
4. **DynamoDB-backed**: Uses DynamoDB to manage configurations, offering scalability and reliability.

## Cost Report:

```
AWS cost report for June 2023 (Previous month):

Data                                               Last 6mo     $Last Month
Amazon Relational Database Service                 ▁▆▆▆▆▇       $243.49
AWS Lambda                                         ▁▂▄▅▇▇       $64.25
AmazonCloudWatch                                   ▁▂▅▅▆▇       $33.70
AWS Config                                         ▁▅▅▆▆▇       $6.27
Amazon Detective                                   ▁▄▇▇▆▆       $3.32
Amazon Simple Queue Service                        ▁▃▆▆▆▇       $2.70
AWS CloudTrail                                     ▁▃▇▇▇▆       $2.65
Amazon DynamoDB                                    ▁▁▃▃▄▇       $2.57
Amazon Pinpoint                                    ▁▇▇▇▇▇       $2.00
AWS Key Management Service                         ▁▇▇▇▇▇       $2.00
AWS Secrets Manager                                ▁▇▇▇▇▇       $2.00
EC2 - Other                                        ▁▂▂▂▄▇       $1.45
CloudWatch Events                                  ▁▃▇▇▇▃       $1.31
Amazon Route 53                                    ▁▇▇▇▇▇       $1.00
Amazon Simple Storage Service                      ▁▅▆▇▇▇       $0.56
Amazon Cognito                                     ▇▂▁▁▄        $0.40
Amazon Simple Notification Service                 ▁▇▃▂▅▂       $0.09
Amazon API Gateway                                 ▃▁▁▇▂        $0.03
Amazon CloudFront                                  ▁▆▅▃▄▇       $0.01
AWS Backup                                         ▁▄▆▇▇▇       $0.00
Amazon Simple Email Service                        ▇▄▁▁▅        $0.00
AWS Glue                                           ▁▁▁▁▁▁       $0.00
Amazon Security Lake                               ▁▁▁▁▁▁       $0.00
AWS CloudShell                                     ▁            $0.00

Total: $369.81
```

## Example of a DynamoDB item:
```
{
 "id": 3314,
 "cost_aggregation_by": "UnblendedCost",
 "desc": "Send AWS costs report to a Slack channel named: #cloud-cost-notifications, Show costs as unblended, group by Service, and excl. credits & taxes. include in the report yesterday costs and the costs in the last 6 months.",
 "exclude_credits": true,
 "exclude_taxes": true,
 "group_by": "SERVICE",
 "include_last_6_months_report": true,
 "include_yesterday_report": true,
 "is_active": true,
 "name": "Service report",
 "owner": "Omri Tsabari",
 "slack_webhook_url": "https://hooks.slack.com/services/T0****/B0****/g****"
}
```

## Item config options
```
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
```

## Run Output:

When executed, the script offers a rich and detailed command line interface:

```
$ python3 lambda_handler.py 
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
                                              
Report #1
Report Owner: Omri Tsabari
Report Name: Purchase Option report
Report Description: Send AWS costs report to Omri Tsabari over Slack with amortization, group by Purchase Option, and excl. credits & taxes. include in the report yesterday costs and the costs in the last 6 months.
Slack Webhook URL: https://hooks.slack.com/services/****01HM7XERQE/C057D2SN95E/kknHWMQtmhb6kKZZUN0kgpr****
-------------------------------------------------
Report #2
Report Owner: Omri Tsabari
Report Name: Service report
Report Description: Send AWS costs report to a Slack channel named: #cloud-cost-notifications
Show costs as unblended, group by Service, and excl. credits & taxes. 
include in the report yesterday costs and the costs in the last 6 months.
Slack Webhook URL: https://hooks.slack.com/services/****01HM7XERQE/C057D2SN95E/kknHWMQtmhb6kKZZUN0kgpr****
-------------------------------------------------
Summary: 2 reports were sent to Slack.
-------------------------------------------------
```

## Directory Structure:

```
.
├── LICENSE
├── aws_operations.py
├── lambda_handler.py
├── slack_utils.py
└── utils.py
├── setup
│   ├── create_dynamodb_table.py
│   └── insert_data_to_dynamodb.py
```

## Getting Started:

1. Create the dynamodb table using `python3 create_dynamodb_table.py`.
2. Insert an item into the dynamodb table and duplicate it as many as you need `python3 insert_data_to_dynamodb.py`.
3. Create a new slack app over https://api.slack.com/apps and configure webhooks per individuals and/or channels as desired.
4. Update the `AWS_REGION` variable to your primary AWS region.
5. Set the `DYNAMO_TABLE_NAME` variable to your DynamoDB table name.
6. Execute the main script using `python3 lambda_handler.py`.

## Dependencies:

- boto3
- AWS SDK
- AWS Credentials
- Python 3.x

Ensure you have the required permissions to access and manipulate AWS services, especially Cost Explorer and DynamoDB.

## Contribute:

Feel free to fork, raise issues, or submit PRs. For major changes, please open an issue first to discuss what you'd like to change.

## License:

This project is licensed under the terms of the included LICENSE file.

