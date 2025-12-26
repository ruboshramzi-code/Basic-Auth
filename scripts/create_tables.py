"""
DynamoDB Table Creation Script
Run this script to create all required DynamoDB tables
"""
import boto3
import os
from config import config

dynamodb = boto3.client('dynamodb', region_name=config.AWS_REGION)

def create_users_table():
    """Create Users table"""
    try:
        dynamodb.create_table(
            TableName=config.USERS_TABLE,
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'email-index',
                    'KeySchema': [
                        {'AttributeName': 'email', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"✓ Created table: {config.USERS_TABLE}")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"⚠ Table already exists: {config.USERS_TABLE}")
    except Exception as e:
        print(f"✗ Error creating {config.USERS_TABLE}: {str(e)}")


def create_refresh_tokens_table():
    """Create RefreshTokens table"""
    try:
        dynamodb.create_table(
            TableName=config.REFRESH_TOKENS_TABLE,
            KeySchema=[
                {'AttributeName': 'token', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'token', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user_id-index',
                    'KeySchema': [
                        {'AttributeName': 'user_id', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            },
            TimeToLiveSpecification={
                'Enabled': True,
                'AttributeName': 'expires_at'
            }
        )
        print(f"✓ Created table: {config.REFRESH_TOKENS_TABLE}")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"⚠ Table already exists: {config.REFRESH_TOKENS_TABLE}")
    except Exception as e:
        print(f"✗ Error creating {config.REFRESH_TOKENS_TABLE}: {str(e)}")


def create_verification_codes_table():
    """Create VerificationCodes table"""
    try:
        dynamodb.create_table(
            TableName=config.VERIFICATION_CODES_TABLE,
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                {'AttributeName': 'code_type', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'code_type', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"✓ Created table: {config.VERIFICATION_CODES_TABLE}")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"⚠ Table already exists: {config.VERIFICATION_CODES_TABLE}")
    except Exception as e:
        print(f"✗ Error creating {config.VERIFICATION_CODES_TABLE}: {str(e)}")


def create_login_attempts_table():
    """Create LoginAttempts table"""
    try:
        dynamodb.create_table(
            TableName=config.LOGIN_ATTEMPTS_TABLE,
            KeySchema=[
                {'AttributeName': 'ip_address', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'ip_address', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'ip_address-timestamp-index',
                    'KeySchema': [
                        {'AttributeName': 'ip_address', 'KeyType': 'HASH'},
                        {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"✓ Created table: {config.LOGIN_ATTEMPTS_TABLE}")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"⚠ Table already exists: {config.LOGIN_ATTEMPTS_TABLE}")
    except Exception as e:
        print(f"✗ Error creating {config.LOGIN_ATTEMPTS_TABLE}: {str(e)}")


def create_rate_limits_table():
    """Create RateLimits table"""
    try:
        dynamodb.create_table(
            TableName=config.RATE_LIMITS_TABLE,
            KeySchema=[
                {'AttributeName': 'limit_key', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'limit_key', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        print(f"✓ Created table: {config.RATE_LIMITS_TABLE}")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"⚠ Table already exists: {config.RATE_LIMITS_TABLE}")
    except Exception as e:
        print(f"✗ Error creating {config.RATE_LIMITS_TABLE}: {str(e)}")


def create_all_tables():
    """Create all tables"""
    print(f"\n{'='*60}")
    print(f"Creating DynamoDB Tables")
    print(f"Region: {config.AWS_REGION}")
    print(f"Environment: {config.TABLE_PREFIX}")
    print(f"{'='*60}\n")
    
    create_users_table()
    create_refresh_tokens_table()
    create_verification_codes_table()
    create_login_attempts_table()
    create_rate_limits_table()
    
    print(f"\n{'='*60}")
    print("Table creation complete!")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    create_all_tables()
