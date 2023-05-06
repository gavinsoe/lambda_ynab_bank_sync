import boto3
from botocore.config import Config

ssm_client = boto3.client("ssm")
config = Config(retries={"max_attempts": 10, "mode": "adaptive"})


def get_parameter(key, decrypt=True):
    parameter = ssm_client.get_parameter(Name=key, WithDecryption=decrypt)

    return parameter["Parameter"]["Value"]


def get_parameters_in_path(path, decrypt=True):
    ssm_parameters = ssm_client.get_parameters_by_path(
        Path=path, WithDecryption=decrypt, Recursive=True
    )

    parameters = {}

    for p in ssm_parameters["Parameters"]:
        parameters[p["Name"]] = p["Value"]

    return parameters
