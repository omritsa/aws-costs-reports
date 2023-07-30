import boto3
import re

def create_dynamodb_table():
    dynamodb = boto3.resource('dynamodb')
    name_pattern = r'^[a-zA-Z0-9._-]{3,255}$'

    while True:
        table_name = input("Enter the DynamoDB table name: ")

        # Validate the table name according to the rules
        if not re.match(name_pattern, table_name):
            print("Invalid table name. Table name should be between 3 and 255 characters, containing only letters, numbers, underscores (_), hyphens (-), and periods (.)")
        else:
            try:
                table = dynamodb.create_table(
                    TableName=table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'id',
                            'KeyType': 'HASH'  # Primary key
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id',
                            'AttributeType': 'N'
                        }
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1
                    }
                )

                # Wait until the table exists, this might take a minute or so.
                table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

                print(f"Table {table_name} created successfully.")
                return table

            except dynamodb.meta.client.exceptions.ResourceInUseException:
                print(f"Table {table_name} already exists.")
                return dynamodb.Table(table_name)

if __name__ == '__main__':
    table = create_dynamodb_table()
