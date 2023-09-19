import json

import pytest
import localstack_client.session as boto3


class TestLambda:
    iam_client = boto3.client("iam")
    lambda_client = boto3.client("lambda")
    lambda_role_name = "LambdaBasicExecution"

    def test_lambda(self) -> None:
        with open("tests/snapshots/aws/lambda/handler.zip", "rb") as f:
            zipped_code = f.read()

        role = self.iam_client.get_role(RoleName="LambdaBasicExecution")

        # Create lambda func
        response = self.lambda_client.create_function(
            FunctionName="helloWorldLambda",
            Runtime="python3.9",
            Role=role["Role"]["Arn"],
            Handler="handler.lambda_handler",
            Code=dict(ZipFile=zipped_code),
            Timeout=300,  # Maximum allowable timeout
        )

        # Invoke lambda func
        response = self.lambda_client.invoke(
            FunctionName="helloWorldLambda",
            Payload=json.dumps({}),
        )

        res = response["Payload"].read().decode("utf-8")
        assert "Hello World from Lambda" in res

        # Delete lambda func
        response = self.lambda_client.delete_function(FunctionName="helloWorldLambda")

    @classmethod
    @pytest.fixture(autouse=True)
    def setup_class(cls, snapshot_factory):
        role_policy = snapshot_factory("aws/lambda/role_policy.json")

        cls.iam_client.create_role(
            RoleName=cls.lambda_role_name,
            AssumeRolePolicyDocument=json.dumps(role_policy),
        )

    @classmethod
    def teardown_class(cls):
        cls.iam_client.delete_role(RoleName=cls.lambda_role_name)
