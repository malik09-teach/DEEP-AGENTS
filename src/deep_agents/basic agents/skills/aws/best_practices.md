# AWS Best Practices

## Security & Reliability

1. **Principle of Least Privilege (PoLP)**:
   - Assign only the exact permissions needed for specific tasks. Avoid `*` wildcard actions on resources in IAM policies.
2. **Encryption Everywhere**:
   - Ensure S3 buckets enforce default server-side encryption (SSE-S3 or SSE-KMS).
   - Use TLS for all API communications.
3. **Cost Optimization**:
   - Clean up idle EC2 instances and unused EBS volumes.
   - Configure S3 lifecycle rules for transitioning older data to Glacier or deleting temporary artifacts.
4. **Monitoring & Logging**:
   - Enable AWS CloudTrail for auditing API calls.
   - Use Amazon CloudWatch alarms for billing and anomalous instance resource utilization.
