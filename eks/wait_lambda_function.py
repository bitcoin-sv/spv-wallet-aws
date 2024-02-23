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
    if event['RequestType'] == 'Delete':
        props = event['ResourceProperties']
        cluster_name= props['cluster_name']
        role_arn= props['role_arn']
        os.system(f"/opt/awscli/aws eks update-kubeconfig --name {cluster_name} --kubeconfig='/tmp/kubeconfig' --role-arn='{role_arn}'")
        os.system("export PATH=$PATH:/opt/awscli/; /opt/helm/helm --kubeconfig='/tmp/kubeconfig' uninstall bux")
        print('wait started')
        time.sleep(40)
        print('wait completed')
        response['output'] = ' Delete event.'
    send(event, context, "SUCCESS", response)

