import json

import boto3

from boto3_fixtures import utils
from boto3_fixtures.contrib import sqs


def check_kinesis_fixtures(kinesis_streams):
    client = boto3.client("kinesis")
    for ks in kinesis_streams:
        client.put_record(
            StreamName=ks, Data=json.dumps({"foo": "bar"}), PartitionKey="foobar"
        )


def check_sqs_fixtures(sqs_queues):
    client = boto3.client("sqs")
    for q in sqs_queues:
        queue_url = sqs.get_queue_url(q)
        utils.call(
            client.send_message,
            QueueUrl=queue_url,
            MessageBody=json.dumps({"foo": "bar"}),
        )


def check_dynamodb_fixtures(dynamodb_tables):
    client = boto3.client("dynamodb")
    resp = utils.call(utils.backoff_check, func=lambda: client.list_tables())
    for table in dynamodb_tables:
        assert table in resp["TableNames"]


def check_s3_fixtures(s3_buckets):
    client = boto3.client("s3")
    resp = utils.call(utils.backoff_check, func=lambda: client.list_buckets())
    bucket_names = {b["Name"]: b for b in resp["Buckets"]}
    for b in s3_buckets:
        assert b in bucket_names


def check_lambda_fixtures(lambda_functions):
    client = boto3.client("lambda")
    resp = utils.call(utils.backoff_check, func=lambda: client.list_functions())
    lambda_names = {lam["FunctionName"]: lam for lam in resp["Functions"]}
    for lam in lambda_functions:
        assert lam["FunctionName"] in lambda_names


def check_sns_fixtures(sns_topics):
    client = boto3.client("sns")
    resp = utils.call(utils.backoff_check, func=lambda: client.list_topics())
    topic_names = [tpc["TopicArn"].rsplit(":", 1)[-1] for tpc in resp["Topics"]]
    assert set(topic_names) == set(sns_topics)
