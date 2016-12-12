from __future__ import print_function


import json
import urllib
import boto3

def lambda_handler(event, context):

    # dump the raw event for log purposes, this is logged in Cloudwatch logs
    print("----------------------")
    print("Received event: " + json.dumps(event, indent=5))
    print("----------------------")