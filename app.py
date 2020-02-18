#!/usr/bin/env python3

from aws_cdk import core

from cdk_example_ingest.cdk_example_ingest_stack import CdkExampleIngestStack


app = core.App()
CdkExampleIngestStack(app, "cdk-example-ingest")

app.synth()
