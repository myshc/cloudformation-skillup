import boto3


def lambda_handler(event, context):
  s3 = boto3.client('s3')
  try:
    buckets_data = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in buckets_data['Buckets']]
    result = '\n'.join(bucket_names)
    return result
  except Exception as ex:
    return ex
