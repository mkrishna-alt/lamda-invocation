from flask import Flask, render_template, request, redirect, url_for
import boto3

app = Flask(__name__)

# AWS credentials and SQS queue URL
aws_access_key = ''
aws_secret_key = ''
region_name = 'us-east-1'
queue_url = 'YOUR_SQS_QUEUE_URL'

# Configure AWS credentials
sqs = boto3.client('sqs', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message_body = request.form['message']

    # Send message to SQS
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print("Message sent. MessageId:", response['MessageId'])
    except Exception as e:
        print("Error sending message:", e)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
