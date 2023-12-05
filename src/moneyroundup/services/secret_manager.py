# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

from json import loads
from typing import Union

import boto3
from botocore.exceptions import ClientError


class SecretManager:
    @staticmethod
    def get_secret(secret_name: str) -> Union[str, dict[str, str]]:
        # Create a Secrets Manager client
        client = boto3.client("secretsmanager")

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        # Decrypts secret using the associated KMS key.
        secret = loads(get_secret_value_response["SecretString"])["secret"]

        return secret
