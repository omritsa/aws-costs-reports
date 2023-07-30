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

AWS Costs Reports offers a comprehensive tool to give engineers and other stakeholders a clear visibility into AWS costs. With a strong emphasis on fostering a culture of FinOps, this tool aggregates, processes, and reports AWS costs in an efficient manner, sending relevant insights via Slack notifications.

## Features:

1. **Configurable Reports**: Personalize cost reports per user or Slack channel. 
2. **Detailed Insights**: Aggregate daily and monthly costs, providing both recent and historical perspectives.
3. **Slack Integration**: Seamlessly send cost insights directly to users or specific Slack channels.
4. **DynamoDB-backed**: Uses DynamoDB to manage configurations, offering scalability and reliability.

## Output:

When executed, the script offers a rich and detailed command line interface:

```
python3 lambda_handler.py 
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
Summary: 2 reports were sent.
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

1. Update the `AWS_REGION` variable to your primary AWS region.
2. Set the `DYNAMO_TABLE_NAME` variable to your DynamoDB table name.
3. Execute the main script using `python3 lambda_handler.py`.

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

