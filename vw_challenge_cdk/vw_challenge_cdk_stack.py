from constructs import Construct
from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_events as events,
    aws_events_targets as targets,
    RemovalPolicy,
    Duration
)


class VwChallengeCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.TableV2(self, "Table",
                                 partition_key=dynamodb.Attribute(
                                     name="id", type=dynamodb.AttributeType.STRING)
                                 )

        fn = lambda_.Function(self, "InsertDataFunction",
                              handler="lambda_handler.handler",
                              runtime=lambda_.Runtime.PYTHON_3_13,
                              code=lambda_.Code.from_asset(
                                  "vw_challenge_cdk/lambda"),
                              environment={"TABLE_NAME": table.table_name}
                              )
        table.grant_write_data(fn)
        endpoint = apigw.LambdaRestApi(
            self,
            "ApiGwEndpoint",
            handler=fn,
            rest_api_name="ChallengeApi"
        )

        items = endpoint.root.add_resource("items")
        items.add_method("POST")

        bucket = s3.Bucket(self, "ChallengeSummary",
                           removal_policy=RemovalPolicy.DESTROY)

        summary_lambda = lambda_.Function(self, "SummaryFunction",
                                          handler="summary_lambda.handler",
                                          runtime=lambda_.Runtime.PYTHON_3_13,
                                          code=lambda_.Code.from_asset(
                                              "vw_challenge_cdk/lambda"),
                                          environment={
                                              "TABLE_NAME": table.table_name,
                                              "BUCKET_NAME": bucket.bucket_name}
                                          )

        table.grant_read_data(summary_lambda)
        bucket.grant_write(summary_lambda)

        rule = events.Rule(
            self, "WeeklySummaryRule",
            schedule=events.Schedule.rate(Duration.days(7))
        )
        rule.add_target(targets.LambdaFunction(summary_lambda))
