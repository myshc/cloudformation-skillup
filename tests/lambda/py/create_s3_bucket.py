import boto3, os, time


AWS_DEFAULT_REGION = 'eu-central-1'
os.environ['AWS_DEFAULT_REGION'] = AWS_DEFAULT_REGION

bucketname = 'lambda.created.me.on-' + str(time.time())


def lambda_handler(event, context):
  s3 = boto3.resource('s3') 
  try:
    return s3.create_bucket(
      Bucket=bucketname,
      CreateBucketConfiguration={'LocationConstraint': AWS_DEFAULT_REGION}
    )
  except Exception as ex:
    return ex
