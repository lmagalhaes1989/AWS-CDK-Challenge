#!/usr/bin/env python3

import aws_cdk as cdk

from vw_challenge_cdk.vw_challenge_cdk_stack import VwChallengeCdkStack


app = cdk.App()
VwChallengeCdkStack(app, "VwChallengeCdkStack")

app.synth()
