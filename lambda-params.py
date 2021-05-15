import json
import boto3
import os
from datetime import datetime
from urllib.parse import urlparse

params_url = "s3://parameterscloudformation/demo-params.json"
template_url = "https://parameterscloudformation.s3.amazonaws.com/cloudformationtest.json"

def parse_params():
  s3 = boto3.resource('s3')
  s3_parse = urlparse(params_url)
  bucket = s3_parse.netloc
  s3_key = s3_parse.path.lstrip('/')
  s3_obj = s3.Object(bucket, s3_key)
  template_raw_data = s3_obj.get()["Body"].read().decode('utf-8')
  template_params = json.loads(template_raw_data)
  return template_params

def launch_stack():
  cfn = boto3.client('cloudformation')
  current_ts = datetime.now().isoformat().split('.')[0].replace(':','-')
  stackname = 'stack-test-from-lambda' + current_ts
  capabilities = ['CAPABILITY_IAM', 'CAPABILITY_AUTO_EXPAND']
  try:
    template_params = parse_params()
    stackdata = cfn.create_stack(
      StackName=stackname,
      DisableRollback=True,
      TemplateURL=template_url,
      Parameters=template_params,
      Capabilities=capabilities)
  except Exception as e:
    print(str(e))
  return stackdata

def lambda_handler(event, context):
  print("Received event:")
  stack_result=launch_stack()
  print(stack_result)
