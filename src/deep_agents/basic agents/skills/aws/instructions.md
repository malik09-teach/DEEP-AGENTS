# AWS Instructions

## Guidelines for Cloud Operations

1. **Authentication & Credentials**
   - Never hardcode AWS access keys or secret keys in source files or notebooks.
   - Always load credentials from environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`) or IAM roles.
   - Use `boto3.Session()` or environment profiles.

2. **Resource Management**
   - Tag all resources with appropriate metadata (`Environment`, `Owner`, `Project`).
   - Validate existence and state before issuing destructive operations (e.g. terminating instances, deleting buckets).
   - Use pagination when querying large sets of resources (`get_paginator`).

3. **Error Handling & Retries**
   - Catch `botocore.exceptions.ClientError` and check `response['Error']['Code']`.
   - Implement exponential backoff for rate-limited calls (`RequestLimitExceeded`, `ThrottlingException`).
