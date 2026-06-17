# 🎙️ Voice to Blog Generator

An end-to-end serverless AI pipeline on AWS that automatically converts voice recordings into fully formatted blog posts — in under 60 seconds.

Built as a hands-on cloud portfolio project while completing the AWS Cloud Practitioner course.

---

## 🌐 Live Demo

**Web App:** http://voice-blog-output-lokesh.s3-website-us-east-1.amazonaws.com

Upload or record your voice → get a published blog post automatically.

---

## 🏗️ Architecture

Voice Recording / MP3 Upload

↓

Amazon S3 (input bucket)

↓ event trigger

AWS Lambda (Python)

↓

Amazon Transcribe ──→ speech to text

↓

Amazon Bedrock - Nova Lite ──→ blog post generation

↓

Amazon S3 (output bucket) ──→ static website hosting

↓

Live Blog Post URL

---

## ⚙️ Tech Stack

| Service | Purpose |
|---|---|
| Amazon S3 | Audio storage + static website hosting |
| AWS Lambda (Python 3.12) | Pipeline orchestration |
| Amazon Transcribe | Speech-to-text conversion |
| Amazon Bedrock (Nova Lite) | AI blog post generation |
| Amazon API Gateway | REST API for web frontend |
| AWS IAM | Least-privilege roles and policies |
| Amazon CloudWatch | Logging and monitoring |

---

## ✨ Features

- Record voice directly in the browser or upload an MP3/WAV file
- Automatic speech-to-text transcription via Amazon Transcribe
- AI rewrites the transcript into a structured blog post with title, intro, body and conclusion
- Blog post saved as HTML and published live on S3 static website
- Async polling architecture — no timeouts, real-time status updates
- Dark mode web interface built with vanilla HTML, CSS and JavaScript
- Fully serverless — zero servers to manage

---

## 🚀 How It Works

1. User visits the web app and records voice or uploads an audio file
2. Frontend sends the audio to API Gateway as base64
3. Lambda saves the audio to S3 and starts an Amazon Transcribe job
4. Frontend polls every 5 seconds for job completion
5. Once transcribed, Lambda calls Amazon Bedrock (Nova Lite) with the transcript
6. Nova Lite generates a complete blog post in HTML format
7. Lambda saves the blog post to S3 and returns the live URL
8. Blog post appears in the browser and is publicly accessible

---

## 📁 Project Structure

aws-voice-to-blog/

├── lambda/

│   └── handler.py        # Lambda function — full pipeline logic

├── webapp/

│   └── index.html        # Frontend web app

├── .gitignore

└── README.md

---

## 🛠️ Setup Guide

### Prerequisites
- AWS account with IAM user
- AWS CLI v2 installed and configured
- Python 3.12
- Git

### Step 1 — Clone the repo
```bash
git clone https://github.com/LOKESHJANI/aws-voice-to-blog.git
cd aws-voice-to-blog
```

### Step 2 — Create S3 buckets
```bash
aws s3api create-bucket --bucket your-audio-input --region us-east-1
aws s3api create-bucket --bucket your-blog-output --region us-east-1
aws s3 website s3://your-blog-output/ --index-document index.html
```

### Step 3 — Create IAM role for Lambda
```bash
aws iam create-role \
  --role-name voice-blog-lambda-role \
  --assume-role-policy-document file://trust-policy.json

aws iam attach-role-policy --role-name voice-blog-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name voice-blog-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam attach-role-policy --role-name voice-blog-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonTranscribeFullAccess
aws iam attach-role-policy --role-name voice-blog-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
```

### Step 4 — Deploy Lambda
```bash
cd lambda
zip ../voice-blog-lambda.zip handler.py
cd ..

aws lambda create-function \
  --function-name voice-blog-generator \
  --runtime python3.12 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/voice-blog-lambda-role \
  --handler handler.lambda_handler \
  --zip-file fileb://voice-blog-lambda.zip \
  --timeout 300 \
  --memory-size 256 \
  --region us-east-1
```

### Step 5 — Create API Gateway
```bash
aws apigateway create-rest-api --name voice-blog-api --region us-east-1
```

Then connect it to Lambda and deploy to a `prod` stage.

### Step 6 — Deploy frontend
Update `API_URL` in `webapp/index.html` with your API Gateway URL, then:
```bash
aws s3 cp webapp/index.html s3://your-blog-output/index.html \
  --content-type text/html
```

---

## 💰 AWS Cost Estimate

| Service | Free Tier | Estimated Cost |
|---|---|---|
| S3 | 5GB free | ~$0.00 |
| Lambda | 1M requests free | ~$0.00 |
| Transcribe | 60 min/month free | ~$0.02/min after |
| Bedrock Nova Lite | Pay per token | ~$0.01 per post |
| API Gateway | 1M calls free | ~$0.00 |

**Total for development and testing: under $1**

---

## 📋 Build Progress

- [x] Phase 1: AWS account + GitHub setup
- [x] Phase 2: S3 buckets with static hosting
- [x] Phase 3: IAM role for Lambda
- [x] Phase 4: Lambda function
- [x] Phase 5: S3 event trigger
- [x] Phase 6: Bedrock model access
- [x] Phase 7: End-to-end test
- [x] Phase 8: Web frontend with API Gateway

---

## 🧠 What I Learned

- Designing serverless event-driven architectures on AWS
- Using IAM roles and least-privilege policies for service-to-service security
- Integrating Amazon Transcribe for real-time speech-to-text
- Calling Amazon Bedrock foundation models (Nova Lite) via API
- Building and deploying REST APIs with API Gateway
- Hosting static websites on S3 with public bucket policies
- Async polling patterns to handle long-running cloud jobs
- Debugging Lambda functions with CloudWatch Logs
- Git version control and GitHub for project documentation

---

## 📄 License

MIT License — feel free to fork and build on this project.

---

## 👤 Author

**Lokesh Janakiraman**
Graduate Student | AWS Cloud Practitioner Learner
[GitHub](https://github.com/LOKESHJANI)