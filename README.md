# AWS Voice-to-Blog Generator

An AI pipeline that converts voice recordings into blog posts using AWS.

## Tech Stack
- Amazon S3 — audio storage & static blog hosting
- AWS Lambda (Python) — pipeline orchestration
- Amazon Transcribe — speech-to-text
- Amazon Bedrock (Claude) — blog post generation
- IAM — least-privilege service permissions

## Status
- [x] Phase 1: AWS account + GitHub setup
- [x] Phase 2: S3 buckets
- [x] Phase 3: IAM role
- [x] Phase 4: Lambda function
- [ ] Phase 5: S3 event trigger
- [ ] Phase 6: Bedrock access
- [ ] Phase 7: End-to-end test