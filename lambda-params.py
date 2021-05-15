import json
import boto3
import os
from datetime import datetime
from urllib.parse import urlparse

template_url = "https://yourlink.s3.amazonaws.com/s3template.json"

def launch_stack():
  cfn = boto3.client('cloudformation')
  current_ts = datetime.now().isoformat().split('.')[0].replace(':','-')
  stackname = 'stack-test-from-lambda-s3' + current_ts
  capabilities = ['CAPABILITY_IAM', 'CAPABILITY_AUTO_EXPAND']
  try:
    stackdata = cfn.create_stack(
      StackName=stackname,
      DisableRollback=True,
      TemplateURL=template_url,ud
      Capabilities=capabilities)
  except Exception as e:
    print(str(e))
  return stackdata  

def lambda_handler(event, context):
  print("Received event:")
  stack_result=launch_stack()
  print(stack_result)