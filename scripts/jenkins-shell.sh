#!/bin/bash
WORKING_DIR=${WORKSPACE}
CLUSTER_NAME="BAH-Demo"
SERVICE_NAME="php-demo-svc-cli"
IMAGE_VERSION="v_"${BUILD_NUMBER}
TASK_FAMILY="php-sample-app"

# Create a new task definition for this build
cd ${WORKING_DIR}
docker push srikanna/ecs-demo:v_${BUILD_NUMBER}
sed -e "s;%BUILD_NUMBER%;${BUILD_NUMBER};g" task-def.json > task-def-v_${BUILD_NUMBER}.json
aws ecs register-task-definition --family php-sample-app --cli-input-json file://task-def-v_${BUILD_NUMBER}.json

# Update the service with the new task definition and desired count
TASK_REVISION=`aws ecs describe-task-definition --task-definition php-sample-app | egrep "revision" | tr "/" " " | awk '{print $2}' | sed 's/"$//'`
DESIRED_COUNT=`aws ecs describe-services --cluster ${CLUSTER_NAME} --services ${SERVICE_NAME} --query 'services[0].[desiredCount]' --output text`
if [ ${DESIRED_COUNT} = "0" ]; then
    DESIRED_COUNT="2"
fi

aws ecs update-service --cluster ${CLUSTER_NAME} --service ${SERVICE_NAME} --task-definition ${TASK_FAMILY}:${TASK_REVISION} --desired-count ${DESIRED_COUNT}