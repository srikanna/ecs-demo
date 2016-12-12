from __future__ import print_function

import json
import urllib
import boto3
import zipfile
import gzip
import os.path

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event["CodePipeline.job"]["data"]["inputArtifacts"][0]["location"]["s3Location"]["bucketName"]
    key = urllib.unquote_plus(event["CodePipeline.job"]["data"]["inputArtifacts"][0]["location"]["s3Location"]["objectKey"])
    try:
        s3.download_file(bucket, key, '/tmp/file.zip')
        zfile = zipfile.ZipFile('/tmp/file.zip')
        zfile.extractall('/tmp')
        namelist = zfile.namelist()
        outDir = os.path.dirname(namelist[0])
        configData = open("/tmp/"+outDir+"/ecs-deploy-config.json").read()
        configJson = json.loads(configData)
        taskData = open("/tmp/"+outDir+"/task-def.json").read()
        taskJson = json.loads(taskData)
        
        regTask = ecs.register_task_definition(family=configJson["TASK_FAMILY"],containerDefinitions=taskJson["containerDefinitions"],volumes=taskJson["volumes"])
        describeSvc = ecs.describe_services(cluster=configJson["CLUSTER_NAME"],services=[configJson["SERVICE_NAME"]])
        updateSvc = ecs.update_service(cluster=configJson["CLUSTER_NAME"],service=configJson["SERVICE_NAME"],desiredCount=describeSvc["services"][0]["desiredCount"],taskDefinition=regTask["taskDefinition"]["family"]+":"+str(regTask["taskDefinition"]["revision"]))
        return response["success"]
    except Exception as e:
        print(e)
        raise e
