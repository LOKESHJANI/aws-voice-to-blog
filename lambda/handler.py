import boto3
import json
import time
import urllib.parse
import base64

s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

INPUT_BUCKET = 'voice-blog-audio-input-lokesh'
OUTPUT_BUCKET = 'voice-blog-output-lokesh'

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST, OPTIONS"
}

def start_job(body):
    audio_data = base64.b64decode(body['audio'])
    key = f"uploads/recording-{int(time.time())}.mp3"
    s3.put_object(
        Bucket=INPUT_BUCKET,
        Key=key,
        Body=audio_data,
        ContentType='audio/mpeg'
    )
    print(f"Audio saved: s3://{INPUT_BUCKET}/{key}")

    job_name = f"voice-blog-{int(time.time())}"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f"s3://{INPUT_BUCKET}/{key}"},
        MediaFormat='mp3',
        LanguageCode='en-US',
        OutputBucketName=OUTPUT_BUCKET,
        OutputKey=f"transcripts/{job_name}.json"
    )
    print(f"Transcription started: {job_name}")
    return job_name

def check_job(job_name):
    response = transcribe.get_transcription_job(
        TranscriptionJobName=job_name
    )
    status = response['TranscriptionJob']['TranscriptionJobStatus']
    print(f"Transcription status: {status}")

    if status == 'IN_PROGRESS':
        return {"status": "IN_PROGRESS"}

    if status == 'FAILED':
        return {"status": "FAILED", "error": "Transcription failed"}

    if status == 'COMPLETED':
        transcript_obj = s3.get_object(
            Bucket=OUTPUT_BUCKET,
            Key=f"transcripts/{job_name}.json"
        )
        transcript_data = json.loads(transcript_obj['Body'].read())
        transcript_text = transcript_data['results']['transcripts'][0]['transcript']
        print(f"Transcript: {transcript_text[:100]}...")

        prompt = f"""You are a professional blog writer.
Below is a spoken transcript. Rewrite it as a well-structured,
engaging blog post with a compelling title, short introduction,
clear body paragraphs, and a conclusion.
Fix any filler words, repetitions or grammar issues.
Return the blog post as clean HTML with basic styling
including a centered layout, readable font, and good spacing.

Transcript:
{transcript_text}"""

        print("Calling Amazon Nova Lite...")
        bedrock_response = bedrock.invoke_model(
            modelId='us.amazon.nova-lite-v1:0',
            body=json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ]
            })
        )

        response_body = json.loads(bedrock_response['body'].read())
        blog_html = response_body['output']['message']['content'][0]['text']

        # Strip markdown code fences if Nova Lite wraps response in them
        blog_html = blog_html.strip()
        if blog_html.startswith('```html'):
            blog_html = blog_html[7:]
        if blog_html.startswith('```'):
            blog_html = blog_html[3:]
        if blog_html.endswith('```'):
            blog_html = blog_html[:-3]
        blog_html = blog_html.strip()
        print("Blog post generated")

        post_key = f"posts/{job_name}.html"
        s3.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=post_key,
            Body=blog_html,
            ContentType='text/html'
        )

        blog_url = f"http://{OUTPUT_BUCKET}.s3-website-us-east-1.amazonaws.com/{post_key}"
        print(f"Blog live at: {blog_url}")

        return {
            "status": "COMPLETED",
            "url": blog_url,
            "content": blog_html
        }

def lambda_handler(event, context):
    print("Lambda invoked")

    # Handle OPTIONS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": ""
        }

    body = json.loads(event.get('body', '{}'))
    action = body.get('action', 'start')

    if action == 'start':
        job_name = start_job(body)
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({
                "status": "STARTED",
                "job_id": job_name
            })
        }

    elif action == 'check':
        job_id = body.get('job_id')
        result = check_job(job_id)
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps(result)
        }

    return {
        "statusCode": 400,
        "headers": CORS_HEADERS,
        "body": json.dumps({"error": "Invalid action"})
    }