from __future__ import print_function
import urllib3
import json
import time
import os

http = urllib3.PoolManager()

def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False, reason=None):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {
        'Status' : responseStatus,
        'Reason' : reason or "See the details in CloudWatch Log Stream: {}".format(context.log_stream_name),
        'PhysicalResourceId' : physicalResourceId or context.log_stream_name,
        'StackId' : event['StackId'],
        'RequestId' : event['RequestId'],
        'LogicalResourceId' : event['LogicalResourceId'],
        'NoEcho' : noEcho,
        'Data' : responseData
    }

    json_responseBody = json.dumps(responseBody)

    print("Response body:")
    print(json_responseBody)

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:
        response = http.request('PUT', responseUrl, headers=headers, body=json_responseBody)
        print("Status code:", response.status)


    except Exception as e:

        print("send(..) failed executing http.request(..):", e)


def handler(event, context):
    response = {}
    if event['RequestType'] == 'Update' or event['RequestType'] == 'Create':
        props = event['ResourceProperties']
        cluster_name= props['cluster_name']
        nodegroup_name= props['nodegroup_name'].split('/')[1]
        os.system(f"/opt/awscli/aws eks update-nodegroup-version --cluster-name {cluster_name} --nodegroup-name {nodegroup_name}")
        response['output'] = f' Update event.'
    response['output'] = f' Event.'
    send(event, context, "SUCCESS", response)

