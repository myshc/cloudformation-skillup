import {S3Client, ListBucketsCommand} from "@aws-sdk/client-s3"

const s3 = new S3Client({})

export const lambda_handler = async (event, context) => {
  try {
    const {Buckets} = await s3.send(new ListBucketsCommand({}))
    const bucketNames = Buckets.map(bucket => bucket.Name)
    const result = bucketNames.join('\n')
    return result
  } catch (err) {
    return err
  }
}
